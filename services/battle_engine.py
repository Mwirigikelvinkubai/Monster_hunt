import random, json
from colorama import Fore, Style
from model import session, Battle, PlayerMonster, MonsterSpecies
from utils.type_chart import multiplier
from .player_service import add_exp, record_win
from .achievement_service import check_all

def _damage(att_pm, def_pm):
    a = json.loads(att_pm.species.base_stats)
    d = json.loads(def_pm.species.base_stats)
    base = max(1, a["base_attack"] - d["base_defense"]//3)
    mult = multiplier(att_pm.species.type, def_pm.species.type)
    return int(base * mult)

def wild_battle(player):
    # pick your first monster vs random species clone
    your_pm = player.monsters[0]
    wild_sp = random.choice(session.query(MonsterSpecies).all())
    wild_pm = PlayerMonster(level=1, current_hp=json.loads(wild_sp.base_stats)["base_hp"],
                            species=wild_sp)

    print(Fore.YELLOW + f"⚔️  {your_pm.species.name} VS {wild_sp.name}" + Style.RESET_ALL)
    log = []
    turn = 1
    while your_pm.current_hp > 0 and wild_pm.current_hp > 0:
        dmg = _damage(your_pm, wild_pm)
        wild_pm.current_hp -= dmg
        log.append(f"T{turn}: you hit {dmg}")
        if wild_pm.current_hp <= 0: break
        dmg2 = _damage(wild_pm, your_pm)
        your_pm.current_hp -= dmg2
        log.append(f"T{turn}: wild hits {dmg2}")
        turn += 1
    win = wild_pm.current_hp <= 0
    session.add(Battle(player1_id=player.id, winner_id=player.id if win else None,
                       battle_log=" | ".join(log)))
    session.commit()

    if win:
        print(Fore.GREEN + "🏆 You won!" + Style.RESET_ALL)
        add_exp(player, 10); record_win(player)
    else:
        print(Fore.RED + "😵 You lost…" + Style.RESET_ALL)
    check_all(player)
