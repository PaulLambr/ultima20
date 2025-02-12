class Character:
    def __init__(self, name, health, attack_power):
        self.name = name
        self.health = health
        self.attack_power = attack_power

    def attack(self, target):
        print(f"{self.name} attacks {target.name} for {self.attack_power} damage!")
        target.health -= self.attack_power
        if target.health <= 0:
            print(f"{target.name} has been defeated!")

# Create player and enemy objects
player = Character("Hero", 20, 5)
goblin = Character("Goblin", 10, 3)

# Simulate an attack
player.attack(goblin)
