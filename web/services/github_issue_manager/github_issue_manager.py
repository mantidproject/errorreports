from services.models import ErrorReport, GithubIssue

import re
import pathlib
import os
import logging
from string import Template
from github import Github, Auth

logger = logging.getLogger()
line_exp = re.compile(r"\s*File \".*(mantidqt|mantidqtinterfaces|workbench|scripts)(\/|\\)(.*)(\", line \d+, in \S+)")
issue_text_template = Template("""
Name: $name
Email: $email

Mantid version: $version
OS: $os
                               
**Additionl Information**
$info

**Stack trace**
```$stacktrace```
""")
comment_text_template = Template("""
Name: $name
Email: $email

Mantid version: $version
OS: $os

**Additionl Information**
$info                                
""")


def get_or_create_github_issue(report) -> GithubIssue | None:
    """
    Given the stacktrace from the report, search for database entries with the same trace.
    If found and there is a linked github issue, leave a comment with the report's key information.
    If not, create a new issue.

    Return None in the following cases:
     - There is no stack trace and no additional information in the report
     - A GIT_AUTH_TOKEN has not been set
     - The bug has already been submitted by the user (identified via the uid) and they have not left any additional information

    Args:
        report: The report recived by ErrorViewSet

    Returns:
        GithubIssue | None: A reference to a new or existing GithubIssue table entry, or None
    """
    if not report.get('stacktrace') and not report.get('textBox'):
        logger.info('No stacktrace or info in the report; skipping github issue interaction')
        return None

    git_access_token = os.getenv('GIT_AUTH_TOKEN')
    issue_repo = os.getenv('GIT_ISSUE_REPO')
    if not git_access_token:
        logger.info('No GIT_AUTH_TOKEN provided; skipping github issue interaction')
        return None

    auth = Auth.Token(git_access_token)
    g = Github(auth=auth)
    repo = g.get_repo(issue_repo)

    github_issue = _search_for_matching_stacktrace(report["stacktrace"])
    if github_issue and issue_repo == github_issue.repoName:
        issue_number = github_issue.issueNumber
        if _search_for_repeat_user(report['uid'], github_issue) and not report['textBox']:
            return github_issue
            
        comment_text = comment_text_template.substitute(name=report['name'],
                                                        email=report['email'],
                                                        os=report['osReadable'],
                                                        version=report['mantidVersion'],
                                                        info=report['textBox'])
        issue = repo.get_issue(number=int(issue_number))
        issue.create_comment(comment_text)
        logger.info(f'Added comment to issue \#{issue_number} ({issue_repo})')
        return github_issue
    else:
        issue_text = issue_text_template.substitute(name=report['name'],
                                                    email=report['email'],
                                                    os=report['osReadable'],
                                                    version=report['mantidVersion'],
                                                    info=report['textBox'],
                                                    stacktrace=report['stacktrace'])
        issue = repo.create_issue(title="Automatic error report", body=issue_text)
        logger.info(f'Created issue \#{issue.number} ({issue_repo})')
        return GithubIssue.objects.create(repoName=issue_repo,
                                          issueNumber=issue.number)

def _trim_stacktrace(stacktrace: str) -> str:
    """
    Returns a rimmed and os non-specific version of the stacktrace given
    """
    return '\n'.join([_stacktrace_line_trimer(line) for line in stacktrace.split('\n')])

def _stacktrace_line_trimer(line: str) -> str:
    """
    Returns a trimmed and os non-specific version of the stacktrace line given
    """
    match = line_exp.match(line)
    if match:
        path = pathlib.PureWindowsPath(os.path.normpath("".join(match.group(1,2,3))))
        return path.as_posix() + match.group(4)
    return line

def _search_for_matching_stacktrace(trace: str) -> GithubIssue | None:
    """
    Search the database for a matching stack trace (irrespective of os, local install location etc.)

    Args:
        trace (str): Raw stack trace from the report

    Returns:
        str | None: Either a GithubIssue entry, or None
    """
    if not trace:
        return None
    trimmed_trace = _trim_stacktrace(trace)
    for raw_trace, github_issue in ErrorReport.objects.exclude(githubIssue__isnull=True).values_list('stacktrace', 'githubIssue'):
        if _trim_stacktrace(raw_trace) == trimmed_trace:
            return GithubIssue.objects.get(id=github_issue)
    return None

def _search_for_repeat_user(uid: str, github_issue: GithubIssue) -> bool:
    """
    Return true if the user id has already submitted the same error
    """
    for entry_uid in ErrorReport.objects.filter(githubIssue=github_issue).values_list('uid'):
        if uid == entry_uid:
            return True
    return False
