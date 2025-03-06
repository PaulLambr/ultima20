import random
import os

# Define a simple mapping: A-Z → 0-25
alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

def generate_keystream(seed, length):
    """Generate a pseudo-random keystream based on the seed."""
    random.seed(seed)
    return [random.randint(0, 31) for _ in range(length)]

def encrypt(plaintext, keystream):
    """Encrypt plaintext by XORing it with the keystream and mapping to a character set."""
    ciphertext = ""
    for i in range(len(plaintext)):
        pt_val = alphabet.index(plaintext[i])
        ct_val = pt_val ^ keystream[i]  # XOR operation
        ciphertext += alphabet[ct_val % len(alphabet)]  # Ensure it's within valid range
    return ciphertext

def decrypt_with_fragment(ciphertext, ks_fragment):
    """Attempt partial decryption using a guessed keystream fragment."""
    decrypted = ""
    for i in range(len(ciphertext)):
        ct_val = alphabet.index(ciphertext[i])
        if i < len(ks_fragment):
            pt_val = ct_val ^ ks_fragment[i]
            decrypted += alphabet[pt_val % len(alphabet)]  # Map back to a letter
        else:
            decrypted += "_"  # Unknown characters remain masked
    return decrypted

# --- Player 1: Encrypt the Message ---
plaintext = input("Player 1, enter your secret message (A-Z only, no spaces): ").upper()
pin = input("Enter a 4-letter PIN (A-Z only): ").upper()

# Generate a numeric seed from the PIN
seed = sum(alphabet.index(letter) for letter in pin)

# Generate keystream and encrypt the message
keystream = generate_keystream(seed, len(plaintext))
ciphertext = encrypt(plaintext, keystream)

# Clear the terminal for secrecy
os.system('cls' if os.name == 'nt' else 'clear')

print("\nPlayer 2, here is the ciphertext:")
print(ciphertext)

# --- Player 2: Code Breaking ---
attempts = 3
best_guess = ""
best_fragment = []

for attempt in range(attempts):
    crib = input(f"\nAttempt {attempt + 1}: Guess the first few letters of the plaintext: ").upper()

    # Compute guessed keystream fragment
    guessed_ks = []
    for i in range(len(crib)):
        if crib[i] in alphabet:
            ct_val = alphabet.index(ciphertext[i])
            pt_val = alphabet.index(crib[i])
            guessed_ks.append(ct_val ^ pt_val)

    # Decrypt using guessed keystream fragment
    decrypted_fragment = decrypt_with_fragment(ciphertext, guessed_ks)
    print("\nDecrypted fragment based on your crib:")
    print(decrypted_fragment)

    # Store the best attempt (heuristic: most readable output)
    if decrypted_fragment.count("_") < len(decrypted_fragment):  
        best_guess = crib
        best_fragment = guessed_ks

print("\nFinal Round: Use your best crib attempt to manually decode the rest of the message!")
print("Ciphertext:", ciphertext)
print("Best Crib:", best_guess)
print("Use logic to manually decode the rest!")

# Optional: Reveal the actual message after the game
reveal = input("\nDo you want to reveal the full plaintext? (Y/N): ").upper()
if reveal == "Y":
    full_decrypted = decrypt_with_fragment(ciphertext, keystream)
    print("\nFull Plaintext:", full_decrypted)
else:
    print("Keep guessing! The answer remains a secret.")
