# Sshi score module
import json
from itertools import repeat
import os


class scoreboard:
    def __init__(self):
        if not os.path.isfile('scoreboard.json'):
            # File doesn't exist
            with open('scoreboard.json', 'w') as board:
                json.dump({'scores': {}}, board)

    def write(self, name: str, score: int):
        name = name.upper()[:3]
        score = '{:>3}'.format(str(score)[:3])
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
