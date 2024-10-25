import json

DATABASE_PATH = "api/database.json"

class Database:

    def get(name=""):
          with open(DATABASE_PATH, "r") as file:
            data = json.load(file)
            return data if name == "" else data[name]

    def set(data):
        with open(DATABASE_PATH, "w") as file:
                file.write(json.dumps(data))
                