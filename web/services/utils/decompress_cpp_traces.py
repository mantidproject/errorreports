import base64
import zlib


def decompress_cpp_traces(compressed_cpp_traces: str):
    """
    Decompress the output from pystack core which is sent from the Mantid
    error reporter.
    """
    return zlib.decompress(base64.standard_b64decode(compressed_cpp_traces)).decode(
        "utf-8"
    )
