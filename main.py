from player import Player
from loader import GameLoader

def main():
    print("=== ЗАВАНТАЖЕННЯ РУШІЯ ===")
    loader = GameLoader()
    loader.load_data()
    
    player_name = input("\nВведіть ім'я героя: ")
    player = Player(player_name)
    
    is_running = True
    print(f"\nвітаємо, {player.name}! Гра почалася.")

    #GAME LOOP
    while is_running:
        #1.RENDER
        current_room = loader.get_room_by_index(player.current_stage_index)
        
        if not current_room:
            print("Ви пройшли гру або вийшли за межі світу!")
            break

        print(f"\n[Локація {player.current_stage_index}]: {current_room['name']}")
        print(f"Опис: {current_room['description']}")
        print(f"HP: {player.hp}/{player.max_hp}")

        #2.INPUT
        command = input("\n>> ").strip().lower().split()
        if not command:
            continue
        
        action = command[0]

        #3.UPDATE
        if action == "exit":
            is_running = False
            print("Гра збережена (імітація). До побачення!")
            
        elif action == "inventory" or action == "i":
            player.show_inventory()

        elif action == "go":
            if len(command) > 1:
                direction = command[1] #forward або back
                if player.move(direction):
                    print("Ви перейшли до наступної локації.")
                else:
                    print("Туди не можна йти.")
            else:
                print("Куди йти? (go forward / go back)")

        elif action == "take":
            #Тимчасова логіка для тесту
            #Беремо перший предмет зі списку луту кімнатиs
            loot_list = current_room.get("loot", [])
            if loot_list:
                item_id = loot_list[0]
                new_item = loader.create_item(item_id)
                if new_item:
                    player.add_item(new_item)
                else:
                    print("Помилка створення предмету.")
            else:
                print("Тут нічого брати.")
        
        else:
            print("Невідома команда. Доступні: go [forward/back], take, inventory, exit")

if __name__ == "__main__":
    main()