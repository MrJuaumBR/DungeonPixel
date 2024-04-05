from ..config import *
from ..src.save import Player_Sprite_Frames # Get player animations

Tips=[
    'Hello, World!',
    'A Python Game.',
    'Made with PyGame.',
    'Try killing enemies to get xp',
    'Leveling up will give cards for you...'
]

def loadscreen(to:object = None,duration_extra:int=360,*args) -> None:
    """
    Load Screen, for Loading &nbsp;

    Parameters:
        to (object): The screen to load to, when complete, call this
        duration_extra (int): The extra duration in FPS
    Returns:
        None
    """
    if to and callable(to):
        run = True

        p_frames = Player_Sprite_Frames['walk']['right']
        P_sprite_frame = 0

        curr_tip = choice(Tips)
        change_tip_counter = duration_extra//4
        duration = duration_extra

        load_bar_green = 100
        while run:
            P_sprite_frame += 0.1
            if P_sprite_frame > len(p_frames):
                P_sprite_frame = 0
            percentage = round(duration/duration_extra*100)
            reverse_percentage = 100-percentage
            pme.draw_text(32*GAME_SCREEN_RATIO,32*GAME_SCREEN_RATIO,f'Loading...', FONT_DOGICAPIXEL36, COLOR_WHITE)
            pme.draw_text(32*GAME_SCREEN_RATIO,72*GAME_SCREEN_RATIO,f'{curr_tip}', FONT_DOGICAPIXEL22, COLOR_WHITE)
            pme.draw_bar(16*GAME_SCREEN_RATIO,536*GAME_SCREEN_RATIO, (GAME_SCREEN_WIDTH-32, 40*GAME_SCREEN_RATIO), [(90, 80, 65), (100, (255 if load_bar_green > 255 else load_bar_green), 100), (255,250,250), ((255,255,255) if load_bar_green < 160 else (90,90,90))], reverse_percentage, 100,text_font=FONT_DOGICAPIXEL12, text=f'{reverse_percentage}%', border_thickness=3)
            # Player Animation, Follow Bar Percentage in x
            # Min = 16, Max = 800-32= 768
            # Calculate Position X Using Percentage
            # X_position = (Min * GAME_SCREEN_RATIO) + ((percentage/100) * ((Min*GAME_SCREEN_RATIO) - (Max*GAME_SCREEN_RATIO))) # percentage in this case need to be float.(this is why divide by 100)
            x_position = 16*GAME_SCREEN_RATIO + ((reverse_percentage/100) * ((768*GAME_SCREEN_RATIO) - (16*GAME_SCREEN_RATIO)))
            pme.screen.blit(pyg.transform.scale(p_frames[int(P_sprite_frame)],(64*GAME_SCREEN_RATIO,64*GAME_SCREEN_RATIO)),(x_position,472*GAME_SCREEN_RATIO))
            load_bar_green += 1 % duration
            ShowFPS()
            pme.update()
            pme.screen.fill(COLOR_BLACK)
            change_tip_counter -= 1
            if change_tip_counter <= 0:
                curr_tip = choice(Tips)
                change_tip_counter = duration_extra//4
            duration -=1
            if duration <= 0:
                run = False

        to(*args)
    else:
        print('No Screen to load to')