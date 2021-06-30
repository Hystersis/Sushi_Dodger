class a:
    def __init__(self) -> None:
        self._a = 1
    
    @property
    def a(self):
        return self._a
    
    @a.setter
    def a(self, value):
        self._a = value