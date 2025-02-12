import random

def temple_escape():
    print("\nYou find a pouch on an altar. It looks valuable.")
    attempts = 3  # Player gets three tries

    while attempts > 0:
        response = input("Do you take the pouch? (yes/no): ").strip().lower()

        if response == "yes":
            fate = random.choice(["safe", "boulder", "trap"])
            
            if fate == "safe":
                print("You escape with the pouch! Congratulations.")
                return True
            elif fate == "boulder":
                print("A massive boulder chases you! Run!")
                attempts -= 1
            else:
                print("A hidden trapdoor opens beneath you! You fall into darkness...")
                return False  # Immediate game over
        
        else:
            print("The temple rumbles... but nothing happens. Maybe you should reconsider.")
            attempts -= 1

    print("The walls collapse, sealing you inside forever. Game over.")
    return False

# Run the game once and check the result
result = temple_escape()

if result:
    print("\nYou loser.")
else:
    print("\nYour butt smells bad.")
