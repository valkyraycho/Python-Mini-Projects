"""
Assumptions:

- data directory contains many files and directories
- you are only interested in the games contained in this directory
- each game is stored in a directory that contains the word "game"
- each game directory contains a single .go file that must be compiled before it can be run


Project Steps/Requirements:

- Find all game directories from /data
- Create a new /games directory 
- Copy and remove the "game" suffix of all games into the /games directory
- Create a .json file with the information about the games
- Compile all of the game code 
- Run all of the game code-
"""

import os
import json
import shutil
from subprocess import PIPE, run
import sys

GAME_DIR_PATTERN = '_game'
GAME_CODE_EXTENSION = '.go'
GAME_COMPILE_COMMAND = ['go', 'build']

def find_all_game_paths(source):
    # game_paths = []
    
    # for root, dirs, files in os.walk(source):
    #     for directory in dirs:
    #         if directory.lower().endswith(GAME_DIR_PATTERN):
    #             path = os.path.join(source, directory)
    #             game_paths.append(path)
    #     # break
    
    # return game_paths
    return [os.path.join(source, entry) 
            for entry in os.listdir(source) 
            if os.path.isdir(os.path.join(source, entry)) 
            and entry.lower().endswith(GAME_DIR_PATTERN)]

def new_names_from_paths(paths, to_strip):
    new_names = []
    
    for path in paths:
        _, directory = os.path.split(path)
        new_dir = directory.replace(to_strip, '')
        new_names.append(new_dir)
        
    return new_names

def create_directory(target_path):
    if os.path.exists(target_path):
        shutil.rmtree(target_path)
    os.mkdir(target_path)
        
def copy_and_overwrite(source, destination):
    if os.path.exists(destination):
        shutil.rmtree(destination)
    
    shutil.copytree(source, destination)
    
def make_json_metadata_file(path, game_dirs):
    data = {
        'games': game_dirs,
        'numberOfGames': len(game_dirs)
    }
    
    with open(path, 'w') as f:
        json.dump(data, f)
  
def compile_game_code(path, game_extension):
    # code_file_name = None
    
    # for root, dirs, files in os.walk(path):
    #     for file in files:
    #         if file.endswith(game_extension):
    #             code_file_name = file
    
    go_files = [file for file in os.listdir(path) if file.endswith(game_extension)]

    for code_file_name in go_files:
        command = GAME_COMPILE_COMMAND + [code_file_name]
        run_command(command, path)
    
def run_command(command, path):
    cwd = os.getcwd()
    os.chdir(path)
    
    result = run(command, stdout=PIPE, stdin=PIPE, universal_newlines=True)
    print(result)
    
    os.chdir(cwd)
    
def main(source, target):
    cwd = os.getcwd()
    source_path = os.path.join(cwd, source)
    target_path = os.path.join(cwd, target)
    
    game_paths = find_all_game_paths(source_path)
    new_game_dirs = new_names_from_paths(game_paths, GAME_DIR_PATTERN)
    
    create_directory(target_path)
    
    for src, dest in zip(game_paths, new_game_dirs):
        dest_path = os.path.join(target_path, dest)
        copy_and_overwrite(src, dest_path)
        compile_game_code(dest_path, GAME_CODE_EXTENSION)
        
    json_path = os.path.join(target_path, 'metadata.json')
    make_json_metadata_file(json_path, new_game_dirs)

if __name__ == "__main__":
    args = sys.argv
    if len(args) != 3:
        raise Exception('You must provide a source and a target directory only')
    
    source, target = args[1:]
    main(source, target)