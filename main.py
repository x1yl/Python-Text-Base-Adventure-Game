import random
from item import ITEMS
from npc import NPCS, NPC
from player import Player
from enemy import ENEMIES, Enemy


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
            while True:
                # Show available actions
                print("\nAvailable actions:")
                print("1. 🔍 Explore current area")
                print("2. 🚶 Move to new location")
                print("3. 🧪 Use items")
                print("4. 💬 Talk to NPCs")
                print("5. 🚪 Quit")
            
                choice = input("What would you like to do? ")

                if choice == "1":
                    # Random encounter based on danger
                    if random.random() < self.locations[player.location]["danger"]:
                        enemy_name = random.choice(list(ENEMIES.keys()))
                        enemy = Enemy(enemy_name, ENEMIES[enemy_name])
                        if not player.handle_combat(enemy):
                            print("\n💀 Game Over! You have been defeated!")
                            break
                    else:
                        # Random gold
                        found_gold = random.randint(1, 10)
                        player.inventory["gold"] += found_gold
                        print(f"💰 You found {found_gold} gold!")
                        break

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
                    break

                elif choice == "3":
                    if not player.use_item():
                        continue
                    break

                elif choice == "4":
                    if player.location == "a abandoned village":
                        print("\nAvailable NPCs:")
                        print("1. Mysterious Merchant")
                        print("2. Elder Wizard")
                        npc_choice = input("Who would you like to talk to? ")
                        if npc_choice == "1":
                            NPCS["merchant"].interact_with_npc(player)
                        elif npc_choice == "2":
                            NPCS["old_wizard"].interact_with_npc(player)
                    else:
                        print("\nNo NPCs here!")
                    break
                elif choice == "5":
                    print("👋 Thanks for playing!")
                    exit()


if __name__ == "__main__":
    Game().main()
