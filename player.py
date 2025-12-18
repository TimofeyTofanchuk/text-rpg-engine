class Player:
    def __init__(self, name):
        self.name = name
        self.hp = 100
        self.max_hp = 100
        self.inventory = []  #список об'єктів Item
        self.current_stage_index = 0  #де гравець зараз

    def move(self, direction):
        if direction == "forward":
            self.current_stage_index += 1
            return True
        elif direction == "back":
            if self.current_stage_index > 0:
                self.current_stage_index -= 1
                return True
        return False

    def add_item(self, item):
        self.inventory.append(item)
        print(f"Ви підібрали: {item.name}")

    def show_inventory(self):
        print("\n--- ІНВЕНТАР ---")
        if not self.inventory:
            print("Порожньо.")
        else:
            for item in self.inventory:
                print(f"- {item.name} ({item.type})")
        print("----------------")