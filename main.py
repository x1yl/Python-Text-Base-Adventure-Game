import random


class Item:
    def __init__(self, name: str, description: str, value: int, effect: dict = None):
        self.name = name
        self.description = description
        self.value = value
        self.effect = effect or {}


ITEMS = {
    "health_potion": Item("Health Potion", "Restores 30 HP", 20, {"heal": 30}),
    "strength_potion": Item(
        "Strength Potion", "Temporarily increases attack by 10", 30, {"attack": 10}
    ),
    "shield": Item(
        "Iron Shield", "Increases defense permanently by 5", 50, {"defense": 5}
    ),
    "sword": Item(
        "Steel Sword", "Increases attack permanently by 8", 45, {"attack": 8}
    ),
    "magic_scroll": Item(
        "Magic Scroll", "Deals 25 damage to enemy", 25, {"damage": 25}
    ),
}


class NPC:
    def __init__(self, name: str, description: str, dialog: dict, inventory: dict):
        self.name = name
        self.description = description
        self.dialog = dialog
        self.inventory = inventory


NPCS = {
    "merchant": NPC(
        "Mysterious Merchant",
        "A hooded figure with various magical items",
        {
            "greeting": "Welcome traveler, care to see my wares?",
            "farewell": "Stay safe in these dangerous lands.",
            "no_gold": "Come back when you have more gold!",
        },
        {"health_potion": 5, "strength_potion": 2, "shield": 1},
    ),
    "old_wizard": NPC(
        "Elder Wizard",
        "A wise wizard who knows the secrets of this land",
        {
            "greeting": "Ah, another soul seeking to escape this cursed realm...",
            "quest": "Bring me 3 magic scrolls, and I shall teach you a powerful spell.",
            "complete": "You have done well. Here's your reward!",
            "farewell": "Stay safe in these dangerous lands.",
        },
        {"magic_scroll": 1},
    ),
}


class Player:
    def __init__(self, name: str):
        self.name = name
        self.health = 100
        self.max_health = 100
        self.attack = 15
        self.defense = 10
        self.inventory = {"health_potion": 2, "gold": 0}
        self.location = "a abandoned village"
        self.active_effects = {}  # For temporary buffs

    def use_item(self, item_name: str) -> bool:
        if item_name in self.inventory and self.inventory[item_name] > 0:
            item = ITEMS[item_name]
            if "heal" in item.effect:
                self.health = min(self.max_health, self.health + item.effect["heal"])
                print(f"🧪 Used {item.name}. Health restored to {self.health}")
            if "attack" in item.effect:
                self.attack += item.effect["attack"]
                print(f"💪 Used {item.name}. Attack increased to {self.attack}")
            if "defense" in item.effect:
                self.defense += item.effect["defense"]
                print(f"🛡️ Used {item.name}. Defense increased to {self.defense}")
            self.inventory[item_name] -= 1
            return True
        return False


class Game:
    """Main class containing game logic and state"""

    def __init__(self):
        # game locations and their danger levels
        self.locations = {
            "a abandoned village": {
                "description": "🏚️ An eerie village with empty houses and broken windows.",
                "danger": 0.2,
            },
            "the haunted forest": {
                "description": "🌲 A dark forest filled with ghostly whispers and shadows.",
                "danger": 0.5,
            },
            "forgotten graveyard": {
                "description": "🪦 A graveyard with ancient tombstones and eerie silence.",
                "danger": 0.7,
            },
            "a cursed castle": {
                "description": "🏰 A castle with a dark history and malevolent presence.",
                "danger": 0.9,
            },
        }

        # enemy types and their stats
        self.enemies = {
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

    def trade_with_npc(self, player: Player, npc: NPC) -> None:
        """Handle trading between player and NPC"""
        while True:
            print("\n=== Trading Menu ===")
            print(f"Your gold: {player.inventory.get('gold', 0)}")
            print("\nNPC's Items:")
            for item_name, quantity in npc.inventory.items():
                if quantity > 0:
                    item = ITEMS[item_name]
                    print(f"{item.name}: {item.value} gold (Quantity: {quantity})")

            print("\nYour Items:")
            for item_name, quantity in player.inventory.items():
                if item_name != "gold" and quantity > 0:
                    item = ITEMS.get(item_name)
                    if item:
                        print(
                            f"{item.name}: {item.value//2} gold (Quantity: {quantity})"
                        )

            print("\nOptions:")
            print("1. Buy")
            print("2. Sell")
            print("3. Exit")

            choice = input("What would you like to do? ")

            if choice == "1":
                item_name = input("Enter the item name to buy: ").lower()
                if item_name in npc.inventory and npc.inventory[item_name] > 0:
                    item = ITEMS[item_name]
                    if player.inventory.get("gold", 0) >= item.value:
                        # Process purchase
                        player.inventory["gold"] = (
                            player.inventory.get("gold", 0) - item.value
                        )
                        npc.inventory[item_name] -= 1
                        player.inventory[item_name] = (
                            player.inventory.get(item_name, 0) + 1
                        )
                        print(f"\nBought {item.name} for {item.value} gold!")
                    else:
                        print("\nNot enough gold!")
                else:
                    print("\nItem not available!")

            elif choice == "2":
                item_name = input("Enter the item name to sell: ").lower()
                if item_name in player.inventory and player.inventory[item_name] > 0:
                    item = ITEMS[item_name]
                    # Sell for half the buy price
                    sell_value = item.value // 2
                    player.inventory["gold"] = (
                        player.inventory.get("gold", 0) + sell_value
                    )
                    player.inventory[item_name] -= 1
                    npc.inventory[item_name] = npc.inventory.get(item_name, 0) + 1
                    print(f"\nSold {item.name} for {sell_value} gold!")
                else:
                    print("\nYou don't have this item!")

            elif choice == "3":
                break

    def interact_with_npc(self, player: Player, npc_id: str) -> None:
        npc = NPCS[npc_id]
        print(f"\n{npc.name}: {npc.dialog['greeting']}")

        while True:
            print("\nOptions:")
            print("1. Trade")
            print("2. Talk")
            print("3. Leave")

            choice = input("What would you like to do? ")

            if choice == "1":
                self.trade_with_npc(player, npc)
            elif choice == "2":
                print(f"\n{npc.name} shares some wisdom...")
                if npc_id == "old_wizard":
                    print(npc.dialog["quest"])
            elif choice == "3":
                print(f"\n{npc.name}: {npc.dialog['farewell']}")
                break

    def combat(self, player: Player, enemy: str) -> bool:
        """
        Handle combat between player and enemy
        Returns True if player survives, False if player dies
        """
        enemy_stats = self.enemies[enemy].copy()
        print(f"\n{self.enemies[enemy]['symbol']} A {enemy} appears!")

        while enemy_stats["health"] > 0 and player.health > 0:
            # Display combat status
            print(
                f"\n❤️ Your Health: {player.health} | {enemy}'s Health: {enemy_stats['health']}"
            )
            while True:
                action = input(
                    "What would you like to do? [attack/potion/run]: "
                ).lower()

                # Handle player actions
                if action == "attack":
                    # Calculate damage
                    damage = max(
                        1,
                        player.attack - enemy_stats["defense"] + random.randint(-5, 5),
                    )
                    enemy_stats["health"] -= damage
                    print(f"⚔️ You deal {damage} damage to the {enemy}!")
                    break

                elif action == "potion":
                    player.use_potion()
                    break

                elif action == "run":
                    # 50% chance to escape
                    if random.random() < 0.5:
                        print("🏃 You successfully fled!")
                        return True
                    print("X Couldn't escape!")
                else:
                    print("X Invalid action! Try again.")

            # Enemy attack
            if enemy_stats["health"] > 0:
                damage = max(
                    1, enemy_stats["attack"] - player.defense + random.randint(-3, 3)
                )
                player.health -= damage
                print(f"💥 The {enemy} deals {damage} damage to you!")

        # Dead player
        if player.health <= 0:
            return False

        gold_reward = self.enemies[enemy]["gold"]
        player.inventory["gold"] += gold_reward
        print(f"\n🎉 Victory! You gained {gold_reward} gold!")
        return True

    def main(self):
        """Main handling of player actions and game"""
        print("🎮 Welcome to 'The Escape'!")
        print("You find yourself in a mysterious land filled with danger.")
        print("Your goal is to survive and escape from this place before you die.")
        print(
            f"All you have on you is a map with the following locations: {', '.join(self.locations.keys())}"
        )
        player_name = input("Enter your name: ")
        player = Player(player_name)

        while player.health > 0:
            # Display current status
            print(f"\n📍 Location: {player.location}")
            print(f"❤️ Health: {player.health}/{player.max_health}")
            print(f"🎒 Inventory: {player.inventory}")

            # Show available actions
            print("\nAvailable actions:")
            print("1. 🔍 Explore current area")
            print("2. 🚶 Move to new location")
            print("3. 🧪 Use health potion")
            print("4. 🚪 Quit")
            print("5. 💬 Talk to NPCs")

            choice = input("What would you like to do? ")

            if choice == "1":
                # Random encounter based on danger
                if random.random() < self.locations[player.location]["danger"]:
                    enemy = random.choice(list(self.enemies.keys()))
                    if not self.combat(player, enemy):
                        print("\n💀 Game Over! You have been defeated!")
                        break
                else:
                    # Random gold
                    found_gold = random.randint(1, 10)
                    player.inventory["gold"] += found_gold
                    print(f"💰 You found {found_gold} gold!")

            elif choice == "2":
                # Location change
                print("\nAvailable locations:")
                for location in self.locations:
                    print(f"- {location}")
                while True:
                    new_location = input("Where would you like to go? ").lower()
                    if new_location in self.locations:
                        player.location = new_location
                        print(f"\n🚶 Traveled to {new_location}")
                        print(self.locations[new_location]["description"])
                        break
                    else:
                        print("X Invalid location!")

            elif choice == "3":
                player.use_potion()

            elif choice == "4":
                print("👋 Thanks for playing!")
                break
            elif choice == "5":
                if player.location == "a abandoned village":
                    print("\nAvailable NPCs:")
                    print("1. Mysterious Merchant")
                    print("2. Elder Wizard")
                    npc_choice = input("Who would you like to talk to? ")
                    if npc_choice == "1":
                        self.interact_with_npc(player, "merchant")
                    elif npc_choice == "2":
                        self.interact_with_npc(player, "old_wizard")


if __name__ == "__main__":
    Game().main()
