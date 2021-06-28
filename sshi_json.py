# Sshi score module
import json
from itertools import repeat
import os
import random
from collections import Counter


class scoreboard:
    def __init__(self):
        if not os.path.isfile('scoreboard.json'):
            # File doesn't exist
            with open('scoreboard.json', 'w') as board:
                json.dump({'scores': {}}, board)

    def write(self, name: str, score: int):
        name = '{:<3}'.format(name.upper()[:3])
        score = '{:>3}'.format(str(score)[:3])
        print('Name, score', name + score)
        with open('scoreboard.json', 'r') as board:
            self.scores = json.load(board)
            print(self.scores)

        with open('scoreboard.json', 'w') as board:
            self.scores['scores'][name] = score
            print(self.scores)
            json.dump(self.scores, board, indent=4)

    def get(self):
        with open('scoreboard.json', 'r') as board:
            self.scores = json.load(board)
            return list(sorted(self.scores['scores'].items(),
                               key=lambda item: item[1]))[:10][::-1] + list(
                    repeat(('JDH', '  0'),
                           max(0, 10 - len(self.scores['scores'].keys()))))
            # This sorts the scores by the score value
            # This is done by item[1] = score
            # [:10] gets the top ten
            # [::-1] reverses the list so that the first is first


class config:
    def __init__(self):
        if not os.path.isfile('scoreboard.json'):
            raise Exception('Config file was deleted!')

    def get(self, write_to):
        with open('scoreboard.json', 'r') as board:
            self.values = json.load(board)['settings']
            for y, v in self.values.items():
                setattr(write_to, str(y), int(v))


class items:
    rarity_classes = {
        1: 43.125,
        2: 25.125,
        3: 10,
        4: 8,
        5: 6,
        6: 4,
        7: 2,
        8: 1,
        9: 0.5,
        10: 0.25
    }

    def __init__(self):
        if not os.path.isfile('scoreboard.json'):
            raise Exception('Items file was deleted!')

    def return_item(self, item_function):
        with open('scoreboard.json', 'r') as board:
            self.items = json.load(board)['items']
        self.choice = random.choices([x['name'] for x in self.items],
                       [items.rarity_classes[x['rarity']] for x in self.items])
        self.choice_values = [x for x in self.items if x['name'] == self.choice[0]][0]
        print(self.choice, self.choice_values)
        item = item_function(**(self.choice_values))
        return item

def test(*args, **kwargs):
    print(args, kwargs)
