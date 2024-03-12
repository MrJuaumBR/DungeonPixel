from ...config import *
from ...src.save import player as G_Player

class TileBase(pyg.sprite.Sprite):
    name = 'TileBase'
    layer = 1

    can_collide = True
    can_action = False

    type = 'tile'

    offset_pos:pyg.math.Vector2 = pyg.math.Vector2()

    size:tuple[int,int] = (32,32)
    image:pyg.Surface
    def __init__(self, pos:tuple) -> None:
        super().__init__()
        self.image = pyg.Surface(self.size,pyg.SRCALPHA)
        self.image.fill((255,255,0,100))
        self.rect = self.image.get_rect(topleft=pos)
        

    def update(self,player:G_Player) -> None:
        pass

class Wall(TileBase):
    name = 'Wall'
    layer = 1

    can_collide = True
    can_action = False

    type = 'wall'

    offset_pos:pyg.math.Vector2 = pyg.math.Vector2()

    size:tuple[int,int] = (32,32)
    image:pyg.Surface
    def __init__(self, pos:tuple) -> None:
        super().__init__(pos)
        ss = spritesheet('./data/assets/textures/tiles.png')
        self.image = ss.image_at((0,0,32,32),-1)


    def update(self,player:G_Player) -> None:
        pass