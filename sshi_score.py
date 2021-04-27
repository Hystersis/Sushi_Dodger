# Sshi score module
import json
from itertools import repeat


class scoreboard:
    def __init__(self):
        with open('scoreboard.json', 'w') as board:
            json.dump({'scores': {}}, board)

    def write(self, name, score):
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

        if self.scores['scores'] == {}:
            return list(repeat(('JDH', 000), 10))
        else:
            return list(sorted(self.scores['scores'].items(),
                               key=lambda item: item[1]))
            # This sorts the scores by the score value
            # This is done by item[1] = score
