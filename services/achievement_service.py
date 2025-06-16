from model import session, Achievement, PlayerAchievement
from colorama import Fore, Style

ACHIEVEMENTS = [
    ("Collector",   "Catch 5 monsters"),
    ("Warrior",     "Win 3 battles"),
]

def _ensure_defs():
    for name, desc in ACHIEVEMENTS:
        if not session.query(Achievement).filter_by(name=name).first():
            session.add(Achievement(name=name, description=desc))
    session.commit()

def check_all(player):
    _ensure_defs()
    # Collector
    if len(player.monsters) >= 5:
        _grant(player, "Collector")
    # Warrior
    if player.wins >= 3:
        _grant(player, "Warrior")

def _grant(player, ach_name):
    ach = session.query(Achievement).filter_by(name=ach_name).first()
    owned = session.query(PlayerAchievement).filter_by(
        player_id=player.id, achievement_id=ach.id).first()
    if not owned:
        session.add(PlayerAchievement(player_id=player.id,
                                      achievement_id=ach.id))
        session.commit()
        print(Fore.CYAN + f"🏅 Achievement unlocked: {ach_name}" + Style.RESET_ALL)
