
import json

def get_users():
    with open("database.json") as f:
        data = json.load(f)
    return data["users"]
