"""
Maze Solver with Breadth-First Search and Curses Visualization
"""

import curses
from curses import wrapper
from collections import deque
import time
from enum import Enum

# Constants
START = 'O'
END = 'X'
OBSTACLE = '#'

# for code clarity and readability
class Color(Enum):

    BLUE = 1
    RED = 2


maze = [
    ["#", "#", "#", "#", START, "#", "#", "#", "#"],
    ["#", " ", " ", " ", " ", " ", " ", " ", "#"],
    ["#", " ", "#", "#", " ", "#", "#", " ", "#"],
    ["#", " ", "#", " ", " ", " ", "#", " ", "#"],
    ["#", " ", "#", " ", "#", " ", "#", " ", "#"],
    ["#", " ", "#", " ", "#", " ", "#", " ", END],
    ["#", " ", "#", " ", "#", " ", "#", "#", "#"],
    ["#", " ", " ", " ", " ", " ", " ", " ", "#"],
    ["#", "#", "#", "#", "#", "#", "#", "#", "#"]
]


def print_maze(stdscr, maze, path=[]):
    BLUE = curses.color_pair(Color.BLUE.value)
    RED = curses.color_pair(Color.RED.value)

    for i, row in enumerate(maze):
        for j, value in enumerate(row):
            if (i, j) in path:
                stdscr.addstr(i, j*2, 'X', RED)
            else:
                stdscr.addstr(i, j*2, value, BLUE)


def find_start(maze, start):
    for i, row in enumerate(maze):
        for j, value in enumerate(row):
            if value == start:
                return i, j
    return None

# Finds valid neighboring positions for a given row and column in the maze
def find_neighbors(maze, row, col):
    neighbors = []
    if row > 0:  # above
        neighbors.append((row - 1, col))
    if row + 1 < len(maze):  # below
        neighbors.append((row + 1, col))
    if col > 0:  # left
        neighbors.append((row, col - 1))
    if col + 1 < len(maze[0]):  # right
        neighbors.append((row, col + 1))

    return neighbors

# Initializes and returns a deque with the starting position and path.
def initialize_queue(maze, start):
    q = deque()
    start_position = find_start(maze, START)
    q.append((start_position, [start_position]))

    return q


def update_screen(stdscr, maze, path):
    stdscr.clear()
    time.sleep(0.2)
    print_maze(stdscr, maze, path)
    stdscr.refresh()

# Checks if a position is not an obstacle and not visited.
def is_valid_position(maze, position, visited):
    row, col = position
    return position not in visited and maze[row][col] != OBSTACLE


def find_path(stdscr, maze):
    visited = set()  # stores the visited position

    q = initialize_queue(maze, START)

    # while the q contains unprocessed positions
    while q:
        # extract one position
        current_position, path = q.popleft()
        # add the position to the visited set
        visited.add(current_position)
        row, col = current_position

        update_screen(stdscr, maze, path)

        # end the function if we find the end
        if maze[row][col] == END:
            return

        # otherwise, find the neighbors of that position
        neighbors = find_neighbors(maze, row, col)

        for neighbor in neighbors:

            if is_valid_position(maze, neighbor, visited):
                q.append((neighbor, path + [neighbor]))


def main(stdscr):
    curses.init_pair(Color.BLUE.value, curses.COLOR_BLUE, curses.COLOR_BLACK)
    curses.init_pair(Color.RED.value, curses.COLOR_RED, curses.COLOR_BLACK)

    find_path(stdscr, maze)
    stdscr.getch()


wrapper(main)
