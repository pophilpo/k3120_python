import abc

class UI(abc.ABC):
    def __init__(self, life):
        self.life = life

    @abc.abstractmethod
    def run(self):
        pass


