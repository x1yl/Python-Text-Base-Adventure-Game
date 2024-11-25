# enemy.py
import random


class Enemy:
    def __init__(self, name: str, stats: dict):
        self.name = name
        self.health = stats["health"]
        self.attack = stats["attack"]
        self.defense = stats["defense"]
        self.gold = stats["gold"]
        self.symbol = stats["symbol"]

    def attack_player(self, player) -> int:
        damage = max(1, self.attack - player.defense + random.randint(-3, 3))
        player.health -= damage
        print(f"💥 The {self.name} deals {damage} damage to you!")
        return damage


ENEMIES = {
    "Ghost": {
        "health": 25,
        "attack": 10,
        "defense": 5,
        "gold": 15,
        "symbol": "👻",
    },
    "Zombie": {
        "health": 35,
        "attack": 12,
        "defense": 8,
        "gold": 20,
        "symbol": "🧟",
    },
    "Vampire": {
        "health": 50,
        "attack": 18,
        "defense": 12,
        "gold": 30,
        "symbol": "🧛",
    },
    "Werewolf": {
        "health": 70,
        "attack": 25,
        "defense": 15,
        "gold": 50,
        "symbol": "🐺",
    },
    "Wraith": {
        "health": 40,
        "attack": 20,
        "defense": 10,
        "gold": 25,
        "symbol": "👹",
    },
    "Banshee": {
        "health": 30,
        "attack": 15,
        "defense": 8,
        "gold": 20,
        "symbol": "👻",
    },
    "Lich": {
        "health": 60,
        "attack": 22,
        "defense": 18,
        "gold": 40,
        "symbol": "💀",
    },
    "Demon": {
        "health": 80,
        "attack": 30,
        "defense": 20,
        "gold": 60,
        "symbol": "👿",
    },
}
