from ..config import *
from ..src.camera import *
from ..src.save import *
from .gameSrc.tiles import *

def game(save:Save):
    run = True

    player:G_Player = save.plr

    Camera = CameraGroup(player=player)

    Tile = TileBase(pos=(64,64))
    Camera.add(Tile)

    while run:
        for ev in pme.get_events():
            if ev.type == QUIT: pme.destroy_window()
            elif ev.type == KEYDOWN:
                if ev.key == K_ESCAPE: run = False

        ShowFPS()
        Camera.update()
        pme.update()
        pme.screen.fill(COLOR_BLACK)
        Camera.draw()
        