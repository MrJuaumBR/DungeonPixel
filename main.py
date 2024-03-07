from data.config import *
from data.screens.play import *
from data.screens.settings import *
from enum import Enum
import time

class GameMode(Enum):
    INVALID = 0
    MAIN_MENU = 0x1
    PLAYING = 0x2
    SETTINGS = 0x4 
    CHARACTER_CREATION = 0x8
    LOAD_CHARACTER = 0x10

class CreateSaveState():
    difficulty_index = 0

def main():    
    game_mode = GameMode.MAIN_MENU.value
    is_running = True
    saves =  0
    create_save_state = CreateSaveState()
    while is_running:
        for ev in pme.get_events():
            if ev.type == QUIT:
                pme.quit()
                exit()
            if ev.type == KEYDOWN:
                if ev.key == K_ESCAPE:
                    if game_mode == GameMode.MAIN_MENU.value:
                        pme.quit()
                    else:
                        game_mode = GameMode.MAIN_MENU.value

        if game_mode & GameMode.MAIN_MENU.value:
            pme.screen.fill(COLOR_BLACK)

            # Game Title
            pme.draw_text(32*GAME_SCREEN_RATIO[0],32*GAME_SCREEN_RATIO[1],f'{GAME_TITLE}', FONT_ANDALIA52, COLOR_WHITE)

            # Game Main Menu Buttons
            if pme.draw_button(64*GAME_SCREEN_RATIO[0],128*GAME_SCREEN_RATIO[1],'Play', FONT_DOGICAPIXEL36, COLOR_WHITE, COLOR_BLACK):
                game_mode = GameMode.LOAD_CHARACTER.value
            elif pme.draw_button(64*GAME_SCREEN_RATIO[0],192*GAME_SCREEN_RATIO[1],'Settings', FONT_DOGICAPIXEL36, COLOR_WHITE, COLOR_BLACK):
                game_mode = GameMode.SETTINGS.value
            elif pme.draw_button(64*GAME_SCREEN_RATIO[0],256*GAME_SCREEN_RATIO[1],'Quit', FONT_DOGICAPIXEL36, COLOR_LIGHTRED, COLOR_BLACK):
                is_running = False
                        
            ShowFPS()
            pme.update()
            GAME_CLOCK.tick(GAME_FPS)
        elif game_mode & GameMode.LOAD_CHARACTER.value:
            run = True
            SaveIndex = 0
            SaveIndex_InList = 0

            Save_X = [64*GAME_SCREEN_RATIO[0],202*GAME_SCREEN_RATIO[0],340*GAME_SCREEN_RATIO[0],64*GAME_SCREEN_RATIO[0],202*GAME_SCREEN_RATIO[0],340*GAME_SCREEN_RATIO[0]]
            Save_Y = 128*GAME_SCREEN_RATIO[1]

            saves = db.get_all('saves')
            def PreLoadSaves(saves:list[dict]):
                pre_loaded_saves = []
                for i,save in enumerate(saves):
                    try:
                        s = Save(0,0)
                        s.load(save['data'])
                        pre_loaded_saves.append(s)
                    except Exception as e:
                        print(e)

                return pre_loaded_saves
            saves = PreLoadSaves(saves)
                    
            pme.screen.fill(COLOR_BLACK)
            
            # Screen Title
            pme.draw_text(32*GAME_SCREEN_RATIO[0],32*GAME_SCREEN_RATIO[1],'Save Select', FONT_ANDALIA52, COLOR_WHITE)
            Buttons = []
            # Saves
            for i in range(GAME_MAX_SAVES): # I Start as 0, i = 0
                if i > (GAME_MAX_SAVES//2)-1: # If i > 3-1, i >= 3
                    Save_Y = 256*GAME_SCREEN_RATIO[1] # Second Line
                else:
                    Save_Y = 128*GAME_SCREEN_RATIO[1] # First Line
                b = pme.draw_rect(Save_X[i],Save_Y,COLOR_DARKGRAY,(128*GAME_SCREEN_RATIO[0],110*GAME_SCREEN_RATIO[1])) # Draw Background
                if len(saves)-1 >= i: # If there's a save at index i
                    pme.draw_text(Save_X[i],Save_Y,f'{int(saves[i].SaveIndex)+1}', FONT_DOGICAPIXEL18, COLOR_WHITE)

                    d = pme.draw_button(Save_X[i]+80*GAME_SCREEN_RATIO[0],Save_Y,'Delete', FONT_DOGICAPIXEL10, COLOR_LIGHTRED, COLOR_BLACK)

                    if pme.is_mouse_hover(b):
                        if pme.mouse_pressed(0):
                            b = True
                        else:
                            b = False
                    else:
                        b = False

                    Buttons.append((i,saves[i].SaveIndex,b,d)) # Index/Id: int, Select Button: bool, Delete Button: bool

                # if i > GAME_MAX_SAVES//2:
                #     Save_Y = 256*GAME_SCREEN_RATIO[1]
                # else:
                #     Save_Y = 128*GAME_SCREEN_RATIO[1]
                # pme.draw_rect(Save_X[i],Save_Y,COLOR_DARKGRAY,(100*GAME_SCREEN_RATIO[0],64*GAME_SCREEN_RATIO[1]))
                # if len(saves)-1 >= i:
                #     pme.draw_text(Save_X[i],Save_Y,f'{saves[i].SaveIndex}', FONT_DOGICAPIXEL18, COLOR_WHITE)

            # Buttons
            Color_Create = lambda: COLOR_LIME if len(saves) < GAME_MAX_SAVES else COLOR_LIGHTRED
            if pme.draw_button(64*GAME_SCREEN_RATIO[0],550*GAME_SCREEN_RATIO[1],'Create New', FONT_DOGICAPIXEL28, Color_Create(), COLOR_BLACK):
                # Create New Save
                if len(saves) < GAME_MAX_SAVES:
                    game_mode = GameMode.CHARACTER_CREATION.value
            elif pme.draw_button(350*GAME_SCREEN_RATIO[0],550*GAME_SCREEN_RATIO[1],f'Load: {SaveIndex+1}', FONT_DOGICAPIXEL28, COLOR_LIME, COLOR_DARKGRAY):
                # Load Save
                if len(saves) > 0:            
                    game_mode = GameMode.PLAYING.value
        elif game_mode & GameMode.CHARACTER_CREATION.value:
            if len(saves) < GAME_MAX_SAVES:
                if create_save(create_save_state):
                    time.sleep(1.0/10.0) #@TODO: Cheap hack
                    game_mode = GameMode.LOAD_CHARACTER.value
            saves = db.get_all(table_name='saves')
            saves = PreLoadSaves(saves)            
        elif game_mode & GameMode.PLAYING.value:            
            if len(saves) > 0:            
                save:Save = saves[SaveIndex_InList]

            from data.screens.game import game
            game(save)
        elif game_mode & GameMode.SETTINGS.value:
            cfg = settings()
            # Returned From Settings
            # Save
            CONFIG['VOLUME'] = cfg[0]
            CONFIG['SCREEN_SIZE'] = cfg[1]
            CONFIG['FPS'] = cfg[2]
            CONFIG['SHOW_FPS'] = cfg[3]
            
            db.update_value(table_name='config',column_name='data',id=0,value=CONFIG)
            db.save()
        else:
            assert(0, "Unreachable code")

        pme.update()
        GAME_CLOCK.tick(GAME_FPS)

    pme.quit()

if __name__ == '__main__':
    main()