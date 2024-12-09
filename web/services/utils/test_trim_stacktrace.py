from services.utils.github_issue_manager import _trim_stacktrace, _stacktrace_line_trimer
import unittest


class TrimStacktraceTest(unittest.TestCase):

    def test_user_specific_dirs_are_removed(self):
        username = "my_cool_user_name"
        test_trace = f'File "/home/{username}/mantidworkbench/lib/python3.8/site-packages/mantidqt/widgets/memorywidget/memoryview.py", line 98, in _set_value'\
                      '   @Slot(int, float, float)'\
                      'KeyboardInterrupt'
        self.assertNotIn(username, _trim_stacktrace(test_trace))

    def test_line_trimmer_file_lines(self):
        examples = {
            r'File "C:\MantidInstall\bin\lib\site-packages\mantidqtinterfaces\Muon\GUI\Common\thread_model.py", line 98, in warning':
            r'mantidqtinterfaces/Muon/GUI/Common/thread_model.py", line 98, in warning',
            r'File "/opt/mantidworkbench6.8/lib/python3.10/site-packages/workbench/plotting/figurewindow.py", line 130, in dropEvent':
            r'workbench/plotting/figurewindow.py", line 130, in dropEvent',
            r'File "D:\Mantid\Software\MantidInstall\bin\lib\site-packages\mantidqt\widgets\codeeditor\execution.py", line 153, in execute':
            r'mantidqt/widgets/codeeditor/execution.py", line 153, in execute',
            r'File "/opt/mantidworkbenchnightly/scripts/ExternalInterfaces/mslice/presenters/workspace_manager_presenter.py", line 112, in _save_to_ads':
            r'scripts/ExternalInterfaces/mslice/presenters/workspace_manager_presenter.py", line 112, in _save_to_ads',
            r"at line 152 in '/usr/local/anaconda/envs/mantid-dev/plugins/python/algorithms/ConvertWANDSCDtoQ.py'":
            r'at line 152 in plugins/python/algorithms/ConvertWANDSCDtoQ.py',
            r'File "/opt/mantidworkbench6.9/lib/python3.10/site-packages/mantid/simpleapi.py", line 1083, in __call__':
            r'mantid/simpleapi.py", line 1083, in __call__'
        }
        for original, expected_trim in examples.items():
            self.assertEqual(_stacktrace_line_trimer(original), expected_trim)

    def test_line_trimmer_other_lines(self):
        examples = {
            "OverflowError: can't convert negative int to unsigned",
            "self.view.editor.updateProgressMarker(lineno, True)",
            "Exception: unknown",
            "ax.make_legend()",
            "KeyError: 'hide_errors'"
        }
        for line in examples:
            self.assertEqual(_stacktrace_line_trimer(line), line)


if __name__ == '__main__':
    unittest.main()
