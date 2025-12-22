import json
import os
import traceback
from player import Player
from loader import GameLoader
from enemy import Enemy

def print_help():
    # Виведення списку доступних команд
    print("\n--- СПИСОК КОМАНД ---")
    print(" go forward / go back : Переміщення по світу")
    print(" take                 : Підібрати предмет у кімнаті")
    print(" inventory (або i)    : Відкрити інвентар детально")
    print(" equip [назва]        : Одягнути зброю або випити зілля")
    print(" attack               : Атакувати ворога (тільки в бою)")
    print(" save                 : Зберегти гру")
    print(" exit                 : Вийти з гри")
    print("---------------------")

def save_game(player):
    # Функція збереження прогресу у файл
    print("...Збереження гри...")
    try:
        data = player.to_dict()
        with open("savegame.json", "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        print("-> [УСПІХ] Гру збережено у 'savegame.json'.")
    except Exception:
        print("-> [ПОМИЛКА] Не вдалося зберегти гру:")
        traceback.print_exc()

def load_game(loader):
    # Функція завантаження збереженої гри
    if not os.path.exists("savegame.json"):
        print("-> Файл збереження не знайдено.")
        return None
    try:
        with open("savegame.json", "r", encoding="utf-8") as f:
            data = json.load(f)
        
        name = data.get("name", "Hero")
        player = Player(name)
        player.load_from_dict(data, loader)
        print("-> Гра успішно завантажена!")
        return player
    except Exception:
        print("-> [ПОМИЛКА] Файл збереження пошкоджено.")
        traceback.print_exc()
        return None

def main():
    # Ініціалізація завантажувача ресурсів
    loader = GameLoader()
    loader.load_data()
    
    print("\n~~~~~~ TEXT RPG ENGINE ~~~~~~")
    
    # Меню вибору: Нова гра або Завантаження
    player = None
    while True:
        print("\n1. Нова гра")
        print("2. Завантажити гру")
        choice = input("Ваш вибір: ").strip()
        
        if choice == "2":
            player = load_game(loader)
            if player: break
        elif choice == "1":
            break
        else:
            print("Будь ласка, введіть 1 або 2.")

    # Створення нового героя, якщо не завантажили збереження
    if not player:
        while True:
            name = input("\nВведіть ім'я героя: ").strip()
            if name:
                player = Player(name)
                break
            print("Ім'я не може бути пустим!")

    is_running = True
    current_enemy = None 
    
    # --- ГОЛОВНИЙ ЦИКЛ ГРИ (GAME LOOP) ---
    while is_running:
        # Отримуємо дані про поточну кімнату
        room = loader.get_room_by_index(player.current_stage_index)
        if not room:
            print("\n*** ВІТАЄМО! ВИ ПРОЙШЛИ ГРУ! ***")
            input("Натисніть Enter для виходу...")
            break

        # Логіка появи ворога в кімнаті
        if room.get("enemy_id") and not current_enemy:
            enemy_data = loader.get_enemy_data(room["enemy_id"])
            if enemy_data:
                current_enemy = Enemy(room["enemy_id"], enemy_data)
                print(f"\n!!! УВАГА !!! З темряви з'являється {current_enemy.name}!")

        # --- БЛОК ВІДОБРАЖЕННЯ (RENDER) ---
        print("\n" + "="*40)
        
        if current_enemy:
            # Інтерфейс під час бою
            print(f"!!! БІЙ !!! Ворог: {current_enemy.name} [HP: {current_enemy.hp}]")
            print(f"Опис ворога: {current_enemy.description}")
        else:
            # Інтерфейс дослідження світу
            print(f"ЛОКАЦІЯ: {room['name']}")
            print(f"ОПИС: {room['description']}")
            
            # Виведення предметів на підлозі
            loot = room.get("loot", [])
            if loot:
                names = []
                for lid in loot:
                    item_obj = loader.create_item(lid)
                    if item_obj: names.append(item_obj.name)
                print(f"\n[ТУТ ЛЕЖИТЬ]: {', '.join(names)}")
            else:
                print("\n[ТУТ ЛЕЖИТЬ]: Нічого")

        # Інформаційна панель гравця (HUD)
        print("-" * 40)
        equip_name = player.equipment['main_hand'].name if player.equipment['main_hand'] else "Нічого"
        inv_names = ", ".join([i.name for i in player.inventory]) if player.inventory else "Пусто"
        
        print(f"ГЕРОЙ: {player.name} | HP: {player.hp}/{player.max_hp}")
        print(f"ЕКІПІРОВАНО: {equip_name}")
        print(f"ІНВЕНТАР: {inv_names}")
        print("-" * 40)
        print("Введіть '?' або 'help' щоб побачити існуючі команди")

        # --- БЛОК ВВЕДЕННЯ (INPUT) ---
        cmd_raw = input(">> ").strip()
        if not cmd_raw: continue
        
        cmd = cmd_raw.lower().split()
        action = cmd[0]

        # --- БЛОК ЛОГІКИ (UPDATE) ---
        
        # Виклик довідки
        if action == "?" or action == "help":
            print_help()
            input("Натисніть Enter щоб продовжити...")
            continue

        # Обробка команд бою
        if current_enemy:
            if action == "attack":
                dmg, w_name, msg = player.attack(current_enemy)
                print(f"\n[АТАКА] Ви вдарили {w_name} і завдали {dmg} урону. {msg}")
                
                # Хід ворога у відповідь
                if current_enemy.is_alive():
                    print(f"[ВОРОГ] {current_enemy.name} атакує вас на {current_enemy.damage} урону!")
                    player.hp -= current_enemy.damage
                    if player.hp <= 0:
                        print("\n*** ВИ ЗАГИНУЛИ ***")
                        is_running = False
                else:
                    print(f"\n[ПЕРЕМОГА] {current_enemy.name} переможений!")
                    room["enemy_id"] = None
                    current_enemy = None
            
            elif action == "use" or action == "equip":
                # Дозволяємо використовувати предмети в бою
                if len(cmd) > 1:
                    item_name = " ".join(cmd[1:])
                    player.equip_item(item_name)
            
            elif action == "run" or action == "go":
                print("Не можна втекти з бою!")
            
            else:
                print("У бою доступні команди: attack, equip [назва], help")
        
        # Обробка мирних команд
        else:
            if action == "go":
                if len(cmd) > 1:
                    if player.move(cmd[1]):
                        print("...перехід...")
                    else:
                        print("Туди не можна йти.")
                else:
                    print("Куди? (go forward / go back)")

            elif action == "take":
                loot = room.get("loot", [])
                if loot:
                    item_id = loot[0]
                    new_item = loader.create_item(item_id)
                    if new_item:
                        player.add_item(new_item)
                        loot.remove(item_id) # Видаляємо предмет з кімнати
                    else:
                        print("Помилка предмета.")
                else:
                    print("Тут нічого брати.")

            elif action == "inventory" or action == "i":
                # Детальний перегляд (хоча короткий вже є в HUD)
                print(f"\nДетальний інвентар:")
                for i in player.inventory:
                    print(f"- {i.name} (Тип: {i.type})")
                input("Натисніть Enter...")

            elif action == "equip":
                if len(cmd) > 1:
                    item_name = " ".join(cmd[1:]) 
                    player.equip_item(item_name)
                else:
                    print("Що екіпірувати? (equip назва)")

            elif action == "save":
                save_game(player)

            elif action == "exit":
                is_running = False
                print("До побачення!")
            
            else:
                print("Невідома команда. Введіть '?' для довідки.")

if __name__ == "__main__":
    main()