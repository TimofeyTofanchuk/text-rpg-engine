import pytest
from player import Player
from item import Item
from enemy import Enemy
from loader import GameLoader

@pytest.fixture
def test_player():
    return Player("TestHero")

@pytest.fixture
def fire_sword():
    #Створюємо тестовий меч (Вогонь)
    data = {
        "name": "Fire Sword",
        "type": "weapon",
        "damage": 20,
        "element": "fire",
        "slots": 1
    }
    return Item("fire_sword_id", data)

@pytest.fixture
def dark_enemy():
    #Створюємо тестового ворога (Темрява)
    data = {
        "name": "Shadow",
        "hp": 100,
        "damage": 10,
        "element": "dark"
    }
    return Enemy("shadow_id", data)

#~~~~ ТЕСТИ ~~~~

def test_player_initialization(test_player):
    """Перевірка початкового стану гравця"""
    assert test_player.name == "TestHero"
    assert test_player.hp == 100
    assert test_player.current_stage_index == 0
    assert test_player.inventory == []

def test_movement(test_player):
    """Перевірка навігації та обмежень"""
    #Спроба піти назад зі старту (має бути False)
    assert test_player.move("back") is False
    assert test_player.current_stage_index == 0
    
    #Рух вперед
    assert test_player.move("forward") is True
    assert test_player.current_stage_index == 1

def test_inventory_and_equip(test_player, fire_sword):
    """Перевірка додавання та екіпірування предмету"""
    test_player.add_item(fire_sword)
    assert len(test_player.inventory) == 1
    
    #Екіпірування
    test_player.equip_item("Fire Sword")
    assert test_player.equipment["main_hand"] is not None
    assert test_player.equipment["main_hand"].name == "Fire Sword"

def test_combat_mechanics(test_player, fire_sword, dark_enemy):
    """Перевірка розрахунку урону та елементальних бонусів"""
    test_player.add_item(fire_sword)
    test_player.equip_item("Fire Sword")
    
    #База (5) + Меч (20) = 25.
    #Вогонь б'є Темряву -> Множник 1.5
    #Очікуваний урон: 25 * 1.5 = 37 (int)
    
    damage, weapon_name, msg = test_player.attack(dark_enemy)
    
    assert damage == 37
    assert "Вогонь розсіює Темряву" in msg
    assert dark_enemy.hp == 63  # 100 - 37

def test_save_load_logic(test_player, fire_sword):
    #Перевірка серіалізації даних
    test_player.current_stage_index = 5
    test_player.add_item(fire_sword)
    test_player.hp = 50
    
    #Перетворюємо в словник (імітація збереження)
    saved_data = test_player.to_dict()
    
    assert saved_data["name"] == "TestHero"
    assert saved_data["hp"] == 50
    assert saved_data["stage"] == 5
    assert "fire_sword_id" in saved_data["inventory_ids"]