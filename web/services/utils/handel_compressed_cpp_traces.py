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
    traces = re.split(r'\nTraceback for ', cpp_traces_from_pystack)
    if len(traces) > 1:
        # Trim boilerplate output
        traces = traces[1:]
    filtered_traces = ["Traceback for " + trace_back for trace_back in
                       traces if _search_for_mantid_codein_trace(trace_back)]
    # On built versions we might not get the file paths so the filter will find
    # nothing, in this case just reurn everything.
    return filtered_traces if filtered_traces != [] else traces


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
