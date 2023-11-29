import curses
from curses import wrapper
import random
import time

FILE_PATH = r'C:\Users\razor\Desktop\Python\Project Practice\Mini Projects\Typing Speed Test\Typing speed test.txt'

GREEN = 1
RED = 2
WHITE = 3

def start_screen(stdscr):
    stdscr.clear()
    stdscr.addstr('Welcome to the Speed Typing Test')
    stdscr.addstr('\nPress any key to begin!')
    stdscr.refresh()
    stdscr.getkey()
    

def display_text(stdscr, current_text, target_text, wpm):
    stdscr.addstr(target_text)
    stdscr.addstr(1, 0, f"WPM: {wpm}")
    color = curses.color_pair(GREEN)
    for i, char in enumerate(current_text):
        if char != target_text[i]:
            color = curses.color_pair(RED)
        stdscr.addstr(0, i, char, color)

def update_wpm(current_text, start_time):
    time_elapsed = max(time.time() - start_time, 1)
    return round((len(current_text) / (time_elapsed / 60)) / 5)

def load_text():
    with open(FILE_PATH, 'r') as f:
        lines = f.readlines()
        return random.choice(lines).strip()


def wpm_test(stdscr):
    target_text = load_text()
    current_text = []
    wpm = 0
    start_time = time.time()
    stdscr.nodelay(True)

    while True:
        stdscr.clear()
        wpm = update_wpm(current_text, start_time)
        display_text(stdscr, current_text, target_text, wpm)

        if "".join(current_text) == target_text:
            stdscr.nodelay(False)
            return True

        try:
            key = stdscr.getkey()
        except:
            continue

        if ord(key) == 27:
            return False

        if key in ('KEY_BACKSPACE', '\b', '\x7f'):
            if len(current_text) > 0:
                current_text.pop()
        elif len(current_text) < len(target_text):
            current_text.append(key)

        stdscr.refresh()


def main(stdscr):
    curses.init_pair(GREEN, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(RED, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(WHITE, curses.COLOR_WHITE, curses.COLOR_BLACK)
    

    start_screen(stdscr)
    while True:
        next = wpm_test(stdscr)
        if next:
            stdscr.addstr(2, 0, "You've completed! Press any key to start again or esc to end.")
            key = stdscr.getkey()
            if ord(key) == 27:
                break
        else:
            break

wrapper(main)
