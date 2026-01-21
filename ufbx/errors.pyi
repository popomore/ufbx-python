"""
Type stubs for ufbx.errors module
"""



class UfbxError(Exception):
    """Base exception for all ufbx errors"""
    error_type: int

    def __init__(self, message: str, error_type: int = 0) -> None: ...


class UfbxFileNotFoundError(UfbxError):
    """Exception raised when FBX file is not found"""
    ...


class UfbxIOError(UfbxError):
    """Exception raised for I/O errors"""
    ...


class UfbxOutOfMemoryError(UfbxError):
    """Exception raised when out of memory"""
    ...
