"""
Imports
"""

from .src.engine import *
from .src.auto_installer import AutoInstaller
from .src.scale import Scale
from random import randint, choice
from math import sqrt
print('[Config] Imported...')

# Auto Installer Setup
AUI = AutoInstaller()

    # Try to install all requirements
try:
    AUI.InstallAll()
    print('[Config - Auto Installer] All Requirements Installed.')
except Exception as e:
    print(f'[Config - Auto Installer] {e}')

# Game Config
from .src.database import (pyd,db)
from .src.database import CreateTables as db_createTables
print('[Config - Database] Imported...')

# Init database
CONFIG_DEFAULT = {
    'FPS': 0,
    'VOLUME':0.5,
    'SCREEN_SIZE':0,
    'SHOW_FPS':False,
    'FULLSCREEN':False
}

db_createTables() # Try to create Database Tables

if len(db.get_all('config')) == 0: # Has no Config
    # If Has no Config Data, Then Create.
    db.add_values('config',columns=['data'],values=[CONFIG_DEFAULT])
    db.save()
    print('Config Added.')

# Get Config From Database
    
CONFIG:dict = db.get_value('config','data',0)

GAME_RES_LIST:list[tuple[int,int],] = [(640,480),(800,600),(1024,768),(1920,1080)]
GAME_FPS_LIST:list[int,] = [30,60,90,120]

CFG_RES:tuple[int,int] = GAME_RES_LIST[CONFIG['SCREEN_SIZE']]
GAME_FPS:int = GAME_FPS_LIST[CONFIG['FPS']]
print(f'[Config] Loaded Data...')

GAME_TITLE = "Dungeon Pixel"
GAME_VERSION = '0.0.4'
print('[Config] Metadata Loaded...')

scale = Scale(GAME_FPS)
GAME_SCREEN_WIDTH,GAME_SCREEN_HEIGHT = CFG_RES
GAME_SCREEN_RATIO = scale.ScaleRatio(GAME_SCREEN_WIDTH,GAME_SCREEN_HEIGHT)
GAME_SCREEN_FLAGS = SCALED|FULLSCREEN if CONFIG['FULLSCREEN'] else SCALED
print('[Config] Screen Resources Loaded...')

GAME_MAX_SAVES = 6
GAME_PLAYER_ANIMATE_FRAME_SKIP = 0.35

GAME_MAP_SIZE = (4096,4096) # Width, Height in Pixels(Tile Size * 128)
GAME_MAP_SIZE_IN_TILES = (GAME_MAP_SIZE[0]//32,GAME_MAP_SIZE[1]//32)
print('[Config] Map & Saves Resources Loaded...')

GAME_CAMERA_MIN_ZOOM = 0.8
GAME_CAMERA_MAX_ZOOM = 1.8
print('[Config] Camera Resources(Zoom) Loaded...')

# Init Engine
pme = Engine()
print('[Config - Engine] Object Created...')
SCREEN = pme.create_screen(GAME_SCREEN_WIDTH, GAME_SCREEN_HEIGHT, GAME_SCREEN_FLAGS)
print('[Config - Engine] Screen Created...')
pme.screen_set_title(GAME_TITLE)
print('[Config - Engine] Started...')

# Resources that requires the Engine Initlization
GAME_CLOCK = pyg.time.Clock()
print('[Config - Clock] Started...')

# Paths
PATH_DATA = './data/'
PATH_ASSETS = './data/assets/'
PATH_SRC = './data/src/'
PATH_AUDIOS = PATH_ASSETS + 'audios/'
PATH_TEXTURES = PATH_ASSETS + 'textures/'
PATH_FONTS = PATH_ASSETS + 'fonts/'

# Fonts Path
PATH_FONT_ANDALIA = PATH_FONTS + 'Andalia.ttf'
PATH_FONT_DOGICAPIXEL = PATH_FONTS + 'dogicapixel.ttf'

# Create Fonts
pme.create_font('Arial', 24)
FONT_ANDALIA52,_ = pme.create_font2(PATH_FONT_ANDALIA, int(52*GAME_SCREEN_RATIO))
FONT_DOGICAPIXEL18,_ = pme.create_font2(PATH_FONT_DOGICAPIXEL, int(18*GAME_SCREEN_RATIO))
FONT_DOGICAPIXEL28,_ = pme.create_font2(PATH_FONT_DOGICAPIXEL, int(28*GAME_SCREEN_RATIO))
FONT_DOGICAPIXEL22,_ = pme.create_font2(PATH_FONT_DOGICAPIXEL, int(22*GAME_SCREEN_RATIO))
FONT_DOGICAPIXEL36,_ = pme.create_font2(PATH_FONT_DOGICAPIXEL, int(36*GAME_SCREEN_RATIO))
FONT_DOGICAPIXEL12,_ = pme.create_font2(PATH_FONT_DOGICAPIXEL, int(12*GAME_SCREEN_RATIO))
FONT_DOGICAPIXEL10,_ = pme.create_font2(PATH_FONT_DOGICAPIXEL, int(10*GAME_SCREEN_RATIO))

# Sounds Load

# Rise 1 ~ 7
SOUND_Rise01 = pyg.mixer.Sound(PATH_AUDIOS + 'Rise01.wav')
SOUND_Rise02 = pyg.mixer.Sound(PATH_AUDIOS + 'Rise02.wav')
SOUND_Rise03 = pyg.mixer.Sound(PATH_AUDIOS + 'Rise03.wav')
SOUND_Rise04 = pyg.mixer.Sound(PATH_AUDIOS + 'Rise04.wav')
SOUND_Rise05 = pyg.mixer.Sound(PATH_AUDIOS + 'Rise05.wav')
SOUND_Rise06 = pyg.mixer.Sound(PATH_AUDIOS + 'Rise06.wav')
SOUND_Rise07 = pyg.mixer.Sound(PATH_AUDIOS + 'Rise07.wav')
# FX 1 ~ 2
SOUND_FX01 = pyg.mixer.Sound(PATH_AUDIOS + 'FX01.wav')
SOUND_FX02 = pyg.mixer.Sound(PATH_AUDIOS + 'FX02.wav')
# Upper 1
SOUND_Upper01 = pyg.mixer.Sound(PATH_AUDIOS + 'Upper01.wav')
# Coin 1
SOUND_Coin01 = pyg.mixer.Sound(PATH_AUDIOS + 'Coin01.wav')
# Downer 1
SOUND_Downer01 = pyg.mixer.Sound(PATH_AUDIOS + 'Downer01.wav')
# Alarm
SOUND_Alarm = pyg.mixer.Sound(PATH_AUDIOS + 'Alarm.wav')
# Click 1
SOUND_Click01 = pyg.mixer.Sound(PATH_AUDIOS + 'Click01.wav')
# Switch 1
SOUND_Switch01 = pyg.mixer.Sound(PATH_AUDIOS + 'Switch01.wav')

# Set Engine Sound Button
pme.button_click_sound= SOUND_Click01
pme.switch_click_sound = SOUND_Switch01

# Colors
COLOR_WHITE = (255, 255, 255)
COLOR_BLACK = (0, 0, 0)
COLOR_RED = (255, 0, 0)
COLOR_BLUE = (0, 0, 255)
COLOR_GREEN = (0, 255, 0)
COLOR_LIME = (150, 255, 150)
COLOR_YELLOW = (255, 255, 0)
COLOR_DARKGRAY = (40, 40, 40)
COLOR_LIGHTRED = (255, 150, 150)

# Misc Functions

GetMultiplierToUpOrDown = lambda x: 1 if x > 0 else -1

def ShowFPS():
    if CONFIG['SHOW_FPS']:
        color = COLOR_WHITE
        C_FPS = int(GAME_CLOCK.get_fps())

        if C_FPS >= GAME_FPS or C_FPS >= GAME_FPS*0.8:
            color = COLOR_LIME
        elif C_FPS >= GAME_FPS*0.6 and C_FPS <= GAME_FPS*0.8:
            color = COLOR_GREEN
        elif C_FPS <= GAME_FPS*0.6 and C_FPS >= GAME_FPS*0.4:
            color = COLOR_YELLOW
        else:
            color = COLOR_RED
        
        pme.draw_text(750*GAME_SCREEN_RATIO,10*GAME_SCREEN_RATIO,f'{C_FPS}', FONT_DOGICAPIXEL12, color)
"""
End of Config file
"""
print('[Config] Loaded')