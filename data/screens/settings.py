from ..config import *

def settings(game_state):
    run = True

    #Slider_VolumePercentage = CONFIG['VOLUME'] or 0
    #Slider_VolumePos = ((64+250)*game_state.Slider_VolumePercentage)*GAME_SCREEN_RATIO[0]

    Select_ScreenSizeIndex = CONFIG['SCREEN_SIZE'] or 0
    Select_FPSIndex = CONFIG['FPS'] or 0
    CheckBx_SHOW_FPS = CONFIG['SHOW_FPS'] or False
    while run:
        # Screen Title
        pme.draw_text(32*GAME_SCREEN_RATIO[0],32*GAME_SCREEN_RATIO[1],'Settings', FONT_ANDALIA52, COLOR_WHITE)

        # Settings Buttons
            # volume
        volume_surface = pme.draw_text(48*GAME_SCREEN_RATIO[0],96*GAME_SCREEN_RATIO[1],f'Volume: {int(game_state.Slider_VolumePercentage*100)}', FONT_DOGICAPIXEL28, COLOR_WHITE)
        #Slider_VolumePos, Slider_VolumePercentage = pme.draw_slider2(64*GAME_SCREEN_RATIO[0],128*GAME_SCREEN_RATIO[1],250*GAME_SCREEN_RATIO[0],[(35,35,35),(100,190,125),(200,200,200)],Slider_VolumePos,detail=True)
        slider_width = 193 #volume_surface.width + (volume_surface.width // 8)
        slider_padding_x = (slider_width - volume_surface.width) // 2
        slider_padding_y = 16
        slider_x = 18 #volume_surface.x - slider_padding_x
        slider_y = volume_surface.y + volume_surface.height + slider_padding_y
        #@NOTE: if slider_x and slider_width are base on volume_surface.width then the slider will be buggy because it will vary based on the text width which is dynamic
        game_state.Slider_VolumePos, game_state.Slider_VolumePercentage = pme.draw_slider(slider_x, slider_y, slider_width, [(35,35,35),(100,190,125),(200,200,200)],game_state.Slider_VolumePos,game_state.Slider_VolumePercentage, detail=True)

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
                pme.destroy_window()
            elif ev.type == KEYDOWN:
                if ev.key == K_ESCAPE:
                    run = False
        ShowFPS()
        pme.update()
        pme.screen.fill(COLOR_BLACK)
        GAME_CLOCK.tick(GAME_FPS)
    
    return game_state.Slider_VolumePercentage,Select_ScreenSizeIndex, Select_FPSIndex, CheckBx_SHOW_FPS