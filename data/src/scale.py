
# Default Sizes
SIZE_SCREEN_WIDTH = 800
SIZE_SCREEN_HEIGHT = 600

# Scale Rate = CURRENT_WIDTH/DEFAULT_WIDTH, CURRENT_HEIGHT/DEFAULT_HEIGHT

def ScaleRatio(WIDTH:int,HEIGHT:int) -> tuple[float,float]:
    return WIDTH / SIZE_SCREEN_WIDTH, HEIGHT / SIZE_SCREEN_HEIGHT

def FPS2Seconds(FPS:int) -> float:
    return 1 / FPS
