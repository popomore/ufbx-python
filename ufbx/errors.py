"""
ufbx Exception Class Definitions
"""

class UfbxError(Exception):
    """Exception raised when ufbx operation fails"""

    def __init__(self, message: str, error_code: int = 0):
        super().__init__(message)
        self.message = message
        self.error_code = error_code

    def __str__(self):
        if self.error_code:
            return f"UfbxError({self.error_code}): {self.message}"
        return f"UfbxError: {self.message}"


class UfbxFileNotFoundError(UfbxError):
    """File not found"""
    pass


class UfbxOutOfMemoryError(UfbxError):
    """Out of memory"""
    pass


class UfbxIOError(UfbxError):
    """IO error"""
    pass
