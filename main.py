import os
import logging
from functools import wraps


# ==========================
#       CUSTOM ERRORS
# ==========================

class FileNotFound(Exception):
    """File not found."""
    pass


class FileCorrupted(Exception):
    """File is corrupted or inaccessible."""
    pass


# ==========================
#   GLOBAL LOGGER CONFIG
# ==========================

def configure_logger(mode="console"):
    logger = logging.getLogger("file_logger")
    logger.setLevel(logging.ERROR)

    # Avoid duplicate handlers
    if not logger.handlers:
        if mode == "console":
            handler = logging.StreamHandler()
        else:
            handler = logging.FileHandler("log.txt")

        formatter = logging.Formatter("%(asctime)s - %(name)s - %(message)s")
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    return logger


# ==========================
#     DECORATOR logged
# ==========================

def logged(exception_type, mode="console"):
    """
    Decorator for logging errors.
    mode = "console" → log to console
    mode = "file"    → log to log.txt
    """

    logger = configure_logger(mode)

    def decorator(func):

        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)

            except exception_type as e:
                logger.error(f"{exception_type.__name__}: {str(e)}")
                raise

        return wrapper

    return decorator


# ==========================
#     MAIN CLASS
# ==========================

class WorkWithFile:
    def __init__(self, filename: str):
        self.filename = filename

        # Check file existence
        if not os.path.exists(self.filename):
            raise FileNotFound(f"File '{self.filename}' not found!")

        # Check accessibility
        try:
            with open(self.filename, "r", encoding="utf-8"):
                pass
        except (OSError, IOError):
            raise FileCorrupted("File is corrupted or inaccessible!")

    # --------------------------
    #           READ
    # --------------------------
    @logged(FileCorrupted, mode="console")
    def read(self):
        with open(self.filename, "r", encoding="utf-8") as f:
            return f.read()

    # --------------------------
    #           WRITE
    # --------------------------
    @logged(FileCorrupted, mode="file")
    def write(self, text: str):
        with open(self.filename, "w", encoding="utf-8") as f:
            f.write(text)

    # --------------------------
    #           APPEND
    # --------------------------
    @logged(FileCorrupted, mode="file")
    def append(self, text: str):
        with open(self.filename, "a", encoding="utf-8") as f:
            f.write(text)


# ==========================
#      DEMO (optional)
# ==========================

if __name__ == "__main__":
    try:
        file = WorkWithFile("text.txt")

        print("=== READ ===")
        print(file.read())

        print("\n=== WRITE ===")
        file.write("Hello!\n")

        print("\n=== APPEND ===")
        file.append("Appended line.\n")

    except FileNotFound as e:
        print(e)
    except FileCorrupted as e:
        print(e)
