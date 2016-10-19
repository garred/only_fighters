from items import Item, load_animations


animations = load_animations('data/items/potions/life_small/')


class LifePotionSmall(Item):

    def touched_by(self, character):
        if character.life != character.max_life:
            character.life = min(character.max_life, character.life + 3)
            self.kill()


