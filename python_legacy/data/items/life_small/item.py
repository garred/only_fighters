from items import Item, load_animations


animations = load_animations('data/items/', 'life_small')


class LifePotionSmall(Item):

    def __init__(self, pos):
        super(LifePotionSmall, self).__init__(pos)

        self.animations = {name: animation.getCopy() for name, animation in animations.items()}
        self.animation = None
        self.set_animation('touch')
        self.position = pos


    def touched_by(self, character):
        super(LifePotionSmall, self).touched_by(character)

        dis = self.distance_to(character)
        if not self.taken and dis < 20:
            if 'hit' in character.animation_name:
                character.life = min(character.max_life, character.life + 3)
                self.kill()
                self.taken = True


