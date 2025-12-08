import os
import logging
from functools import wraps


# ==========================
#       CUSTOM ERRORS
# ==========================

class FileNotFound(Exception):
    """Файл не знайдено."""
    pass


class FileCorrupted(Exception):
    """Файл пошкоджений або недоступний."""
    pass


# ==========================
#     DECORATOR logged
# ==========================

def logged(exception_type, mode="console"):
    """
    Декоратор для логування помилок.
    mode = "console" → лог в консоль
    mode = "file"    → лог у log.txt
    """

    def decorator(func):

        @wraps(func)
        def wrapper(*args, **kwargs):

            logger = logging.getLogger(func.__name__)
            logger.setLevel(logging.ERROR)

            # Видалити старі хендлери, щоб не дублювалися
            if logger.hasHandlers():
                logger.handlers.clear()

            # Обираємо режим
            if mode == "console":
                handler = logging.StreamHandler()
            else:
                handler = logging.FileHandler("log.txt")

            formatter = logging.Formatter("%(asctime)s-%(name)s - %(message)s")
            handler.setFormatter(formatter)
            logger.addHandler(handler)

            try:
                return func(*args, **kwargs)

            except exception_type as e:
                logger.error(f"{exception_type.__name__}: {str(e)}")
                raise

            finally:
                logger.removeHandler(handler)

        return wrapper

    return decorator


# ==========================
#     MAIN CLASS
# ==========================

class WorkWithFile:
    def __init__(self, filename: str):
        self.filename = filename

        # Перевірка існування
        if not os.path.exists(self.filename):
            raise FileNotFound(f"Файл '{self.filename}' не знайдено!")

        # Перевірка доступу
        try:
            with open(self.filename, "r", encoding="utf-8"):
                pass
        except Exception:
            raise FileCorrupted("Файл пошкоджений або недоступний!")

    # --------------------------
    #           READ
    # --------------------------
    @logged(FileCorrupted, mode="console")
    def read(self):
        try:
            with open(self.filename, "r", encoding="utf-8") as f:
                return f.read()
        except Exception as e:
            raise FileCorrupted("Не вдалося прочитати файл") from e

    # --------------------------
    #           WRITE
    # --------------------------
    @logged(FileCorrupted, mode="file")
    def write(self, text: str):
        try:
            with open(self.filename, "w", encoding="utf-8") as f:
                f.write(text)
        except Exception as e:
            raise FileCorrupted("Помилка запису у файл") from e

    # --------------------------
    #           APPEND
    # --------------------------
    @logged(FileCorrupted, mode="file")
    def append(self, text: str):
        try:
            with open(self.filename, "a", encoding="utf-8") as f:
                f.write(text)
        except Exception as e:
            raise FileCorrupted("Не вдалося дописати у файл") from e


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
