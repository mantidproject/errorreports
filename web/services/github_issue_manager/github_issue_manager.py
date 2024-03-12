import re
import pathlib
import os

line_exp = re.compile(r"File \".*(mantidqt|mantidqtinterfaces|workbench|scripts)(\/|\\)(.*)(\", line \d+, in \S+)")


def get_or_create_github_issue(report) -> str:
    trimmed_stack_trace = _trim_stacktrace(report["stacktrace"])
    issue_number = _search_for_matching_stacktrace(trimmed_stack_trace)
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

def _search_for_matching_stacktrace(trimmed_trace: str) -> str | None:
    pass