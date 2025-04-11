from django.test import TestCase
from services.utils.handel_compressed_cpp_traces import (
    extract_mantid_code_threads_from_cpp_traces)

import base64
from pathlib import Path
import zlib


test_data_path = Path(__file__).parent / "test_data"


class HandleCppTracesTest(TestCase):

    def _compress_and_call(self, traces: str):
        compressed_bytes = zlib.compress(traces.encode("utf-8"))
        return extract_mantid_code_threads_from_cpp_traces(
            base64.standard_b64encode(compressed_bytes))

    def test_extract_mantid_code_handles_unformatted_input(self):
        traces = "This is some unexpected output from pytest" \
                 "It has two lines."
        self.assertEqual([traces], self._compress_and_call(traces))

    def test_extract_mantid_code_tims_out_the_boilerplate(self):
        traces = ""
        with open(test_data_path / 'boilerplate_and_trace.txt') as fp:
            traces = ''.join(fp.readlines())

        with open(test_data_path / 'trace_without_boilerplate.txt') as fp:
            expected_output = ''.join(fp.readlines())
            self.assertEqual([expected_output],
                             "Traceback for " + self._compress_and_call(traces)
                             )

    def test_extract_mantid_code_filters_non_mantid_threads(self):
        traces = ""
        with open(test_data_path / 'boilerplate_and_mantid_trace.txt') as fp:
            traces = ''.join(fp.readlines())

        with open(test_data_path / 'just_mantid_traces.txt') as fp:
            expected_output = ''.join(fp.readlines())
            expected_output = expected_output.split('\n\n')
            self.assertEqual(expected_output,
                             self._compress_and_call(traces))
