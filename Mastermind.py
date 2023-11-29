import random

COLORS = ["R", "G", "B", "Y", "O", "W"]
TRIES = 10
CODE_LENGTH = 4


def generate_code():
    return random.sample(COLORS, CODE_LENGTH)


def guess_code():
    while True:
        guesses = input("Your guess: ").strip().upper().split(" ")

        if len(guesses) != CODE_LENGTH:
            print(f"You must enter {CODE_LENGTH} letters.")
            continue

        for guess in guesses:
            if guess not in COLORS:
                print(f"{guess} is not a valid color.")
                break
        else:
            break

    return guesses


def check_code(guess_code, real_code):
    color_counts = {}
    correct_positions = 0
    incorrect_positions = 0

    for color in real_code:
        if color not in color_counts:
            color_counts[color] = 0
        color_counts[color] += 1

    print(color_counts)
    

    for guess, real in zip(guess_code, real_code):
        if guess == real:
            correct_positions += 1
            color_counts[guess] -= 1
            
    print(color_counts)
    

    for guess, real in zip(guess_code, real_code):
        if guess != real and guess in color_counts and color_counts[guess] > 0:
            incorrect_positions += 1
            color_counts[guess] -= 1
            
    print(color_counts)

    return correct_positions, incorrect_positions


def welcome_message(game_count):
    print(f"Welcome to Mastermind. Game {game_count}")
    print(f"You have {TRIES} tries to guess the code.")
    print(f"The valid colors are: {', '.join(COLORS)}")
    print(f"The code will be {CODE_LENGTH} letters long.")
    print("-"*40)
    print()


def game():
    game_count = 1

    while True:
        welcome_message(game_count)
        code = generate_code()
        for attempt in range(1, TRIES + 1):
            guess = guess_code()
            correct_positions, incorrect_positions = check_code(guess, code)

            if correct_positions == CODE_LENGTH:
                print(
                    f"Congratulations! You guessed the code in {attempt} tries.")
                break

            print(f"Correct positions: {correct_positions} | Incorrect positions: {incorrect_positions}")
            print()

        else:
            print(f"All {TRIES} tries have been used. The code is: ", *code)

        continue_game = input("Would you like to play again? (y/n):").lower()
        if continue_game == "n":
            break


if __name__ == "__main__":
    game()
