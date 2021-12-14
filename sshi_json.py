# Sshi score module
import json
from itertools import repeat
import os
import random
from collections import Counter

# !FILE = scoreboard.json

# It is in this form, so it is readable as json 'code'
json_file_template = """
{
    "scores": {

    },
    
    "settings": {
        "Music": true,
        "SFX": true
    },
    "items": [
        {
            "name": "slow down time",
            "effects": {
                "fps": 8
            },
            "rarity": 3,
            "duration": 5,
            "sprite": [
                0,
                12
            ]
        },
        {
            "name": "health",
            "instants": {
                "health": 1
            },
            "rarity": 10,
            "sprite": [
                0,
                0
            ]
        },
        {
            "name": "restart",
            "rarity": 2,
            "instants": {
                "restart": null
            },
            "key_press": "F5",
            "sprite": [
                12,
                12
            ]
        }
    ]
}
"""

def init():
    """This creates the json file if it doesn't exist with the template above,
    it must be called before all functions
    """
    global json_file_template
    # Creates the scoreboard.json file
    if not os.path.isfile('scoreboard.json'):
        # This creates the file
        with open("scoreboard.json", "w") as jsonfile:
            # This deserializes the json data into 'python' form
            x = json.loads(json_file_template)

            # This then takes that python friendly form and writes it to the json file (converting it) 
            json.dump(x, jsonfile, indent=4)
            
        

class scoreboard:
    """The manager for the scoreboard and the scoreboard part of FILE
    """
    def __init__(self):
        """Resets the scoreboard if the FILE doesn't exist
        """
        # if not os.path.isfile('scoreboard.json'):
        #     # File doesn't exist
        #     with open('scoreboard.json', 'w') as board:
        #         json.dump({'scores': {}}, board)
        pass

    def write(self, name: str, score: int):
        """Writes a players name to the scoreboard

        Parameters
        ----------
        name : str
            A 3-letter name for the player
        score : int
            The player's name

        Parameters
        ----------
        scores : dict
            The retrieved scores from FILE
        """
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
        """Returns a list of scores to be displayed

        Notes
        -----
        The list has to be 10 long so it 'pads' the scores with JDH : 0,
        to add length - this is also an easter egg ;-)

        It sorts the scores from heighest to lowest with the sorted() function
        it uses lambda to retrieve the key from the value (name belonging to
        the score)

        Returns
        -------
        list
            A list of 10 long with the scores
        """
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
    """This retrieves all the settings from FILE
    file
    """
    def __init__(self):
        """Check that FILE exists

        Raises
        ------
        Exception
            If FILE/config file exists
        """
        if not os.path.isfile('scoreboard.json'):
            raise Exception('Config file was deleted!')

    def get(self, write_to):
        """Gets all the settings from FILE and writes them to a class

        Parameters
        ----------
        write_to : class
            The class were the retrieved settings will be written to
        """        
        with open('scoreboard.json', 'r') as board:
            self.values = json.load(board)['settings']
            for y, v in self.values.items():
                setattr(write_to, str(y), int(v))
    
    def sget(self, name_of_value):
        """Allows for one value to be retrieved from config

        Parameters
        ----------
        value : string
            The name of the value to retriever

        Returns
        -------
        Any
            The value retrieved
        """             
        with open('scoreboard.json', 'r') as board:
            try:
                # If the desired value exists, return it
                desired_value = json.load(board)['settings'][name_of_value]
            except:
                # If it doesn't just return None
                desired_value = None
        return desired_value         
    
    def write(self, value_to_change, what_to_change_to):
        """Allows for writing to the settings values

        Parameters
        ----------
        value_to_change : string
            Which value should be changed
        what_to_change_to : Any
            What the value should be changed to
        """        
        with open('scoreboard.json', 'r') as board:
            self.values = json.load(board)
            print(self.values)

        with open('scoreboard.json', 'w') as board:
            self.values['settings'][value_to_change] = what_to_change_to
            print(self.values)
            json.dump(self.values, board, indent=4)


class items:
    """The class for managing all the classes

    Attributes
    ----------
    rarity_classes : dict
        Maps the rarity 'rank' to float value,
        the higher the 'rank' the higher the float
        so the higher the chance of the item
    """
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
        """This check the FILE exists

        Raises
        ------
        Exception
            Raises if FILE doesn't exist
        """
        if not os.path.isfile('scoreboard.json'):
            raise Exception('Items file was deleted!')

    def return_item(self, item_function, **kwargs):
        """[summary]

        Parameters
        ----------
        item_function : sshi_core.item
            Creates the item by change the item_function's values, this
            determines how the item interacts with the environment

        Returns
        -------
        sshi_core.item
            This is the class -item-, with all its values set for proper interaction
        """        
        with open('scoreboard.json', 'r') as board:
            self.items = json.load(board)['items']
        self.choice = random.choices([x['name'] for x in self.items],
                       [items.rarity_classes[x['rarity']] for x in self.items])
        self.choice_values = [x for x in self.items if x['name'] == self.choice[0]][0]
        item = item_function(**kwargs, **(self.choice_values))
        return item

    def item_val(self, key: str, value: str) -> list:
        """Returns the value of specific item from FILE
        e.g. Rarity of health = 10

        Parameters
        ----------
        key : str
            The item to retrieve the value from
        value : str
            The value to be retrieved

        Returns
        -------
        any
            Returns the requested value from the !First! item seen
        """
        with open('scoreboard.json', 'r') as board:
            self.avaitems = json.load(board)['items']
        return [x[value] for x in self.avaitems if x['name'] == key][0]
