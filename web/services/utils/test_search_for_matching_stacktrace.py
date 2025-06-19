from django.test import TestCase
from services.models import ErrorReport, GithubIssue
from services.utils.github_issue_manager import _search_for_matching_stacktrace


class MatchingStackTraceSearchTest(TestCase):
    entries = [
        ('  File "/home/username/mantidworkbench/lib/python3.8/site-packages/mantidqt/widgets/memorywidget/memoryview.py", line 98, in _set_value'
         '    @Slot(int, float, float)'
         'KeyboardInterrupt',
         '1'),
        (r'  File "C:\MantidInstall\bin\mantidqt\widgets\workspacedisplay\matrix\table_view_model.py", line 172, in data'
          '    return str(self.relevant_data(row)[index.column()])'
          'OverflowError: can\'t convert negative int to unsigned',
          '2'),
        (r' File "C:\MantidInstall\bin\mantidqt\widgets\codeeditor\interpreter.py", line 363, in _on_exec_error'
          '   self.view.editor.updateProgressMarker(lineno, True)'
          'RuntimeError: wrapped C/C++ object of type ScriptEditor has been deleted',
          '3'),
        (r'  File "C:\MantidInstall\bin\lib\site-packages\mantidqt\widgets\plotconfigdialog\curvestabwidget\presenter.py", line 367, in line_apply_to_all'
          '    self.apply_properties()'
         r'  File "C:\MantidInstall\bin\lib\site-packages\mantidqt\widgets\plotconfigdialog\curvestabwidget\presenter.py", line 69, in apply_properties'
          '    FigureErrorsManager.toggle_errors(curve, view_props)'
         r'  File "C:\MantidInstall\bin\lib\site-packages\workbench\plotting\figureerrorsmanager.py", line 108, in toggle_errors'
          '    hide_errors = view_props.hide_errors or view_props.hide'
         r'  File "C:\MantidInstall\bin\lib\site-packages\mantidqt\widgets\plotconfigdialog\curvestabwidget\__init__.py", line 137, in __getattr__'
          '    return self[item]'
          'KeyError: \'hide_errors\'',
          '4'),
    ]

    def setUp(self):
        defaults = {
            'uid': '123',
            'host': 'test_host',
            'dateTime': '2014-12-08T18:50:35.817942000',
            'osName': 'Liunx',
            'osArch': 'x86_64',
            'osVersion': 'ubuntu',
            'ParaView': '3.98.1',
            'mantidVersion': '6.6.0',
            'mantidSha1': 'e9423bdb34b07213a69caa90913e40307c17c6cc'
        }
        for trace, issue_number in self.entries:
            issue = GithubIssue.objects.create(repoName="my/repo", issueNumber=issue_number)
            ErrorReport.objects.create(stacktrace=trace, githubIssue=issue, **defaults)

    def test_retrieve_issue_number_with_identical_trace(self):
        for trace, issue_number in self.entries:
            self.assertEqual(issue_number, _search_for_matching_stacktrace(trace).issueNumber)

    def test_retrieve_issue_number_with_different_path_seperators(self):
        for trace, issue_number in self.entries:
            altered_trace = trace.replace('/', '\\') if '/' in trace else trace.replace('\\', '/')
            self.assertEqual(issue_number, _search_for_matching_stacktrace(altered_trace).issueNumber)

    def test_different_user_name_yields_same_issue_number(self):
        trace, issue_number = self.entries[0]
        trace.replace('username', 'different_username')
        self.assertEqual(issue_number, _search_for_matching_stacktrace(trace).issueNumber)

    def test_different_install_location_yields_same_issue_number(self):
        trace, issue_number = self.entries[1]
        trace.replace('MantidInstall', 'my\\mantid\\install')
        self.assertEqual(issue_number, _search_for_matching_stacktrace(trace).issueNumber)

