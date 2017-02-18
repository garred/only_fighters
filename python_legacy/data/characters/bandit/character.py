from data.characters.ninja.character import NinjaCharacter, NinjaEnemy, NinjaPlayer
from characters import load_animations




# Loading all the animation files

animations = load_animations('data/characters/bandit/')



# Bandit class

class BanditCharacter(NinjaCharacter):

    def __init__(self):
        super(BanditCharacter, self).__init__()
        self.animations = {name: animation.getCopy() for name, animation in animations.items()}


class BanditEnemy(NinjaEnemy):

    def __init__(self):
        super(BanditEnemy, self).__init__()
        self.animations = {name: animation.getCopy() for name, animation in animations.items()}


class BanditPlayer(NinjaPlayer):

    def __init__(self, keymap):
        super(BanditPlayer, self).__init__(keymap)
        self.animations = {name: animation.getCopy() for name, animation in animations.items()}