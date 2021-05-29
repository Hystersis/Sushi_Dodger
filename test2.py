class add:
    def __init__(self):
        pass
    def add(self,x):
        self.instience = []
        for i in range(x):
            self.instience.append(Dog(x))
    def command(self,c):
        for i in self.instience:
            i .c()

class Dog:
    def __init__(self,name):
        self.name = name
        print("added")
    def speak(self):
        print('Woof')

def func(hello):
    print(hello)

func()
def func2(f):
    def wrapper(*args, **kwargs):
        kv = f(*args,**kwargs)
