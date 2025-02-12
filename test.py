import random

# Create a full deck of 52 cards
suits = ["Hearts", "Diamonds", "Clubs", "Spades"]
values = [2, 3, 4, 5, 6, 7, 8, 9, 10, "J", "Q", "K", "A"]
deck = [(value, suit) for value in values for suit in suits]

# Function to generate a card
def generate_card(deck):
    card = random.choice(deck)  # Pick a random card
    deck.remove(card)           # Remove the chosen card from the deck
    return card

# Function to calculate card value
def card_value(card):
    return values.index(card[0]) + 2  # Index + 2 matches numeric values

# Initialize variables
player1_score = 0
player2_score = 0
player1_prisoner = None
player2_prisoner = None

# Main game loop
while len(deck) >= 2:  # Ensure there are enough cards for a round
    # Players draw their cards
    player1_card = generate_card(deck)
    player2_card = generate_card(deck)

    # Display cards
    print(f"\nPlayer 1's Card: {player1_card[0]} of {player1_card[1]}")
    print(f"Player 2's Card: {player2_card[0]} of {player2_card[1]}")

    # Compare card values
    player1_value = card_value(player1_card)
    player2_value = card_value(player2_card)

    if player1_value > player2_value:
        print("Player 1 wins this round!")
        player1_score += 2
    elif player1_value < player2_value:
        print("Player 2 wins this round!")
        player2_score += 2
    else:
        print("War!")
        if len(deck) < 8:  # Not enough cards for war
            print("Not enough cards left for war! Game over.")
            break

        # Each player draws three cards face down and one face up
        player1_war_cards = [generate_card(deck) for _ in range(3)]
        player2_war_cards = [generate_card(deck) for _ in range(3)]
        player1_war_card = generate_card(deck)
        player2_war_card = generate_card(deck)

        print(f"Player 1's War Card: {player1_war_card[0]} of {player1_war_card[1]}")
        print(f"Player 2's War Card: {player2_war_card[0]} of {player2_war_card[1]}")

        # Allow prisoners to be used
        if player1_prisoner and card_value(player1_prisoner) > card_value(player1_war_card):
            use_prisoner = input("Player 1, use your prisoner? (y/n): ").lower() == "y"
            if use_prisoner:
                print(f"Player 1 uses their prisoner: {player1_prisoner[0]} of {player1_prisoner[1]}")
                player1_war_card = player1_prisoner
                player1_prisoner = None

        if player2_prisoner and card_value(player2_prisoner) > card_value(player2_war_card):
            use_prisoner = input("Player 2, use your prisoner? (y/n): ").lower() == "y"
            if use_prisoner:
                print(f"Player 2 uses their prisoner: {player2_prisoner[0]} of {player2_prisoner[1]}")
                player2_war_card = player2_prisoner
                player2_prisoner = None

        # Compare the war cards
        if card_value(player1_war_card) > card_value(player2_war_card):
            print("Player 1 wins the war!")
            player1_score += 8
            # Take a random card as a prisoner
            all_war_cards = player1_war_cards + [player1_war_card] + player2_war_cards + [player2_war_card]
            player1_prisoner = random.choice(all_war_cards)
        elif card_value(player1_war_card) < card_value(player2_war_card):
            print("Player 2 wins the war!")
            player2_score += 8
            # Take a random card as a prisoner
            all_war_cards = player1_war_cards + [player1_war_card] + player2_war_cards + [player2_war_card]
            player2_prisoner = random.choice(all_war_cards)
        else:
            print("Another tie during war! Cards are discarded.")

# Display final results
print("\nFinal Scores:")
print(f"Player 1: {player1_score} cards")
print(f"Player 2: {player2_score} cards")

if player1_score > player2_score:
    print("Player 1 wins the game!")
elif player1_score < player2_score:
    print("Player 2 wins the game!")
else:
    print("It's a tie!")
