from api.database import Database

class BikeManager:

    # Getters

    def get_bike_locations(id):
        inventory = Database.get_inventory()
        if id in inventory:
            return inventory[id]
        return []
    
    def get_bike_data(id):
         bikes = Database.get_bikes()
         if id in bikes:
              return bikes[id]
         return []

    # Setters

    def add_bike_in_inventory(id, location):
        inventory: list = Database.get_inventory()
        inventory.append(location)
        inventory.sort()
        Database.set_inventory(inventory)

    def remove_bike_from_inventory(id, location):
        inventory: list = Database.get_inventory()
        inventory.remove(location)
        inventory.sort()
        Database.set_inventory(inventory)

    # Utils

    def get_bikes():
        result = []
        bikes = Database.get_bikes()
        for k in bikes:
            result.append([k, bikes[k][0], bikes[k][1]])
        return result

    def get_available_bikes():
        result = []
        bikes = Database.get_bikes()
        inventory = Database.get_inventory()
        for k in inventory:
            if len(inventory[k]) != 0:
                result.append([k, bikes[k][0], bikes[k][1]])
        return result
    
    def buy_bike(id, location):
        locations = BikeManager.get_bike_locations(id)
        if location in locations:
            return BikeManager.remove_bike(id, location)
        return False
    
    def is_available(id):
        locations = BikeManager.get_bike_locations(id)
        return locations != []