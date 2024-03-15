from services.models import ErrorReport

import re
import pathlib
import os

line_exp = re.compile(r"\s*File \".*(mantidqt|mantidqtinterfaces|workbench|scripts)(\/|\\)(.*)(\", line \d+, in \S+)")


def get_or_create_github_issue(report) -> str:
    issue_number = _search_for_matching_stacktrace(report["stacktrace"])
    if issue_number:
        pass
    pass

def _trim_stacktrace(stacktrace: str) -> str:
    return '\n'.join([_stacktrace_line_trimer(line) for line in stacktrace.split('\n')])

def _stacktrace_line_trimer(line: str) -> str:
    match = line_exp.match(line)
    if match:
        path = pathlib.PureWindowsPath(os.path.normpath("".join(match.group(1,2,3))))
        return path.as_posix() + match.group(4)
    return line

def _search_for_matching_stacktrace(trace: str) -> str | None:
    trimmed_trace = _trim_stacktrace(trace)
    for raw_trace, issue_number in ErrorReport.objects.exclude(githubIssueNumber__exact='').values_list('stacktrace', 'githubIssueNumber'):
        if _trim_stacktrace(raw_trace) == trimmed_trace:
            return issue_number
    return None
