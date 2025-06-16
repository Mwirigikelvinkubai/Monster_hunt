
from model import MonsterSpecies, session
import json

monsters = [
    {
        "name": "Zivra",
        "type": "Air",
        "base_stats": {
            "base_hp": 35, "base_attack": 80, "base_defense": 25,
            "scaling": {"hp": 2, "attack": 6, "defense": 1}
        },
        "rarity": 0.10,
        "abilities": [
            {"name": "Zephyr Strike", "type": "Air", "power": 100, "effect": "speed_up"},
            {"name": "Whisper Cloak", "type": "Air", "power": 0, "effect": "evade"}
        ]
    },
    {
        "name": "Terrosu",
        "type": "Earth",
        "base_stats": {
            "base_hp": 90, "base_attack": 30, "base_defense": 95,
            "scaling": {"hp": 6, "attack": 2, "defense": 5}
        },
        "rarity": 0.35,
        "abilities": [
            {"name": "Soil Armor", "type": "Earth", "power": 0, "effect": "defense_up"},
            {"name": "Pebble Shot", "type": "Earth", "power": 25}
        ]
    },
    {
        "name": "Kawa",
        "type": "Water",
        "base_stats": {
            "base_hp": 60, "base_attack": 45, "base_defense": 40,
            "scaling": {"hp": 5, "attack": 3, "defense": 3}
        },
        "rarity": 0.25,
        "abilities": [
            {"name": "Wave Dance", "type": "Water", "power": 40},
            {"name": "Tide Pull", "type": "Water", "power": 0, "effect": "disable"}
        ]
    },
    {
        "name": "Ignis Pup",
        "type": "Fire",
        "base_stats": {
            "base_hp": 40, "base_attack": 55, "base_defense": 35,
            "scaling": {"hp": 4, "attack": 4, "defense": 2}
        },
        "rarity": 0.40,
        "abilities": [
            {"name": "Bark Burn", "type": "Fire", "power": 45},
            {"name": "Ember Sniff", "type": "Fire", "power": 0, "effect": "reveal_enemy"}
        ]
    },
    {
        "name": "Umbloom",
        "type": "Earth",
        "base_stats": {
            "base_hp": 55, "base_attack": 45, "base_defense": 55,
            "scaling": {"hp": 5, "attack": 3, "defense": 4}
        },
        "rarity": 0.20,
        "abilities": [
            {"name": "Spore Cloud", "type": "Earth", "power": 0, "effect": "sleep"},
            {"name": "Petal Slash", "type": "Earth", "power": 50}
        ]
    }
]

# Insert into DB
for m in monsters:
    monster = MonsterSpecies(
        name=m["name"],
        type=m["type"],
        base_stats=json.dumps(m["base_stats"]),
        rarity=m["rarity"],
        abilities=json.dumps(m["abilities"])
    )
    session.add(monster)

session.commit()
print("✅ MonsterSpecies table seeded with 5 human‑flavoured monsters.")
for m in monsters:
    if session.query(MonsterSpecies).filter_by(name=m["name"]).first():
        continue  # Skip if monster already exists
    monster = MonsterSpecies(
        name=m["name"],
        type=m["type"],
        base_stats=json.dumps(m["base_stats"]),
        rarity=m["rarity"],
        abilities=json.dumps(m["abilities"])
    )
    session.add(monster)

