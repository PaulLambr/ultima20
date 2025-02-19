import random  # Import random module


def randomNumber():
    return random.randint(1, 50)  # Generate a random number between 1 and 50


def matchNumbers():
    generated_number = randomNumber()  # Get a random number
    attempts = 5

    print("Welcome to the Guessing Game!")
    print("I'm thinking of a number between 1 and 50.")
    print(f"You have {attempts} attempts to guess it.")

    while attempts > 0:
        try:
            your_number = int(input("\nPick a number between 1 and 50: "))

            if your_number == generated_number:
                print(f"\n🎉 You got it! The random number was: {generated_number}")
                break
            elif your_number < generated_number:
                print("\nToo low!")
            else:
                print("\nToo high!")

            attempts -= 1  # Decrease attempts

            if attempts > 0:
                print(f"You have {attempts} attempts remaining.")
            else:
                print(
                    f"\nYou ran out of tries. The correct answer was {generated_number}."
                )
        except ValueError:
            print("Invalid input! Please enter a valid number.")


# Call the function
matchNumbers()

# git add .
# git commit -m "Updated some files"
# git push
# git pull origin main

# player_level = 2

# git branch
# git checkout Potions
# git pull origin Potions

# git fetch origin
# git checkout -b Potions origin/Potions

