from data.characters.ninja.character import NinjaCharacter, NinjaEnemy, NinjaPlayer
from characters import load_animations


# Loading all the animation files

animations = load_animations('data/characters/archer/')


# Archer class

class ArcherCharacter(NinjaCharacter):

    def __init__(self):
        super(ArcherCharacter, self).__init__()
        self.animations = {name: animation.getCopy() for name, animation in animations.items()}


class ArcherEnemy(NinjaEnemy):

    def __init__(self):
        super(ArcherEnemy, self).__init__()
        self.animations = {name: animation.getCopy() for name, animation in animations.items()}


class ArcherPlayer(NinjaPlayer):

    def __init__(self, keymap):
        super(ArcherPlayer, self).__init__(keymap)
        self.animations = {name: animation.getCopy() for name, animation in animations.items()}