from ..config import *
from ..src.camera import *
from ..src.save import *

def game(save:Save):
    run = True

    player:G_Player = save.player

    Camera = CameraGroup(player=player)
    """
    while run:
        for ev in pme.get_events():
            if ev.type == QUIT: pme.quit()
            elif ev.type == KEYDOWN:
                if ev.key == K_ESCAPE: run = False
    """
    pme.screen.fill(COLOR_BLACK)
    Camera.update()        
    #pme.update()    
    Camera.draw()
    ShowFPS()
        