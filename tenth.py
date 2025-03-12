import random

challenges = [
    "Take a sip if you're wearing a black shirt.",
    "Take two sips if your name starts with a vowel.",
    "Pass your drink to the player on your right.",
    "Do 5 push-ups or take a sip.",
    "Tell a joke or take two sips.",
    "Do a dance for 10 seconds or take a sip.",
    "Name 3 countries in 5 seconds or take a sip.",
    "Do a tongue twister 3 times fast or take a sip.",
    "Imitate a famous person or take a sip.",
    "High five the person next to you or take a sip."
]

print("🎉 Welcome to the Python Drinking Game! 🎉")
print("Press Enter to get a challenge or type 'quit' to exit.")

while True:
    user_input = input("\nPress Enter to get a challenge: ")
    if user_input.lower() == "quit":
        print("Game over! Thanks for playing! 🎊")
        break

    challenge = random.choice(challenges)
    print("👉", challenge)
