import json
import os
from item import Item

class GameLoader:
    def __init__(self):
        self.items_data = {}
        self.world_data = []

    def load_data(self):
        #завантаження предметів
        try:
            with open("data/items.json", "r", encoding="utf-8") as f:
                raw_items = json.load(f)
                #перетворення словника JSON на об'єкти
                for key, val in raw_items.items():
                    self.items_data[key] = Item(key, val)
            print("-> Предмети завантажено.")
        except FileNotFoundError:
            print("Помилка: Не знайдено data/items.json")

        #завантаження світу
        try:
            with open("data/world.json", "r", encoding="utf-8") as f:
                self.world_data = json.load(f)
            print("-> Світ завантажено.")
        except FileNotFoundError:
            print("Помилка: Не знайдено data/world.json")

    def get_room_by_index(self, index):
        if 0 <= index < len(self.world_data):
            return self.world_data[index]
        return None

    def create_item(self, item_id):
        #повертає копію предмета щоб не змінювати оригінал
        if item_id in self.items_data:
            import copy
            return copy.deepcopy(self.items_data[item_id])
        return None