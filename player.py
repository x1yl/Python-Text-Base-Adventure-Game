# player.py
from item import ITEMS
import random


class Player:
    def __init__(self, name: str):
        self.name = name
        self.health = 100
        self.max_health = 100
        self.attack = 15
        self.defense = 10
        self.inventory = {"health_potion": 2, "gold": 0}
        self.location = "a abandoned village"
        self.active_effects = {}
        self.quest_items = {"magic_scroll": 0}

    def use_item(self) -> bool:
        self.display_inventory()
        item_name = input("Enter item name (or 'back'): ").lower()

        if item_name == "back":
            return False

        if item_name in self.inventory and self.inventory[item_name] > 0:
            item = ITEMS[item_name]
            if item.use(self):
                self.inventory[item_name] -= 1
                return True

        print("You don't have that item!")
        return False

    def display_inventory(self) -> None:
        print("\nYour inventory:")
        for item_name, quantity in self.inventory.items():
            if item_name != "gold":
                item = ITEMS.get(item_name)
                if item:
                    print(f"{item_name}: {quantity}")

    def attack_enemy(self, enemy) -> int:
        damage = max(1, self.attack - enemy.defense + random.randint(-5, 5))
        enemy.health -= damage
        print(f"⚔️ You deal {damage} damage to the {enemy.name}!")
        return damage

    def handle_combat(self, enemy) -> bool:
        print(f"\n{enemy.symbol} A {enemy.name} appears!")

        while enemy.health > 0 and self.health > 0:
            print(
                f"\n❤️ Your Health: {self.health} | {enemy.name}'s Health: {enemy.health}"
            )

            while True:
                action = input("What would you like to do? [attack/item/run]: ").lower()

                if action == "attack":
                    self.attack_enemy(enemy)
                    break
                elif action == "item":
                    if not self.use_item():
                        continue
                    break
                elif action == "run":
                    if random.random() < 0.5:
                        print("🏃 You successfully fled!")
                        return True
                    print("X Couldn't escape!")
                    break
                else:
                    print("X Invalid action! Try again.")

            if enemy.health > 0:
                enemy.attack_player(self)

        if self.health <= 0:
            return False

        self.inventory["gold"] += enemy.gold
        print(f"\n🎉 Victory! You gained {enemy.gold} gold!")
        return True
