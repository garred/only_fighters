from items import Item, load_animations


animations = load_animations('data/items/', 'bow')


class Bow(Item):

    def __init__(self, pos):
        super(Bow, self).__init__(pos)
        self.animations = {name: animation.getCopy() for name, animation in animations.items()}
        self.animation = None
        self.set_animation('touch')


    def touched_by(self, character):
        super(Bow, self).touched_by(character)

        dis = self.distance_to(character)
        if not self.taken and dis < 20:
            if 'hit' in character.animation_name:
                character.weapon = 'bow'
                self.kill()
                self.taken = True