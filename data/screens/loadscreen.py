from ..config import *

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

        curr_tip = choice(Tips)
        change_tip_counter = duration_extra//4
        duration = duration_extra
        while run:
            pme.draw_text(32*GAME_SCREEN_RATIO[0],32*GAME_SCREEN_RATIO[1],f'Loading...', FONT_DOGICAPIXEL36, COLOR_WHITE)
            pme.draw_text(32*GAME_SCREEN_RATIO[0],72*GAME_SCREEN_RATIO[1],f'{curr_tip}', FONT_DOGICAPIXEL22, COLOR_WHITE)
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