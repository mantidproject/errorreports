from services.models import ErrorReport, GithubIssue
from services.utils.decompress_cpp_traces import decompress_cpp_traces

import re
import pathlib
import os
import logging
from string import Template
from github import Github, Auth

logger = logging.getLogger()
line_exp = re.compile(
    r"\s*File \".*(mantid|mantidqt|mantidqtinterfaces|"
    r"workbench|scripts|plugins)"
    r"(\/|\\)(.*)(\", line \d+, in \S+)"
)
alt_line_exp = re.compile(
    r"\s*(at line \d+ in )\'.*(mantid|mantidqt|"
    r"mantidqtinterfaces|workbench|scripts|plugins)"
    r"(\/|\\)(.*)\'"
)
ISSUE_TEXT = Template("""
Name: $name
Email: $email

Mantid version: $version
OS: $os

**Additional Information**
$info

**Stack trace**
```$stacktrace```
""")
COMMENT_TEXT = Template("""
Name: $name
Email: $email

Mantid version: $version
OS: $os

**Additional Information**
$info
""")


def get_or_create_github_issue(report) -> GithubIssue | None:
    """
    Given the stacktrace from the report, search for database entries with the
    same trace. If found and there is a linked github issue, leave a comment
    with the report's key information. If not, create a new issue.

    Return None in the following cases:
     - There is no stack trace and no additional information in the report
     - A GIT_AUTH_TOKEN has not been set
     - The bug has already been submitted by the user (identified via the uid)
       and they have not left any additional information

    Args:
        report: The report recieved by ErrorViewSet

    Returns:
        GithubIssue | None: A reference to a new or existing GithubIssue table
        entry, or None
    """
    stacktrace = report.get("stacktrace")
    text_box = report.get("textBox")
    cpp_compressed_traces = report.get("cppCompressedTraces")
    if not any([stacktrace, text_box, cpp_compressed_traces]):
        logger.info(
            "No stacktrace or info in the report; skipping github issue interaction"
        )
        return None

    git_access_token = os.getenv("GIT_AUTH_TOKEN")
    issue_repo = os.getenv("GIT_ISSUE_REPO")
    if not git_access_token:
        logger.info("No GIT_AUTH_TOKEN provided; skipping github issue interaction")
        return None

    logger.error(f"This is the token=[{git_access_token}] and this is the repo=[{issue_repo}]")

    auth = Auth.Token(git_access_token)
    g = Github(auth=auth)
    repo = g.get_repo(issue_repo)

    github_issue = _search_for_matching_stacktrace(stacktrace)
    if github_issue and issue_repo == github_issue.repoName:
        issue_number = github_issue.issueNumber
        if (
            _search_for_repeat_user(report["uid"], github_issue)
            and not report["textBox"]
        ):
            return github_issue

        comment_text = COMMENT_TEXT.substitute(
            name=report["name"],
            email=report["email"],
            os=report["osReadable"],
            version=report["mantidVersion"],
            info=report["textBox"],
        )
        issue = repo.get_issue(number=int(issue_number))
        issue.create_comment(comment_text)
        logger.info(f"Added comment to issue {issue.url})")
        return github_issue
    else:
        trace = stacktrace
        if cpp_compressed_traces:
            trace = decompress_cpp_traces(cpp_compressed_traces)

        issue_text = ISSUE_TEXT.substitute(
            name=report["name"],
            email=report["email"],
            os=report["osReadable"],
            version=report["mantidVersion"],
            info=report["textBox"],
            stacktrace=trace,
        )
        error_report_label = repo.get_label("Error Report")
        issue = repo.create_issue(
            title="Automatic error report", labels=[error_report_label], body=issue_text
        )
        logger.info(f"Created issue {issue.url})")
        return GithubIssue.objects.create(repoName=issue_repo, issueNumber=issue.number)


def _trim_stacktrace(stacktrace: str) -> str:
    """
    Returns a trimmed and os non-specific version of the stacktrace given
    """
    return "\n".join([_stacktrace_line_trimer(line) for line in stacktrace.split("\n")])


def _stacktrace_line_trimer(line: str) -> str:
    """
    Returns a trimmed and os non-specific version of the stacktrace line given
    """
    match = line_exp.match(line)
    if match:
        path = pathlib.PureWindowsPath(os.path.normpath("".join(match.group(1, 2, 3))))
        return path.as_posix() + match.group(4)

    match = alt_line_exp.match(line)
    if match:
        path = pathlib.PureWindowsPath(os.path.normpath("".join(match.group(2, 3, 4))))
        return match.group(1) + path.as_posix()

    return line


def _search_for_matching_stacktrace(trace: str) -> GithubIssue | None:
    """
    Search the database for a matching stack trace (irrespective of os, local
    install location etc.)

    Args:
        trace (str): Raw stack trace from the report

    Returns:
        str | None: Either a GithubIssue entry, or None
    """
    if not trace:
        return None
    trimmed_trace = _trim_stacktrace(trace)
    for raw_trace, github_issue in ErrorReport.objects.exclude(
        githubIssue__isnull=True
    ).values_list("stacktrace", "githubIssue"):
        if _trim_stacktrace(raw_trace) == trimmed_trace:
            return GithubIssue.objects.get(id=github_issue)
    return None


def _search_for_repeat_user(uid: str, github_issue: GithubIssue) -> bool:
    """
    Return true if the user id has already submitted the same error
    """
    return any(
        [
            uid == entry_uid
            for entry_uid in ErrorReport.objects.filter(
                githubIssue=github_issue
            ).values_list("uid")
        ]
    )
