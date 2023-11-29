import random
import time

# roll function


def roll():
    MIN = 1
    MAX = 6
    return random.randint(MIN, MAX)


def players_round():
    print(f"\nPlayer's turn!")
    print(f"Your total score is {player_scores[player]}.")
    current_score = 0

    while True:
        play = input("\nroll? [y/n]: ")
        while play.lower() != 'y' and play.lower() != 'n':
            print("Invalid input.")
            play = input("\nroll? [y/n]: ")

        if play.lower() != 'y':
            break

        value = roll()
        if value == 1:
            print("\nYour rolled a 1! Turn done")
            current_score = 0
            break

        current_score += value
        print(f"\nYou rolled a {value}.")
        print(f"Your current score for this round is {current_score}")
        print(f"Your possible total score for this round is {current_score+player_scores[player]}")

    player_scores[player] += current_score
    print(f"\nYour total score is {player_scores[player]}.")


def computers_round():
    print(f"\nComputer {player}'s turn!")
    print(f"Computer {player}'s total score is {player_scores[player]}.")
    current_score = 0

    while True:
        time.sleep(1)
        if player_scores[player] == 0 and current_score == 0:
            play = True
        elif current_score == 0:
            play = True
        else:
            play = random.randint(0, 3)

        if not play:
            print(f"\nComputer {player} chose not to play.")
            break

        value = roll()
        if value == 1:
            print(f"\nComputer {player} rolled a 1! Turn done")
            current_score = 0
            break

        current_score += value
        print(f"\nComputer {player} rolled a {value}.")
        print(f"Computer {player}'s current score for this round is {current_score}")
        print(f"Computer {player}'s possible total score for this round is {current_score+player_scores[player]}")

    player_scores[player] += current_score
    print(f"\nComputer {player}'s total score is {player_scores[player]}.")


# initial setup
while True:
    num_of_players = input("Enter the number of players (2-4): ")
    if num_of_players.isdigit():
        num_of_players = int(num_of_players)
        if 2 <= num_of_players <= 4:
            break
        else:
            print("The number should be between 2 and 4.")
    else:
        print("Invalid input.")

MAX_SCORE = 50
player_scores = [0 for _ in range(num_of_players)]

# game start
while max(player_scores) < 50:
    for player in range(num_of_players):
        if player == 0:
            players_round()
        else:
            computers_round()

    print("\nScoreboard:")
    print("Player:", player_scores[0])
    for i in range(1, num_of_players):
        print(f"Computer {i}:", player_scores[i])

winner_score = max(player_scores)
winner = player_scores.index(winner_score)
if winner == 0:
    print(f"Player is the winner with a score of: {winner_score}")
else:
    print(f"Computer {winner} is the winner with a score of: {winner_score}")
