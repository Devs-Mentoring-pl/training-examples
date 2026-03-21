import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DB_NAME = "users.sqlite3"
DB_PATH = os.path.join(BASE_DIR, "..", "instance", DB_NAME)
