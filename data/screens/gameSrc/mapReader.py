import os
from .tiles import *

tile_dict:dict = {
    'baseTile':{
        'tile':TileBase,
        'code':'?'
    },
    'wall':{
        'tile':Wall,
        'code':'W'
    }
}

def get_tile_code(tile_code:str) -> str:
    for key in tile_dict.keys():
        if tile_dict[key]['code'] == tile_code:
           return key 
        
    return None

def read_map(path:str) -> dict:
    # Line 1 = CONFIG ( Literally This )
    # Line 2 = Map Name ( String )
    # 3 = Map Code ( Multiples Lines )
    lines = open(path,'r').readlines()

    MAP_NAME = lines[2]
    MAP_CODE = lines[3:]

    map:dict = {
        'name':MAP_NAME,
        'code':MAP_CODE,
    }

    return map

def convert_map_code(map_data:dict) -> list[list,]:
    map_tiles = []
    map_code = map_data['code']

    for line in map_code:
        line_tiles = []
        for tile in line:
            t = get_tile_code(tile)
            if t:
                line_tiles.append(tile_dict[t]['tile'])
            else:
                line_tiles.append('.')
                
        map_tiles.append(line_tiles)
    return map_tiles

def get_map_size(map:dict) -> tuple[int,int]:
    return len(map['code'][0]),len(map['code']) # X, Y