from ..config import *

def settings():
    run = True

    Slider_VolumePercentage = CONFIG['VOLUME'] or 0
    Slider_VolumePos = ((64+250)*Slider_VolumePercentage)*GAME_SCREEN_RATIO[0]

    Select_ScreenSizeIndex = CONFIG['SCREEN_SIZE'] or 0
    Select_FPSIndex = CONFIG['FPS'] or 0
    CheckBx_SHOW_FPS = CONFIG['SHOW_FPS'] or False
    while run:
        # Screen Title
        pme.draw_text(32*GAME_SCREEN_RATIO[0],32*GAME_SCREEN_RATIO[1],'Settings', FONT_ANDALIA52, COLOR_WHITE)

        # Settings Buttons
            # volume
        pme.draw_text(48*GAME_SCREEN_RATIO[0],96*GAME_SCREEN_RATIO[1],f'Volume: {int(Slider_VolumePercentage*100)}', FONT_DOGICAPIXEL28, COLOR_WHITE)
        Slider_VolumePos, Slider_VolumePercentage = pme.draw_slider(64*GAME_SCREEN_RATIO[0],128*GAME_SCREEN_RATIO[1],250*GAME_SCREEN_RATIO[0],[(35,35,35),(100,190,125),(200,200,200)],Slider_VolumePos,detail=True)

            # Screen size
        pme.draw_text(48*GAME_SCREEN_RATIO[0],192*GAME_SCREEN_RATIO[1],f'Screen Size:', FONT_DOGICAPIXEL28, COLOR_WHITE)
        Select_ScreenSizeIndex = pme.draw_select(200*GAME_SCREEN_RATIO[0],224*GAME_SCREEN_RATIO[1],FONT_DOGICAPIXEL28,[(35,35,35),(100,190,125),(200,200,200)],GAME_RES_LIST,Select_ScreenSizeIndex)

            # FPS
        pme.draw_text(48*GAME_SCREEN_RATIO[0],288*GAME_SCREEN_RATIO[1],f'FPS:', FONT_DOGICAPIXEL28, COLOR_WHITE)
        Select_FPSIndex = pme.draw_select(64*GAME_SCREEN_RATIO[0],320*GAME_SCREEN_RATIO[1],FONT_DOGICAPIXEL28,[(35,35,35),(100,190,125),(200,200,200)],GAME_FPS_LIST,Select_FPSIndex)

            # SHOW_FPS
        CheckBx_SHOW_FPS = pme.draw_checkbox(64*GAME_SCREEN_RATIO[0],416*GAME_SCREEN_RATIO[1],FONT_DOGICAPIXEL18,'Show Fps',CheckBx_SHOW_FPS,[(35,35,35),(100,190,125),(200,200,200)])

        
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
    
    return Slider_VolumePercentage,Select_ScreenSizeIndex, Select_FPSIndex, CheckBx_SHOW_FPS