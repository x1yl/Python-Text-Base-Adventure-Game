# item.py
class Item:
    def __init__(self, name: str, description: str, value: int, effect: dict = None):
        self.name = name
        self.description = description
        self.value = value
        self.effect = effect or {}

    def use(self, target) -> bool:
        """Apply item effects to target"""
        if "heal" in self.effect:
            target.health = min(target.max_health, target.health + self.effect["heal"])
            print(f"🧪 Used {self.name}. Health restored to {target.health}")
        if "attack" in self.effect:
            target.attack += self.effect["attack"]
            print(f"💪 Used {self.name}. Attack increased to {target.attack}")
        if "defense" in self.effect:
            target.defense += self.effect["defense"]
            print(f"🛡️ Used {self.name}. Defense increased to {target.defense}")
        return True


# Game items
ITEMS = {
    "health_potion": Item(
        "Health Potion",
        "Restores 30 HP",
        20,
        {"heal": 30},
    ),
    "strength_potion": Item(
        "Strength Potion",
        "Increases attack by 10",
        30,
        {"attack": 10},
    ),
    "shield": Item(
        "Iron Shield",
        "Increases defense by 5",
        50,
        {"defense": 5},
    ),
    "sword": Item(
        "Steel Sword",
        "Increases attack by 8",
        45,
        {"attack": 8},
    ),
    "magic_scroll": Item(
        "Magic Scroll",
        "Deals 25 damage",
        25,
        {"damage": 25},
    ),
}
