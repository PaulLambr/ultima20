import random

totalscore = 50  # Starting cash

# Function to draw 4 random numbers
def draw_numbers():
    return random.sample(range(1, 51), 4)

# Calculate score based on matches
def calculate_score(user_picks, drawn_numbers):
    matches = set(user_picks) & set(drawn_numbers)
    match_count = len(matches)

    # Scoring logic
    if match_count == 1:
        return 1  # 1 dollar for 1 match
    elif match_count == 2:
        return 5  # 5 dollars for 2 matches
    elif match_count == 3:
        return 25  # 25 dollars for 3 matches
    elif match_count == 4:
        return 50  # 50 dollars for 4 matches
    else:
        return 0  # No winnings for no matches

# Validate user input
def get_valid_picks():
    while True:
        try:
            picks = input("\nPick 4 numbers between 1 and 50 (comma-separated): ").split(",")
            picks = list(map(int, picks))  # Convert to integers
            if len(picks) != 4:
                raise ValueError("You must pick exactly 4 numbers.")
            if not all(1 <= num <= 50 for num in picks):
                raise ValueError("All numbers must be between 1 and 50.")
            if len(set(picks)) != len(picks):
                raise ValueError("Duplicate numbers are not allowed.")
            return picks
        except ValueError as e:
            print(f"Invalid input: {e}")

# Main game logic
def play_game():
    global totalscore

    print("Welcome to Keno! Try your luck and see how much cash you can win!")
    print("You start with $100. Each round costs $5 to play.")

    while True:
        # Get user picks
        user_picks = get_valid_picks()

        # Deduct $5 to play
        totalscore -= 5

        # Draw 4 random numbers
        drawn_numbers = draw_numbers()
        print(f"\nThe drawn numbers are: {drawn_numbers}")

        # Calculate score
        score = calculate_score(user_picks, drawn_numbers)
        print(f"\nYour picks: {user_picks}")
        print(f"Matches: {set(user_picks) & set(drawn_numbers)}")
        print(f"Your winnings this round: ${score}")

        # Update total cash
        totalscore += score
        print(f"Your total cash: ${totalscore}")

        # Check if the player is out of money
        if totalscore <= 0:
            print("\nYou're out of cash! Game over!")
            break

        # Ask the user if they want to play again
        play_again = input("\nDo you want to play again? (y/n): ").strip().lower()
        if play_again != "y":
            print(f"\nThanks for playing! You walk away with: ${totalscore}.")
            break

# Play the game
play_game()
