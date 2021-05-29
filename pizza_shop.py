from collections import OrderedDict
import itertools
import threading
import time
from rich import print
from rich.layout import Layout
from rich.panel import Panel
from rich.progress import Progress
from rich.prompt import Confirm

class Order:
    orders = OrderedDict()
    def __init__(self,p,name):
        self.p = [p.title() for p in p]
        print(self.p)
        self.o = Pizza(p)
        self.i = self.o.get_ingredients()
        self.n = name.title()
        Order.orders[name] = self.o
        Kitchen.make_order(self.i)


class Pizza:
    pizzas = {
    'Presets': ['Carne','Hawaiian','Mozzerella'],
    'Meat': ['Ham','Turkey','Salami','Pepperoni','Beef','Cabanossi','Bacon'],
    'Cheese': ['Parmaesan','Cheedar']
    }
    preMade = {'Carne':['Ham', 'Pepperoni', 'Cabanossi', 'Beef', 'Bacon'],'Hawaiian':['Ham','Salami','Cheedar'],'Mozzerella':['Cheddar']}
    def __init__(self,p):
        self.p = set(p)
        self.ingredients = []
        for y, x in Pizza.pizzas.items():
            z = set(x)
            print(self.p)
            self.ingredients += list(self.p.intersection(z))
            print(self.p.difference_update(set(self.p.intersection(z))))
            self.p.difference_update(set(self.p.intersection(z)))
            print(self.p)
            if (y == 'Presets') and self.ingredients != []:
                self.premade(self.ingredients[0])
            break
        # Add expection code here
        if type(self.p) != None:
            raise Exception(f'Invalid ingredients {self.p}')

    def premade(self,x):
        self.ingredients = Pizza.preMade[x]
    def get_ingredients(self):
        return self.ingredients

class Kitchen:
    def __init__(self,x):
        pass
    @classmethod
    def make_order(cls,x):
        with Progress() as progress:
            Meats, Cheese = [], []
            for i in x:
                print(i)
                if i in Pizza.pizzas['Meat']:
                    Meats.append(i)
                elif i in Pizza.pizzas['Cheese']:
                    Cheese.append(i)
            task1 = progress.add_task('[red]Putting on meats...\t',total = len(Meats))
            for i in Meats:
                time.sleep(1)
                progress.update(task1, advance=1)
            task2 = progress.add_task('[yellow]Putting on cheeses...\t',total = len(Cheese))
            for i in Cheese:
                time.sleep(0.5)
                progress.update(task1, advance=1)
            print()

def mainloop(l,upper,all):
    l.update(Panel('[red]Please enter your order [/red] [blink](using a space to seperate different items):',title = '[red underline]Your order:'))
    print(all)
    e = input('>>>')
    e = e.split(' ')
    u = str(f'[red]Please enter your order [/red] [blink](using a space to seperate different items)[/blink]:\n [white]{e}\n[yellow]Your name:')
    l.update(Panel(u,title = '[red underline]Your order:'))
    pizza_options = str(Pizza.pizzas)
    for i in Pizza.pizzas.values():
        for i in i:
            for x in e:
                if i == x.title(): pizza_options = pizza_options.replace(f'{x.title()}',f'[reverse yellow]{x.title()}[/reverse yellow]')
    upper.update(Panel(pizza_options,title = '[blue underline]Menu'))
    print(all)
    f = str(input('>>>'))
    u += f'{f}'
    l.update(Panel(u,title = '[red underline]Your order:'))
    print(all)
    Order(e,f)

global pizza_art
pizza_art = "[white]                                     ._\n                                   ,(  `-.\n                                 ,\': `.   `.\n                               ,` *   `-.   \n                             ,\'  ` :+  = `.  `.\n                           ,~  (o):  .,   `.  `.\n                         ,\'  ; :   ,(__) x;`.  ;\n                       ,\'  :\'  itz  ;  ; ; _,-\'\n                     .\'O ; = _\' C ; ;\'_,_ ;\n                   ,;  _;   ` : ;\'_,-\'   i\'\n                 ,` `;(_)  0 ; \',\'       :\n               .\';6     ; \' ,-\'~\n             ,\' Q  ,& ;\',-.\'\n           ,( :` ; _,-\'~  ;\n         ,~.`c _\',\'\n       .\';^_,-\' ~\n     ,\'_;-\'\'\n    ,,~\n    i\'\n    :"

if __name__ == '__main__':
    print('working')
    layout = Layout()
    layout.split_column(
        Layout(name = "Menu"),
        Layout(name = "Your order")
    )
    print(Pizza.pizzas)
    while True:
        layout["Menu"].update(Panel(str(Pizza.pizzas),title = '[blue underline]Menu'))
        mainloop(layout["Your order"],layout["Menu"],layout)
        print(pizza_art)
        end_output = '=' * 50 + '\nDo you want to make another order?\n' + '=' * 50 + '\n'
        end_check = Confirm.ask(end_output)
        if end_check == True:
            continue
        else:
            break
