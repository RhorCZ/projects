import random
import time
from datetime import datetime
import os
import sys

#Values
SEPARATOR = "-----------------------------------------------"
RANDOM_NUMBER = str(random.randint(1000,9999))
RANDOM_NUMBER_TUPLE = tuple(RANDOM_NUMBER)
START_TIME = time.time()
SCRIPT_PATH = os.path.dirname(os.path.realpath(sys.argv[0]))

#Welcome
def welcome_user():
    print("Hi there!")
    print(SEPARATOR)
    print("I've generated a random 4 digit number for you.\nLet's play a bulls and cows game.")
    print(SEPARATOR)

#Check given input
def is_correct_input(user_input):
    if not user_input.isdigit() or len(user_input) != 4:
            print("Wrong input!")
            print(SEPARATOR)
            return False

#Handle user's input
def handle_input(user_input):
    input_list = tuple(user_input) 
    bulls, used_list = get_bulls(input_list)
    cows = get_cows(input_list, used_list)

    input_result(bulls, cows)

#Get bulls
def get_bulls(input_list):
    used = dict()
    bulls = 0
    for index in range(len(input_list)):
            num = input_list[index]
            if num in RANDOM_NUMBER:
                if num == RANDOM_NUMBER_TUPLE[index]:
                    used[index] = num
                    bulls += 1
    return bulls, used

#Get cows
def get_cows(input_list, used):
    cows = 0
    for index in range(len(input_list)):
        if not index in used.keys():
            num = input_list[index]
            repeats = RANDOM_NUMBER.count(num)
            if num in RANDOM_NUMBER:
                if repeats != sum([1 for i in used.values() if i == num]):
                    used[index] = num
                    cows += 1
    return cows

#Print result of user's input
def input_result(bulls,cows):
    bull_word = "bulls"
    cow_word = "cows"

    if bulls == 1:
        bull_word = "bull"
    if cows == 1:
        cow_word = "cow"

    print(f"{bulls} {bull_word}, {cows} {cow_word}")
    print(SEPARATOR)

#Get time
def get_time():
    elapsed = round((time.time() - START_TIME))
    minutes, seconds = divmod(elapsed,60)            

    return f'{minutes} minutes and {seconds} seconds'

#user evaluation
def get_score(tries):
    if tries <= 2:
        return "amazing"
    elif tries <= 5:
        return "good"
    elif tries <= 7:
        return "average"
    else:
        return "not so good"

#Save results to file
def save_to_file(filename,took_time, tries, score):
    with open(filename, "a+") as file:
        now = datetime.now().strftime("[%d.%m.%Y %H:%M:%S]")
        file.write(f"{now} Number: {RANDOM_NUMBER} Tries: {tries} Score: {score} Duration: {took_time} \n")
        file.close()

#End game results
def end_of_game(tries):
    guess_word = "guesses"
    score = get_score(tries)
    took_time = get_time()

    if tries == 1:
        guess_word = "guess"

    print(SEPARATOR)
    print(f"Correct, you've guessed the right number\nin {tries} {guess_word}.")
    print(f"It took you: {took_time}")
    print(SEPARATOR)

    print(f"That's {score}.")
    print(SEPARATOR)

    print("Writing game stats to file...")
    save_to_file(os.path.join(SCRIPT_PATH,"bulls_cows_stats.txt"),took_time,tries,score)
    print("Done")

#Start the game
def start_game():
    welcome_user()
    tries = 0
    while True:
        user_input = input("Enter number:")
        tries += 1

        if is_correct_input(user_input) == False:
            continue

        if user_input == RANDOM_NUMBER:
            end_of_game(tries)
            break

        handle_input(user_input)


def main():
    start_game()

main()