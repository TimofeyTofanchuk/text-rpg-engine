class Player:
    def __init__(self, name):
        # Ініціалізація основних параметрів гравця
        self.name = name
        self.hp = 100
        self.max_hp = 100
        self.inventory = []
        # Словник для збереження екіпірованих предметів
        self.equipment = {
            "main_hand": None, # Основна зброя
            "off_hand": None   # Друга рука (або пусто, якщо зброя дворучна)
        }
        self.current_stage_index = 0 # Поточна позиція у світі (індекс масиву)

    def move(self, direction):
        # Логіка переміщення між кімнатами
        if direction == "forward":
            self.current_stage_index += 1
            return True
        elif direction == "back":
            # Забороняємо виходити за межі стартової кімнати
            if self.current_stage_index > 0:
                self.current_stage_index -= 1
                return True
        return False

    def add_item(self, item):
        # Додавання предмету в інвентар
        self.inventory.append(item)
        print(f"-> [ОТРИМАНО]: {item.name}")

    def equip_item(self, item_name):
        # Пошук предмету в інвентарі за назвою (без урахування регістру)
        item_to_equip = None
        for it in self.inventory:
            if it.name.lower() == item_name.lower():
                item_to_equip = it
                break
        
        if not item_to_equip:
            print(f"Предмет '{item_name}' не знайдено в інвентарі.")
            return

        # Перевірка типу предмету та вільних слотів
        if item_to_equip.type == "weapon":
            slots = item_to_equip.stats.get("slots", 1)
            if slots == 2:
                # Дворучна зброя займає обидва слоти
                self.equipment["main_hand"] = item_to_equip
                self.equipment["off_hand"] = None
                print(f"-> Екіпіровано (Дворучне): {item_to_equip.name}")
            else:
                # Одноручна зброя йде в основну руку
                self.equipment["main_hand"] = item_to_equip
                print(f"-> Екіпіровано (Права рука): {item_to_equip.name}")

        elif item_to_equip.type == "consumable":
            # Якщо це зілля, воно використовується одразу
            self.use_potion(item_to_equip)
        else:
            print("Цей предмет не можна екіпірувати.")

    def use_potion(self, item):
        # Логіка лікування
        val = item.stats.get("effect_value", 0)
        # HP не може перевищувати максимум
        self.hp = min(self.hp + val, self.max_hp)
        self.inventory.remove(item)
        print(f"-> Ви випили {item.name}. HP: {self.hp}/{self.max_hp}")

    def attack(self, target):
        # Розрахунок пошкоджень у бою
        base_dmg = 5
        weapon = self.equipment["main_hand"]
        
        # Визначення характеристик зброї
        if weapon:
            dmg = weapon.stats.get("damage", 0)
            elem = weapon.stats.get("element", "physical")
            w_name = weapon.name
        else:
            dmg = 0
            elem = "physical"
            w_name = "Кулаки"
        
        total = base_dmg + dmg
        
        # Перевірка елементальних бонусів (Камінь-Ножиці-Папір)
        mult = 1.0
        msg = ""
        if elem == "water" and target.element == "fire": 
            mult = 1.5; msg = "(Вода гасить Вогонь!)"
        elif elem == "fire" and target.element == "dark": 
            mult = 1.5; msg = "(Вогонь розсіює Темряву!)"
        elif elem == "dark" and target.element == "water": 
            mult = 1.5; msg = "(Темрява поглинає Воду!)"
        
        final_dmg = int(total * mult)
        target.take_damage(final_dmg)
        
        return final_dmg, w_name, msg

    def to_dict(self):
        # Підготовка даних гравця для збереження у JSON
        inv_ids = [i.id for i in self.inventory]
        # Зберігаємо ID екіпірованої зброї або None
        mh_id = self.equipment["main_hand"].id if self.equipment["main_hand"] else None
        
        return {
            "name": self.name,
            "hp": self.hp,
            "max_hp": self.max_hp,
            "stage": self.current_stage_index,
            "inventory_ids": inv_ids,
            "main_hand_id": mh_id
        }

    def load_from_dict(self, data, loader):
        # Відновлення стану гравця із завантажених даних
        self.hp = data.get("hp", 100)
        self.max_hp = data.get("max_hp", 100)
        self.current_stage_index = data.get("stage", 0)
        
        # Відновлення предметів в інвентарі за їх ID
        self.inventory = []
        for item_id in data.get("inventory_ids", []):
            item = loader.create_item(item_id)
            if item: self.inventory.append(item)
            
        # Відновлення екіпірування
        mh_id = data.get("main_hand_id")
        if mh_id:
            self.equipment["main_hand"] = loader.create_item(mh_id)