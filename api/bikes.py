from api.database import Database

CATALOG = "catalog"
INVENTORY = "inventory"
TRANSACTIONS = "transactions"

################################################################################################
#                                            GETTERS                                           #
################################################################################################

def get_bike_locations(id: str) -> list[str] :
    """
    :param id: a bike id.
    :return: the list of locations with that bike in the inventory.
    """
    inventory = Database.get(INVENTORY)
    if id in inventory:
        return inventory[id]
    return []

def get_bike_description(id: str) -> list[str] :
    """
    :param id: a bike id.
    :return: [n, sd, lg], with:

        - n  the name              of the bike.
        - sd the short description of the bike.
        - ld the long  description of the bike.
    """
    catalog = Database.get(CATALOG)
    if id in catalog:
        return catalog[id]
    return []

def get_catalog() -> list[list[str]]:
    """
    :return: a [id, n, sd, ld] list of bikes data, with:
        
        - id the id                of a bike.
        - n  the name              of a bike.
        - sd the short description of a bike.
        - ld the long  description of a bike.
    """
    bikes = []
    catalog = Database.get(CATALOG)
    for id in catalog:
        bikes.append([id] + catalog[id])
    return bikes

def get_available_bikes():
    """
    :return: a [id, n, sd, ld] list of available bikes data, with:
        
        - id the id                of a bike.
        - n  the name              of a bike.
        - sd the short description of a bike.
        - ld the long  description of a bike.
    """
    bikes_available = []
    catalog = Database.get(CATALOG)
    inventory = Database.get(INVENTORY)
    for id in inventory:
        if len(inventory[id]) != 0:
            bikes_available.append([id] + catalog[id])
    return bikes_available

def is_in_inventory(id: str) -> bool:
    """
    :param id: a bike id.
    :return: true iff there is a bike with this id and with at least one location in the inventory.
    """
    locations = get_bike_locations(id)
    return len(locations) != 0

def is_in_catalog(id: str):
    """
    :param id: a bike id.
    :return: true iff there is a bike with this id in the catalog.
    """
    desc = Database.get(CATALOG)
    return id in desc.keys()

################################################################################################
#                                            SETTERS                                           #
################################################################################################

def add_bike_in_inventory(id: str, location: str) -> None:
    """
    Add that location to the list of locations for the bike of that id.
    :param id: a bike id.
    :param location: an inventory location.
    """
    data = Database.get()
    data[INVENTORY][id].append(location)
    data[INVENTORY][id].sort()
    Database.set(data)

def remove_bike_from_inventory(id: str, location: str) -> None:
    """
    Remove that location to the list of locations for the bike of
    that id, if there is any.
    :param id: a bike id.
    :param location: an inventory location.
    """
    data = Database.get()
    data[INVENTORY][id].remove(location)
    Database.set(data)

def buy_bike(id: str, location: str) -> bool:
    """
    Remove the bike with that id from that location if it's really there.
    :param id: a bike id.
    :param location: a location in the inventory.
    :return: true iff that location exists (and so the transaction went well).
    """
    if location in get_bike_locations(id):
        remove_bike_from_inventory(id, location)
        return True
    return False

def transaction(fields: dict[str, str], date: str) -> bool:

    """
    :param fields: a dictionnary with the details of a transaction.
    :param date: the date of the transaction.
    :return: true iff the transaction went well.
    """

    bike_id = fields['bike_id']
    transaction = {
        "date": date,
        "bike_id": bike_id,
        "email": fields['email'],
        "nom": fields['nom'],
        "adresse": fields['adresse'] + ", " + fields['ville'] + " " + fields['postal']
    }

    db = Database.get()
    db[TRANSACTIONS].append(transaction)
    Database.set(db)

    locations = get_bike_locations(bike_id)
    if len(locations) == 0:
        return False

    location = locations.pop()
    remove_bike_from_inventory(bike_id, location)

    return True
