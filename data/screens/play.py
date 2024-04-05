from ..config import *
from ..src.save import *
from .loadscreen import loadscreen as loadingScr
from ..src.save import Player_Sprite_Frames # Get player animations

def play_select_character():
    run = True
    SaveIndex = -1
    SaveIndex_InList = 0

    p_sprite_frame = 0
    p_frames = Player_Sprite_Frames['idle']['down']

    Save_X = [96*GAME_SCREEN_RATIO,234*GAME_SCREEN_RATIO,372*GAME_SCREEN_RATIO,96*GAME_SCREEN_RATIO,234*GAME_SCREEN_RATIO,372*GAME_SCREEN_RATIO]
    Save_Y = 128*GAME_SCREEN_RATIO

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
    
    while run:
        # Screen Title
        pme.draw_text(32*GAME_SCREEN_RATIO,32*GAME_SCREEN_RATIO,'Save Select', FONT_ANDALIA52, COLOR_WHITE)
        p_sprite_frame += 0.1
        if p_sprite_frame >= len(p_frames):
            p_sprite_frame = 0
        pme.screen.blit(pyg.transform.scale(p_frames[int(p_sprite_frame)],(128*GAME_SCREEN_RATIO,128*GAME_SCREEN_RATIO)),(544*GAME_SCREEN_RATIO,132*GAME_SCREEN_RATIO))
        Buttons = []
        # Saves
        for i in range(GAME_MAX_SAVES): # I Start as 0, i = 0
            if i > (GAME_MAX_SAVES//2)-1: # If i > 3-1, i >= 3
                Save_Y = 256*GAME_SCREEN_RATIO # Second Line
            else:
                Save_Y = 128*GAME_SCREEN_RATIO # First Line
            b = pme.draw_rect(Save_X[i],Save_Y,COLOR_DARKGRAY,(128*GAME_SCREEN_RATIO,110*GAME_SCREEN_RATIO)) # Draw Background
            if len(saves)-1 >= i: # If there's a save at index i
                pme.draw_text(Save_X[i],Save_Y,f'{int(saves[i].SaveIndex)+1}', FONT_DOGICAPIXEL18, COLOR_WHITE)

                d = pme.draw_button(Save_X[i]+80*GAME_SCREEN_RATIO,Save_Y,'Delete', FONT_DOGICAPIXEL10, COLOR_LIGHTRED, COLOR_BLACK)

                if pme.is_mouse_hover(b):
                    if pme.mouse_pressed(0):
                        b = True
                    else:
                        b = False
                else:
                    b = False

                Buttons.append((i,saves[i].SaveIndex,b,d)) # Index/Id: int, Select Button: bool, Delete Button: bool

            # if i > GAME_MAX_SAVES//2:
            #     Save_Y = 256*GAME_SCREEN_RATIO
            # else:
            #     Save_Y = 128*GAME_SCREEN_RATIO
            # pme.draw_rect(Save_X[i],Save_Y,COLOR_DARKGRAY,(100*GAME_SCREEN_RATIO,64*GAME_SCREEN_RATIO))
            # if len(saves)-1 >= i:
            #     pme.draw_text(Save_X[i],Save_Y,f'{saves[i].SaveIndex}', FONT_DOGICAPIXEL18, COLOR_WHITE)

        # Buttons
        Color_Create = lambda: COLOR_LIME if len(saves) < GAME_MAX_SAVES else COLOR_LIGHTRED
        if pme.draw_button(64*GAME_SCREEN_RATIO,550*GAME_SCREEN_RATIO,'Create New', FONT_DOGICAPIXEL28, Color_Create(), COLOR_BLACK):
            # Create New Save
            if len(saves) < GAME_MAX_SAVES:
                create_save()
                saves = db.get_all(table_name='saves')
                saves = PreLoadSaves(saves)
        
        pme.draw_text(350*GAME_SCREEN_RATIO,575*GAME_SCREEN_RATIO,f'Save: {int(SaveIndex)+1 if SaveIndex != -1 else 'Select a Save.'}', FONT_DOGICAPIXEL18, COLOR_WHITE)
        if pme.draw_button(700*GAME_SCREEN_RATIO,550*GAME_SCREEN_RATIO,f'Play', FONT_DOGICAPIXEL28, (COLOR_LIME if SaveIndex != -1 else COLOR_LIGHTRED), COLOR_DARKGRAY):
            # Load Save
            if len(saves) > 0:
                # If Save is selected
                if SaveIndex != -1:
                    save:Save = saves[SaveIndex_InList]
                
                    from .game import game
                    loadingScr(game,scale.Seconds2FPS(randint(1,8)),save)

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

        for ev in pme.get_events():
            if ev.type == QUIT:
                pme.quit()
            elif ev.type == KEYDOWN:
                if ev.key == K_ESCAPE:
                    run = False
            elif ev.type == MOUSEBUTTONUP:
                if ev.button == 6:
                    run = False

        ShowFPS()
        pme.update()
        pme.screen.fill(COLOR_BLACK)
        GAME_CLOCK.tick(GAME_FPS)

def create_save():
    run = True

    DifficultyIndex = 0
    DifficultyList = ['Easy','Normal','Hard']

    DebugIndex = 0

    SavesList = db.get_all(table_name='saves')

    while run:
        pme.draw_text(32*GAME_SCREEN_RATIO,32*GAME_SCREEN_RATIO,'Create New Save', FONT_ANDALIA52, COLOR_WHITE)

        # Difficulty
        pme.draw_text(64*GAME_SCREEN_RATIO,128*GAME_SCREEN_RATIO,f'Difficulty: {DifficultyList[DifficultyIndex]}', FONT_DOGICAPIXEL28, COLOR_WHITE)
        DifficultyIndex = pme.draw_select(128*GAME_SCREEN_RATIO,192*GAME_SCREEN_RATIO,FONT_DOGICAPIXEL28,[(35,35,35),(100,190,125),(200,200,200)],DifficultyList,DifficultyIndex)

        # Is Debug
        pme.draw_text(64*GAME_SCREEN_RATIO,256*GAME_SCREEN_RATIO,f'Is Debug:', FONT_DOGICAPIXEL28, COLOR_WHITE)
        DebugIndex = pme.draw_select(128*GAME_SCREEN_RATIO,320*GAME_SCREEN_RATIO,FONT_DOGICAPIXEL28,[(35,35,35),(100,190,125),(200,200,200)],['No','Yes'],DebugIndex)

        if pme.draw_button(64*GAME_SCREEN_RATIO,550*GAME_SCREEN_RATIO,'Create', FONT_DOGICAPIXEL28, COLOR_LIME, COLOR_BLACK):
            # Create Save
            s = Save(len(SavesList),DifficultyIndex)
            s.plr.debug = DebugIndex or 0
            s.save()
            run = False
        for ev in pme.get_events():
            if ev.type == QUIT:
                pme.quit()
            elif ev.type == KEYDOWN:
                if ev.key == K_ESCAPE:
                    run = False
            elif ev.type == MOUSEBUTTONUP:
                if ev.button == 6:
                    run = False

        ShowFPS()
        pme.update()
        pme.screen.fill(COLOR_BLACK)
        GAME_CLOCK.tick(GAME_FPS)