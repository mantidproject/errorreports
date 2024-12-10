import base64
import re
import zlib


def extract_mantid_code_threads_from_cpp_traces(compressed_cpp_traces: str):
    """
    Take base64 encoded string of the compressed output from pystack core.
    Return a list of trace back threads which includes code from
    the mantid repo.
    """
    cpp_traces_from_pystack = zlib.decompress(
        base64.standard_b64decode(compressed_cpp_traces)).decode("utf-8")
    return ["Traceback for " + trace_back for trace_back in
            re.split(r'\nTraceback for ', cpp_traces_from_pystack)[1:] if
            _search_for_mantid_codein_trace(trace_back)]


def _search_for_mantid_codein_trace(trace_back: str) -> bool:
    cpp_mantid_code = re.search(
        r"^\s*\(C\) File \".*/(mantid|mantidqt|mantidqtinterfaces|workbench|"
        r"scripts|plugins)/.*$",
        trace_back,
        re.MULTILINE) is not None
    python_mantid_code = re.search(
        r"^\s*\(Python\) File \".*/(mantid|"
        r"mantidqt|mantidqtinterfaces|workbench|scripts|plugins)/.*$",
        trace_back,
        re.MULTILINE) is not None
    return cpp_mantid_code or python_mantid_code
