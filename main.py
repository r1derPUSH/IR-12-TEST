import os
import logging
from functools import wraps


# ==========================
#       CUSTOM ERRORS
# ==========================

class FileNotFound(Exception):
    pass


class FileCorrupted(Exception):
    pass


# ==========================
#   LOGGER CONFIG
# ==========================

def configure_logger(mode="console"):
    logger = logging.getLogger("file_logger")
    logger.setLevel(logging.ERROR)

    if not logger.handlers:
        handler = logging.StreamHandler() if mode == "console" else logging.FileHandler("log.txt")
        formatter = logging.Formatter("%(asctime)s - %(message)s")
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    return logger


# ==========================
#      DECORATOR
# ==========================

def logged(exception_type, mode="console"):
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
#     MAIN FILE CLASS
# ==========================

class WorkWithFile:
    def __init__(self, filename: str):
        self.filename = filename

        # Auto-create file if missing
        if not os.path.exists(self.filename):
            with open(self.filename, "w", encoding="utf-8") as f:
                f.write("")

        # Check accessibility
        try:
            with open(self.filename, "r", encoding="utf-8"):
                pass
        except (OSError, IOError):
            raise FileCorrupted("File is corrupted or inaccessible!")

    @logged(FileCorrupted)
    def read(self):
        with open(self.filename, "r", encoding="utf-8") as f:
            return f.read()

    @logged(FileCorrupted, mode="file")
    def append(self, text: str):
        with open(self.filename, "a", encoding="utf-8") as f:
            f.write(text + "\n")


# ==========================
#      TERMINAL INPUT
# ==========================

if __name__ == "__main__":
    file = WorkWithFile("text.txt")

    print("==== FILE LOGGER ====")
    print("Вводь текст, він буде автоматично записаний у text.txt")
    print("Напиши 'exit' щоб вийти.\n")

    while True:
        user_input = input("> ")

        if user_input.lower() == "exit":
            print("\n=== FINAL FILE CONTENT ===")
            print(file.read())
            print("==========================")
            break

        file.append(user_input)

        print("✔ Записано!")
        print("Поточний вміст файлу:")
        print(file.read())
        print("----------------------")
