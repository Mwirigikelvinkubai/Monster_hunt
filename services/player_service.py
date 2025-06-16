from model import session, Player
from colorama import Fore, Style

LVL_EXP = 20

def get_or_create(username):
    p = session.query(Player).filter_by(username=username).first()
    if not p:
        p = Player(username=username)
        session.add(p); session.commit()
        print(Fore.GREEN + f"New player '{username}' created." + Style.RESET_ALL)
    return p

def add_exp(player, amount):
    player.exp += amount
    leveled_up = False
    while player.exp >= LVL_EXP:
        player.exp -= LVL_EXP
        player.level += 1
        leveled_up = True
    if leveled_up:
        print(Fore.YELLOW + f"⭐ {player.username} reached Lv.{player.level}!" + Style.RESET_ALL)
    session.commit()

def record_win(player):
    player.wins += 1
    session.commit()
