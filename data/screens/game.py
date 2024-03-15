from ..config import *
from ..src.camera import *
from ..src.save import *
from .gameSrc.tiles import *
from .gameSrc.mapReader import read_map, convert_map_code, get_map_size

def map_hotload(map_last_write_time:float,map_path:str,Camera:CameraGroup) -> float:
    # here we get the current last write time (it can be either new or the same as before) of the map file to later compare against last write time (old)
    map_current_last_write_time = os.path.getmtime(map_path)
    # this tells us if the file has changed on disk
    if map_last_write_time != map_current_last_write_time: 
        map:dict = read_map(map_path)
        map_tiles = convert_map_code(map)
        map_size = get_map_size(map)
        
        # loop and remove all the sprites but not the player because he is not in the map
        for sprite in Camera.sprites():
            if sprite is not Camera.player:
                Camera.remove(sprite)

        # Load Map
        for y,line in enumerate(map_tiles):
            for x,tile in enumerate(line):
                if callable(tile):
                    Camera.add(tile(pos=((x+1)*32,(y+1)*32)))

        map_last_write_time = os.path.getmtime(map_path) # here we update last write time of the map file because it was just edited in disk. we update stuff because we need to remember for the next iteration, otherwise it will trigger this if statement always, in this case
        return map_last_write_time
    else:
        return map_last_write_time

def game(save:Save):
    run = True

    player:G_Player = save.plr

    Camera:CameraGroup = CameraGroup(player=player)

    # change the file name to "map.txt" because vscode is going nuts thinking it is a javascript file. this var is for stopping copy pasta everywhere
    map_path = "./data/screens/gameSrc/map.txt" 
    # every file has info about it and we are going to need to know what was the last write to this file to later compare againt another one. its for the hotload of the map
    map_last_write_time = os.path.getmtime(map_path) 
    map:dict = read_map(map_path)
    map_tiles = convert_map_code(map)
    map_size = get_map_size(map)

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

        
        map_last_write_time = map_hotload(map_last_write_time,map_path,Camera)

        ShowFPS()
        Camera.update()
        pme.update()
        pme.screen.fill(COLOR_BLACK)
        Camera.draw()
        