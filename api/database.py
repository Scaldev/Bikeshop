import json

DATABASE_PATH = "api/database.json"

class Database:

    def get(name=""):
          """
          :param name: the name of a table.
          :return: the content of that table, or the whole database if none was provided.
          """
          with open(DATABASE_PATH, "r") as file:
            data = json.load(file)
            return data if name == "" else data[name]

    def set(data):
        """
        Overwrites the database with new data.
        data must contains EVERY table (catalog, inventory and transactions).
        :param data: a database.
        """
        with open(DATABASE_PATH, "w") as file:
                file.write(json.dumps(data))
                