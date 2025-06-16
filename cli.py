import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


from colorama import init, Fore, Style
init(autoreset=True)

from utils.ascii_art import show


from services import (
    player_service, monster_service, battle_engine
)
from model import session

current = None

def login():
    global current
    show("logo")
    uname = input("Username: ").strip()
    current = player_service.get_or_create(uname)

def menu():
    while True:
        print(f"\n{Fore.YELLOW}=== Main Menu (Lv.{current.level}) ==={Style.RESET_ALL}")
        print("1. Catch a Monster")
        print("2. View Collection")
        print("3. Heal All Monsters")
        print("4. Battle a Wild Monster")
        print("5. Exit")
        choice = input("> ")
        if choice == "1":
            monster_service.catch(current)
        elif choice == "2":
            col = monster_service.collection(current)
            if not col:
                print("No monsters yet.")
            else:
                for i,m in enumerate(col,1):
                    print(f"{i}. {m.species.name} Lv.{m.level} HP:{m.current_hp}")
        elif choice == "3":
            monster_service.heal_all(current)
        elif choice == "4":
            if not current.monsters:
                print("Catch a monster first!")
            else:
                battle_engine.wild_battle(current)
        elif choice == "5":
            print("Goodbye!"); break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    login()
    menu()
