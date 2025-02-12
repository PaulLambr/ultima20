import random
import sys

inventory = []
areinvisible = False
turns = 5
arefree = False
hasbeensaidonce = False
hobbithealth = 25
playerhealth = 20  # Player now has health too

print("\nYou are in a hole in the ground, filled with the ends of worms and an oozy smell. An evil hobbit holds you captive."
      "\nHe sits in front of his hearth smoking a long clay pipe."
      "\nThough your portly stomach is bound, you can feel the familiar weight of a ring in your waist-pocket.")

def additem(item):
    inventory.append(item)  # Append the item instead of reassigning inventory

def foyer():
    global hobbithealth, arefree, areinvisible, playerhealth  # Allow modification of these variables
    print("\nYou are in the evil hobbit's foyer. He stands in front of the door to bar your exit.")
    
    while True:
        choice = input("\n:")
        hitpoints = random.randint(3, 10)  # Ensure a minimum hit
        hobbitattack = random.randint(1, 6)  # Hobbit counterattack damage

        if choice in ["attack hobbit with poker", "attack", "attack hobbit"] and "poker" in inventory:
            print(f"\nYou whack the evil hobbit for {hitpoints} hitpoints!")
            hobbithealth -= hitpoints

            if hobbithealth <= 0:
                print("\nYou kill the evil hobbit and escape through the quaint round door!")
                sys.exit()  # Exit game successfully

            # Hobbit fights back if still alive
            print(f"\nThe evil hobbit retaliates! He slashes you for {hobbitattack} hitpoints!")
            playerhealth -= hobbitattack

            # Check if the player dies
            if playerhealth <= 0:
                print("\nYou collapse from your wounds. The evil hobbit gobbles you up!")
                sys.exit()

            continue

        else:
            print("\nThe evil hobbit gobbles you up while you're deciding what to do.")
            sys.exit()

while True:
    choice = input("\n:")
    if turns < 1:
        print("\nThe evil hobbit eventually gets bored with your nonsense and eats you alive.")
        sys.exit()

    if choice == "look at hobbit":
        print("\nTight curly rings of hair around his head and toe knuckles. A pentagram glows from the furrows of his burnished forehead. Flame red eyes.")
        turns -= 1
        continue

    elif choice in ["i", "inventory"]:
        print(f"\nYou are carrying: {', '.join(inventory) if inventory else 'nothing'}")
        turns -= 1

    elif choice == "get ring":
        if "ring of power" not in inventory:
            additem("ring of power")
            print("\nYou wriggle a hand free and clasp the ring in your palm. It whispers words of black speech into your mind.")
            turns -= 1
        else:
            print("\nYou already have the ring.")

    elif choice == "put on ring" and "ring of power" in inventory:
        print("\nYou slip the gold circle over the end of your finger. The evil hobbit rises to his feet and shrieks."
              "\nHe reaches for the fire poker.")
        areinvisible = True
        turns -= 1

    elif choice == "listen to black speech":
        print("\nIf it were me, I'd speak the words that free.")
        turns -= 1
    
    elif choice in ["speak the words that free", "say the words that free"] and areinvisible:
        print("\nYou speak the words of the spell. Your bonds are loosed and you are now free to move. The evil hobbit looks around for you like a demon possessed.")
        turns = 10
        arefree = True
        continue

    elif choice in ["speak the words that free", "say the words that free"] and not areinvisible:
        print("\nYou speak the words of the spell. Your bonds are loosed and you are now free to move. The evil hobbit sees you and stabs you with a burning hot poker.")
        sys.exit()

    elif choice in ["search room", "look around room", "l", "look"] and arefree and not hasbeensaidonce:
        print("\nYou crawl around the hearth room on your hands and knees so as to avoid the hot poker being violently brandished through the air."
              "\nThe evil hobbit drops the poker with a loud clang and rushes to the round door of the foyer to make sure you don't escape.")
        turns -= 1
        hasbeensaidonce = True
        continue

    elif choice in ["search room", "look around room", "l", "look"] and arefree and hasbeensaidonce:
        print("\nThe evil hobbit has left the hearth room to the south.")
        turns -= 1
        continue

    elif choice in ["get poker", "get hot poker"] and arefree:
        additem("poker")
        print("\nYou take care to pick up the poker by the less hot end.")
        turns -= 1
        continue

    elif choice in ["s", "south"] and arefree:
        foyer()

    else:
        print("\nI'm dreadfully sorry but I don't understand.")
        turns -= 1
        continue
