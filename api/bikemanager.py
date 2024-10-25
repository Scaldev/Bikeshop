from api.database import Database

class BikeManager:

    # Getters

    def get_bike_locations(id):
        inventory = Database.get('Inventaire')
        if id in inventory:
            return inventory[id]
        return []
    
    def get_bike_data(id):
         description = Database.get('Description')
         if id in description:
              return description[id]
         return []

    # Setters

    def add_bike_in_inventory(id, location):
        data = Database.get()
        data['Inventaire'][id].append(location)
        data['Inventaire'][id].sort()
        Database.set(data)

    def remove_bike_from_inventory(id, location):
        data = Database.get()
        data['Inventaire'][id].remove(location)
        Database.set(data)
    
    ###############################################################

    # Get data

    def get_bikes():
        bikes = []
        desc = Database.get('Description')
        for k in desc:
            bikes.append([k, desc[k][0], desc[k][1]])
        return bikes

    def get_available_bikes():
        bikes_available = []
        desc = Database.get('Description')
        inventory = Database.get('Inventaire')
        for k in inventory:
            if len(inventory[k]) != 0:
                bikes_available.append([k, desc[k][0], desc[k][1]])
        return bikes_available
    
    def is_available(id):
        locations = BikeManager.get_bike_locations(id)
        return locations != []
    
    # Setters

    def buy_bike(id, location):
        locations = BikeManager.get_bike_locations(id)
        if location in locations:
            return BikeManager.remove_bike(id, location)
        return False
    
    def transaction(fields, date):

        code = fields['code']

        transaction = {
            "date": date,
            "code": code,
            "email": fields['email'],
            "nom": fields['nom'],
            "adresse": fields['adresse'] + ", " + fields['ville'] + " " + fields['postal']
        }

        db = Database.get()
        db['Transactions'].append(transaction)
        Database.set(db)

        locations = BikeManager.get_bike_locations(code)
        location = locations.pop()

        BikeManager.remove_bike_from_inventory(code, location)

        return True
