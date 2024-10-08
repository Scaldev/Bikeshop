table_inventory = {
    "000001": ["100", "101", "102", "103", "104"],
    "000002": ["110", "111", "112"],
    "000003": [],
    "000004": ["250", "251", "252", "253", "254", "255", "256", "257", "258"]
}

table_bikes = {
    "000001": ("Vélo Swag", "Le meilleur au monde", "Blabla blablabla blabla"),
    "000002": ("Vélo Très Bg", "Je suis : amoureux", "Blabla blablabla bla blabla"),
    "000003": ("Vélo Rapide 2000", "mmmmmiouuu ça va vite", "Blabla blablabla bla blabla"),
    "000004": ("Vélo Vraiment Nul", "N'achetez pas ce truc", "Blabla blablabla bla blabla"),
}

def get_models() :
    result = []
    for k in table_inventory:
        result.append([k, table_bikes[k][0], table_bikes[k][1]])
    return result

def get_available_bikes():
    result = []
    for k in table_inventory:
        print(k, table_bikes[k], len(table_bikes[k]))
        if len(table_inventory[k]) != 0:
            result.append([k, table_bikes[k][0], table_bikes[k][1]])
    print(result)
    return result

def get_bike(code):
    if code in table_bikes:
        return table_bikes[code]
    return None

def get_available(code):
    if code in table_inventory:
        return len(table_inventory[code]) != 0
    return None
