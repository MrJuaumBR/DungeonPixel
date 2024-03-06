from data.config import *
from data.screens.play import *
from data.screens.settings import *



def main():
    while True:
        # Game Title
        pme.draw_text(32*GAME_SCREEN_RATIO[0],32*GAME_SCREEN_RATIO[1],f'{GAME_TITLE}', FONT_ANDALIA52, COLOR_WHITE)

        # Game Main Menu Buttons
        if pme.draw_button(64*GAME_SCREEN_RATIO[0],128*GAME_SCREEN_RATIO[1],'Play', FONT_DOGICAPIXEL36, COLOR_WHITE, COLOR_BLACK):
            play_select_character()
        if pme.draw_button(64*GAME_SCREEN_RATIO[0],192*GAME_SCREEN_RATIO[1],'Settings', FONT_DOGICAPIXEL36, COLOR_WHITE, COLOR_BLACK):
            cfg = settings()
            # Returned From Settings
            # Save
            CONFIG['VOLUME'] = cfg[0]
            CONFIG['SCREEN_SIZE'] = cfg[1]
            CONFIG['FPS'] = cfg[2]
            CONFIG['SHOW_FPS'] = cfg[3]
            
            db.update_value(table_name='config',column_name='data',id=0,value=CONFIG)
            db.save()
        if pme.draw_button(64*GAME_SCREEN_RATIO[0],256*GAME_SCREEN_RATIO[1],'Quit', FONT_DOGICAPIXEL36, COLOR_LIGHTRED, COLOR_BLACK):
            pme.quit()
        

        for ev in pme.get_events():
            if ev.type == QUIT:
                pme.quit()
                exit()
            if ev.type == KEYDOWN:
                if ev.key == K_ESCAPE:
                    pme.quit()
        ShowFPS()
        pme.update()
        pme.screen.fill(COLOR_BLACK)
        GAME_CLOCK.tick(GAME_FPS)

if __name__ == '__main__':
    main()