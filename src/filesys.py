import os

class FileSys:
    _instances = {}
    _base_dir = "user_files"

    def __new__(cls, username):
        if username not in cls._instances:
            instance = super().__new__(cls)
            instance.username = username
            os.makedirs(cls._base_dir, exist_ok=True)
            cls._instances[username] = instance
        return cls._instances[username]

    def _get_user_file_path(self):
        filename = f"{self.username}.txt"
        return os.path.join(self._base_dir, filename)

    def write(self, content):
        filepath = self._get_user_file_path()
        try:
            with open(filepath, "a") as f:
                f.write(content + "\n")
            return True
        except Exception as e:
            print(f"Error writing to {filepath}: {e}")
            return False

    def read(self):
        filepath = self._get_user_file_path()
        try:
            with open(filepath, "r") as f:
                return f.read()
        except FileNotFoundError:
            return None
        except Exception as e:
            print(f"Error reading from {filepath}: {e}")
            return None