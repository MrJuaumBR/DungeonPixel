from data.config import *
from data.screens.play import *
from data.screens.settings import *
import os

class GameState:
    Slider_VolumePercentage = 0
    Slider_VolumePos = 0

class GameConfig:
    dictionary: dict
    last_write_time: float
    game_title_x: int
    game_title_y: int
    play_button_x: int
    play_button_y: int
    settings_button_x: int
    settings_button_y: int
    quit_button_x: int
    quit_button_y: int

    settings_x = 0
    settings_y = 0
    volume_x = 0
    volume_y = 0
    slider_x = 0
    slider_y = 0
    slider_circle_x = 0
    slider_circle_y = 0
    screen_size_x = 0
    screen_size_y = 0
    screen_size_left_arrow_x = 0
    screen_size_left_arrow_y = 0
    window_dimension_x = 0
    window_dimension_y = 0
    screen_size_right_arrow_x = 0
    screen_size_right_arrow_y = 0
    fps_x = 0
    fps_y = 0
    fps_left_arrow_x = 0
    fps_left_arrow_y = 0
    fps_number_x = 0
    fps_number_y = 0
    fps_right_arrow_x = 0
    fps_right_arrow_y = 0
    show_fps_x = 0
    show_fps_y = 0
    show_fps_checkbox_x = 0
    show_fps_checkbox_y = 0




def main():
    print(os.getcwd())
    game_state = GameState()
    game_state.Slider_VolumePercentage = CONFIG['VOLUME'] or 0
    game_state.Slider_VolumePos = ((64+250)*game_state.Slider_VolumePercentage)*GAME_SCREEN_RATIO[0]

    game_config = GameConfig
    pme.hot_load_game_config(game_config)
    game_config.last_write_time = os.path.getmtime("./data/config.ini")
    while True:
        current_config_last_write_time = os.path.getmtime("./data/config.ini")
        if game_config.last_write_time != current_config_last_write_time:
            pme.hot_load_game_config(game_config)
            game_config.last_write_time = os.path.getmtime("./data/config.ini")

        # Game Title
        #pme.draw_text(32*GAME_SCREEN_RATIO[0],32*GAME_SCREEN_RATIO[1],f'{GAME_TITLE}', FONT_ANDALIA52, COLOR_WHITE)
        pme.draw_text(game_config.game_title_x, game_config.game_title_y, f'{GAME_TITLE}', FONT_ANDALIA52, COLOR_WHITE)

        # Game Main Menu Buttons
        if pme.draw_button(game_config.play_button_x,game_config.play_button_y,'Play', FONT_DOGICAPIXEL36, COLOR_WHITE, COLOR_BLACK):
            play_select_character()
        if pme.draw_button(game_config.settings_button_x,game_config.settings_button_y,'Settings', FONT_DOGICAPIXEL36, COLOR_WHITE, COLOR_BLACK):
            cfg = settings(game_state, game_config)
            # Returned From Settings
            # Save
            CONFIG['VOLUME'] = cfg[0]
            CONFIG['SCREEN_SIZE'] = cfg[1]
            CONFIG['FPS'] = cfg[2]
            CONFIG['SHOW_FPS'] = cfg[3]
            
            db.update_value(table_name='config',column_name='data',id=0,value=CONFIG)
            db.save()
        if pme.draw_button(game_config.quit_button_x,game_config.quit_button_y,'Quit', FONT_DOGICAPIXEL36, COLOR_LIGHTRED, COLOR_BLACK):
            pme.destroy_window()
        

        for ev in pme.get_events():
            if ev.type == QUIT:
                pme.destroy_window()
                exit()
            if ev.type == KEYDOWN:
                if ev.key == K_ESCAPE:
                    pme.destroy_window()
        ShowFPS()
        pme.update()
        pme.screen.fill(COLOR_BLACK)
        GAME_CLOCK.tick(GAME_FPS)

if __name__ == '__main__':
    main()