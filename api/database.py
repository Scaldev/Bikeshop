import json

DATABASE_PATH = "api/database.json"

class Database:

    # Getters

    def get_inventory():
        with open(DATABASE_PATH, "r") as file:
            data = json.load(file)
            return data["Inventaire"]
        
    def get_bikes():
        with open(DATABASE_PATH, "r") as file:
            data = json.load(file)
            return data["Description"]
        
    # Setters

    def set_inventory(data):
        with open(DATABASE_PATH, "w") as file:
                json.write(data, file)

    def set_description(data):
        with open(DATABASE_PATH, "w") as file:
                json.write(data, file)
