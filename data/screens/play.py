from ..config import *
from ..src.save import *
import time

def play():
    pass

def play_select_character():#@TODO: Delete function?
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
            create_save()
            saves = db.get_all(table_name='saves')
            saves = PreLoadSaves(saves)
    elif pme.draw_button(350*GAME_SCREEN_RATIO[0],550*GAME_SCREEN_RATIO[1],f'Load: {SaveIndex+1}', FONT_DOGICAPIXEL28, COLOR_LIME, COLOR_DARKGRAY):
        # Load Save
        if len(saves) > 0:            
            save:Save = saves[SaveIndex_InList]

            from .game import game            
            game(save)

    for order,id, select, delete in Buttons:
        if select:
            SaveIndex = id
            SaveIndex_InList = order
        if delete:
            db.delete_values(table_name='saves',id=id,columns=['data'])
            db.save()
            saves = db.get_all(table_name='saves')
            saves = PreLoadSaves(saves)
            pyg.time.delay(250) # Delay to prevent accidental button presses
    """
    for ev in pme.get_events():
        if ev.type == QUIT:
            pme.quit()
        elif ev.type == KEYDOWN:
            if ev.key == K_ESCAPE:
                run = False
    """
    ShowFPS()
    pme.update()
    pme.screen.fill(COLOR_BLACK)
    GAME_CLOCK.tick(GAME_FPS)

def create_save(create_save_state):
    result = False

    DifficultyList = ['Easy','Normal','Hard']

    SavesList = db.get_all(table_name='saves')

    pme.screen.fill(COLOR_BLACK)

    pme.draw_text(32*GAME_SCREEN_RATIO[0],32*GAME_SCREEN_RATIO[1],'Create New Save', FONT_ANDALIA52, COLOR_WHITE)

    # Difficulty
    pme.draw_text(64*GAME_SCREEN_RATIO[0],128*GAME_SCREEN_RATIO[1],f'Difficulty: {DifficultyList[create_save_state.difficulty_index]}', FONT_DOGICAPIXEL28, COLOR_WHITE)
    create_save_state.difficulty_index = pme.draw_select(128*GAME_SCREEN_RATIO[0],192*GAME_SCREEN_RATIO[1],FONT_DOGICAPIXEL28,[(35,35,35),(100,190,125),(200,200,200)],DifficultyList,create_save_state.difficulty_index)

    if pme.draw_button(64*GAME_SCREEN_RATIO[0],550*GAME_SCREEN_RATIO[1],'Create', FONT_DOGICAPIXEL28, COLOR_LIME, COLOR_BLACK):
        # Create Save
        s = Save(len(SavesList),create_save_state.difficulty_index)
        s.save()
        create_save_state.difficulty_index = 0
        result = True
    """
    for ev in pme.get_events():
        if ev.type == QUIT:
            pme.quit()
        elif ev.type == KEYDOWN:
            if ev.key == K_ESCAPE:
                run = False

    """
    ShowFPS()    

    return result    