from ..game import *

class TileBase(pyg.sprite.Sprite):
    name = 'TileBase'
    layer = 1

    can_collide = True
    can_action = False

    type = 'tile'

    offset_pos:pyg.math.Vector2
    def __init__(self, image:pyg.Surface, pos:tuple) -> None:
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(topleft=pos)