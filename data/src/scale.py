
# Default Sizes
SIZE_SCREEN_WIDTH = 800
SIZE_SCREEN_HEIGHT = 600

# Scale Rate = CURRENT_WIDTH/DEFAULT_WIDTH, CURRENT_HEIGHT/DEFAULT_HEIGHT

class Scale:
    FPS:int

    def __init__(self,FPS:dict) -> None:
        try:
            self.FPS = FPS
        except Exception as e:
            print(e)

    def ScaleRatio(self,WIDTH:int,HEIGHT:int) -> float:
        # Calculation
        # A = WIDTH / ORIGIN_WIDTH
        # B = HEIGHT / ORIGIN_HEIGHT
        # if A == B:
        # return A or B

        return WIDTH/SIZE_SCREEN_WIDTH if WIDTH/SIZE_SCREEN_WIDTH == HEIGHT/SIZE_SCREEN_HEIGHT else 0
    
    def FPS2Seconds(self) -> float:
        return 1 / self.FPS

    def Seconds2FPS(self,Seconds:float) -> int:
        # Seconds to Frame Per Second
        return Seconds * self.FPS