import sys
import clipboard
import json

SAVE_DATA = 'clipboard.json'


def save_data(filepath, data):
    with open(filepath, 'w') as f:
        json.dump(data, f)


def load_data(filepath):
    try:
        with open(filepath, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}


if len(sys.argv) == 2:
    command = sys.argv[1]
    data = load_data(SAVE_DATA)

    if command == 'save':
        key = input('Enter the key to save the data under: ')
        data[key] = clipboard.paste()
        save_data(SAVE_DATA, data)
        print(f'Data saved under {key}')

    elif command == 'load':
        key = input('Enter the key to load the data from: ')
        if key in data:
            clipboard.copy(data[key])
            print(f'Data loaded under {key}')
        else:
            print('Invalid key')

    elif command == 'list':
        print(data)

    else:
        print('Invalid command')
else:
    print('Please pass exactly one command.')
