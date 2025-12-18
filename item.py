class Item:
    def __init__(self, id_name, data):
        self.id = id_name
        self.name = data.get("name", "Unknown")
        self.type = data.get("type", "misc")
        self.stats = data  #всі інші параметри (damage, slots)
    
    def __str__(self):
        return f"[{self.name}]"