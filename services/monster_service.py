import random, json
from model import session, MonsterSpecies, PlayerMonster
from colorama import Fore, Style
from .player_service import add_exp
from .achievement_service import check_all

def _rate(species, level):           # simple catch formula
    return min(species.rarity + level * 0.01, 0.95)

def catch(player):
    species = random.choice(session.query(MonsterSpecies).all())
    chance  = _rate(species, player.level)
    print(f"{Fore.CYAN}A wild {species.name} appeared! Catch chance {chance*100:.1f}%{Style.RESET_ALL}")
    if random.random() < chance:
        hp = json.loads(species.base_stats)["base_hp"]
        pm = PlayerMonster(player_id=player.id, species_id=species.id,
                           level=1, current_hp=hp)
        session.add(pm); session.commit()
        print(Fore.GREEN + "✅ You caught it!" + Style.RESET_ALL)
        add_exp(player, 5)
        check_all(player)            # achievements
    else:
        print(Fore.RED + "❌ It escaped!" + Style.RESET_ALL)

def collection(player):
    return session.query(PlayerMonster).filter_by(player_id=player.id).all()

def heal_all(player):
    for m in player.monsters:
        m.current_hp = json.loads(m.species.base_stats)["base_hp"]
    session.commit()
    print(Fore.GREEN + "💚 All monsters healed." + Style.RESET_ALL)

def level_up(pm, amount=1):
    pm.level += amount
    # evolution check
    evo_to = pm.species.evolves_to
    if evo_to and pm.level >= 10:     # simple rule
        new_species = session.query(MonsterSpecies).filter_by(name=evo_to).first()
        if new_species:
            pm.species = new_species
            print(Fore.MAGENTA + f"🔄 {evo_to} evolution achieved!" + Style.RESET_ALL)
    session.commit()
