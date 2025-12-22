class Enemy:
    def __init__(self, id_name, data):
        self.id = id_name
        self.name = data.get("name", "Невідомий ворог")
        self.hp = data.get("hp", 10)
        self.max_hp = data.get("hp", 10)
        self.damage = data.get("damage", 2)
        self.element = data.get("element", "physical")
        self.description = data.get("description", "")

    def is_alive(self):
        return self.hp > 0

    def take_damage(self, amount):
        self.hp -= amount
        if self.hp < 0:
            self.hp = 0