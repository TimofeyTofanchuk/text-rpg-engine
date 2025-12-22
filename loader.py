import json
import copy
from item import Item
#Імпорт класу Enemy додамо пізніше, поки що використовуємо словник або placeholder
#Але для чистоти коду, давай припустимо, що клас Enemy у нас буде (створимо його в наступному кроці)

class GameLoader:
    def __init__(self):
        self.items_data = {}
        self.enemies_data = {}
        self.world_data = []

    def load_data(self):
        #1 Завантаження предметів
        try:
            with open("data/items.json", "r", encoding="utf-8") as f:
                raw_items = json.load(f)
                for key, val in raw_items.items():
                    self.items_data[key] = Item(key, val)
            print("-> Предмети завантажено.")
        except FileNotFoundError:
            print("ПОМИЛКА: Не знайдено data/items.json")

        #2 Завантаження ворогів (НОВЕ)
        try:
            with open("data/enemies.json", "r", encoding="utf-8") as f:
                self.enemies_data = json.load(f)
            print("-> Вороги завантажено.")
        except FileNotFoundError:
            print("ПОМИЛКА: Не знайдено data/enemies.json")

        #3 Завантаження світу
        try:
            with open("data/world.json", "r", encoding="utf-8") as f:
                self.world_data = json.load(f)
            print("-> Світ завантажено.")
        except FileNotFoundError:
            print("ПОМИЛКА: Не знайдено data/world.json")

    def get_room_by_index(self, index):
        if 0 <= index < len(self.world_data):
            return self.world_data[index]
        return None

    def create_item(self, item_id):
        if item_id in self.items_data:
            return copy.deepcopy(self.items_data[item_id])
        return None

    def get_enemy_data(self, enemy_id):
        #Повертає словник даних для створення ворога
        if enemy_id in self.enemies_data:
            return copy.deepcopy(self.enemies_data[enemy_id])
        return None