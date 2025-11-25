import os

FILE = os.path.join(os.path.dirname(__file__), "user_name.txt")

def set_name(name: str):
    name = name.strip()
    if not name:
        return
    with open(FILE, "w", encoding="utf-8") as f:
        f.write(name)

def get_name():
    if not os.path.exists(FILE):
        return None
    with open(FILE, "r", encoding="utf-8") as f:
        return f.read().strip()
