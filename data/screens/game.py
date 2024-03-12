from ..config import *
from ..src.camera import *
from ..src.save import *
from .gameSrc.tiles import *
from .gameSrc.mapReader import read_map, convert_map_code, get_map_size

def game(save:Save):
    run = True

    player:G_Player = save.plr

    Camera:CameraGroup = CameraGroup(player=player)

    map:dict = read_map('./data/screens/gameSrc/map')
    map_tiles = convert_map_code(map)
    map_size = get_map_size(map)
    
    print(map_size)
    print(map_tiles)

    # Load Map
    for y,line in enumerate(map_tiles):
        for x,tile in enumerate(line):
            if callable(tile):
                Camera.add(tile(pos=((x+1)*32,(y+1)*32)))

    while run:
        for ev in pme.get_events():
            if ev.type == QUIT: pme.quit()
            elif ev.type == KEYDOWN:
                if ev.key == K_ESCAPE: run = False

        ShowFPS()
        Camera.update()
        pme.update()
        pme.screen.fill(COLOR_BLACK)
        Camera.draw()
        