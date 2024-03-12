from ..config import *

def settings(game_state, game_config):
    run = True

    #Slider_VolumePercentage = CONFIG['VOLUME'] or 0
    #Slider_VolumePos = ((64+250)*game_state.Slider_VolumePercentage)*GAME_SCREEN_RATIO[0]

    Select_ScreenSizeIndex = CONFIG['SCREEN_SIZE'] or 0
    Select_FPSIndex = CONFIG['FPS'] or 0
    CheckBx_SHOW_FPS = CONFIG['SHOW_FPS'] or False
    while run:
        current_config_last_write_time = os.path.getmtime("./data/config.ini")
        if game_config.last_write_time != current_config_last_write_time:
            pme.hot_load_game_config(game_config)
            game_config.last_write_time = os.path.getmtime("./data/config.ini")

        # Screen Title
        pme.draw_text(game_config.settings_x,game_config.settings_y,'Settings', FONT_ANDALIA52, COLOR_WHITE)

        # Settings Buttons
            # volume
        volume_surface = pme.draw_text(game_config.volume_x,game_config.volume_y,f'Volume: {int(game_state.Slider_VolumePercentage*100)}', FONT_DOGICAPIXEL28, COLOR_WHITE)
        #Slider_VolumePos, Slider_VolumePercentage = pme.draw_slider2(64*GAME_SCREEN_RATIO[0],128*GAME_SCREEN_RATIO[1],250*GAME_SCREEN_RATIO[0],[(35,35,35),(100,190,125),(200,200,200)],Slider_VolumePos,detail=True)
        slider_width = 193 #volume_surface.width + (volume_surface.width // 8)        
        game_state.Slider_VolumePos, game_state.Slider_VolumePercentage = pme.draw_slider(game_config.slider_x, game_config.slider_y, slider_width, [(35,35,35),(100,190,125),(200,200,200)],game_state.Slider_VolumePos,game_state.Slider_VolumePercentage, detail=True)

            # Screen size
        pme.draw_text(game_config.screen_size_x,game_config.screen_size_y,f'Screen Size:', FONT_DOGICAPIXEL28, COLOR_WHITE)
        Select_ScreenSizeIndex = pme.draw_select(game_config.window_dimension_x,game_config.window_dimension_y,FONT_DOGICAPIXEL28,[(35,35,35),(100,190,125),(200,200,200)],GAME_RES_LIST,Select_ScreenSizeIndex)

            # FPS
        pme.draw_text(game_config.fps_x,game_config.fps_y,f'FPS:', FONT_DOGICAPIXEL28, COLOR_WHITE)
        Select_FPSIndex = pme.draw_select(game_config.show_fps_checkbox_x,game_config.show_fps_checkbox_y,FONT_DOGICAPIXEL28,[(35,35,35),(100,190,125),(200,200,200)],GAME_FPS_LIST,Select_FPSIndex)

            # SHOW_FPS
        CheckBx_SHOW_FPS = pme.draw_checkbox(game_config.show_fps_x,game_config.show_fps_y,FONT_DOGICAPIXEL18,'Show Fps',CheckBx_SHOW_FPS,[(35,35,35),(100,190,125),(200,200,200)])

        
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