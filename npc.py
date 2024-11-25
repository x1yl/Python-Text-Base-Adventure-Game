# npc.py
from player import Player
from item import ITEMS, Item
import random


class NPC:
    def __init__(self, name: str, description: str, dialog: dict, inventory: dict):
        self.name = name
        self.description = description
        self.dialog = dialog
        self.inventory = inventory

    def trade_with_npc(self, player: Player) -> None:
        while True:
            self._display_trade_menu(player)
            choice = input("What would you like to do? ")

            if choice == "1":
                self._handle_buy(player)
            elif choice == "2":
                self._handle_sell(player)
            elif choice == "3":
                break

    def interact_with_npc(self, player: Player) -> None:
        print(f"\n{self.name}: {self.dialog['greeting']}")
        while True:
            print("\nOptions:\n1. Trade\n2. Talk\n3. Leave")
            choice = input("What would you like to do? ")

            if choice == "1":
                self.trade_with_npc(player)
            elif choice == "2":
                print(f"\n{self.name} shares some wisdom...")
                if self.name == "Elder Wizard":
                    if player.quest_items["magic_scroll"] >= 3:
                        print(self.dialog["complete"])
                        player.quest_items["magic_scroll"] -= 3

                        # Random reward selection
                        reward_type = random.choice(["effect", "item"])
                        if reward_type == "effect":
                            effect_type = random.choice(
                                [
                                    ("attack", 15, "🗡️ Attack"),
                                    ("defense", 10, "🛡️ Defense"),
                                    ("max_health", 25, "❤️ Max Health"),
                                ]
                            )
                            if effect_type[0] == "attack":
                                player.attack += effect_type[1]
                            elif effect_type[0] == "defense":
                                player.defense += effect_type[1]
                            elif (
                                effect_type[0] == "max_health"
                                and player.health == player.max_health
                            ):
                                player.health += effect_type[1]
                            if effect_type[0] == "max_health":
                                player.max_health += effect_type[1]

                            print(
                                f"🌟 You learned a powerful spell! {effect_type[2]} increased by {effect_type[1]}!"
                            )
                        else:
                            reward_item = random.choice(
                                [
                                    ("sword", "Steel Sword"),
                                    ("shield", "Iron Shield"),
                                    ("strength_potion", "Strength Potion"),
                                    ("health_potion", "Health Potion"),
                                ]
                            )
                            player.inventory[reward_item[0]] = (
                                player.inventory.get(reward_item[0], 0) + 2
                            )
                            print(
                                f"🎁 The wizard rewards you with two {reward_item[1]}s!"
                            )
                    else:
                        print(f"{self.dialog['quest']}")
                        print(
                            f"Current progress: {player.quest_items['magic_scroll']}/3 Magic Scrolls"
                        )
            elif choice == "3":
                print(f"\n{self.name}: {self.dialog['farewell']}")
                break

    def _display_trade_menu(self, player: Player) -> None:
        print(f"\n=== Trading Menu ===\nYour gold: {player.inventory.get('gold', 0)}")
        self._display_npc_items()
        self._display_player_items(player)
        print("\nOptions:\n1. Buy\n2. Sell\n3. Exit")

    def _display_npc_items(self) -> None:
        print("\nNPC's Items:")
        for item_name, quantity in self.inventory.items():
            if quantity > 0:
                item = ITEMS[item_name]
                print(f"{item_name}: {item.value} gold (Quantity: {quantity})")

    def _display_player_items(self, player: Player) -> None:
        print("\nYour Items:")
        for item_name, quantity in player.inventory.items():
            if item_name != "gold" and quantity > 0:
                item = ITEMS.get(item_name)
                if item:
                    print(f"{item.name}: {item.value//2} gold (Quantity: {quantity})")

    def _handle_buy(self, player: Player) -> None:
        item_name = input("Enter the item name to buy: ").lower()
        if item_name in self.inventory and self.inventory[item_name] > 0:
            item = ITEMS[item_name]
            if player.inventory.get("gold", 0) >= item.value:
                self._complete_purchase(player, item_name, item)
            else:
                print("\nNot enough gold!")
        else:
            print("\nItem not available!")

    def _handle_sell(self, player: Player) -> None:
        item_input = input("Enter the item name to sell: ").lower()
        # Convert input to internal item name format
        item_name = "_".join(item_input.split())
        if item_name in player.inventory and player.inventory[item_name] > 0:
            item = ITEMS[item_name]
            self._complete_sale(player, item_name, item)
        else:
            print("\nYou don't have this item!")

    def _complete_purchase(self, player: Player, item_name: str, item: Item) -> None:
        player.inventory["gold"] -= item.value
        self.inventory[item_name] -= 1
        player.inventory[item_name] = player.inventory.get(item_name, 0) + 1
        print(f"\nBought {item.name} for {item.value} gold!")

    def _complete_sale(self, player: Player, item_name: str, item: Item) -> None:
        sell_value = item.value // 2
        player.inventory["gold"] += sell_value
        player.inventory[item_name] -= 1
        self.inventory[item_name] = self.inventory.get(item_name, 0) + 1
        print(f"\nSold {item.name} for {sell_value} gold!")


# NPCs data
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
