class AppException(Exception):
    """Base exception for the entire application"""
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)


# -----------------------------
# File Upload Errors
# -----------------------------
class FileUploadException(AppException):
    pass


# -----------------------------
# Processing Errors (OCR / NLP)
# -----------------------------
class ProcessingException(AppException):
    pass


# -----------------------------
# Database Errors
# -----------------------------
class DatabaseException(AppException):
    pass


# -----------------------------
# ML Model Errors
# -----------------------------
class ModelException(AppException):
    pass
