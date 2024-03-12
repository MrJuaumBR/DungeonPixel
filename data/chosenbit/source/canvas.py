import pygame

class CanvasState:
    screen = 0

class Message:
    keyboard_state = {}

class Color:
    r = 0.0
    g = 0.0
    b = 0.0
    a = 0.0

    def __init__(self, r, g, b, a) -> None:
        self.r = r
        self.g = g
        self.b = b
        self.a = a

    def _convert_to_pygame_color(self) -> pygame.Color:
        r = int(self.r * 255)
        g = int(self.g * 255)
        b = int(self.b * 255)
        a = int(255 - (255 * self.a))
        
        result = (r, g, b, a)
        return result
    
class Rectangle:
    x = 0
    y = 0
    width = 0
    height = 0
    color = 0

    def __init__(self, x, y, width, height, color) -> None:
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color

    def _convert_to_pygame_rectangle(self) ->  pygame.Rect:
        result = pygame.rect.Rect(self.x, self.y, self.width, self.height)

        return result

def create_canvas(canvas: CanvasState, title: str, width: int, height: int):
    result = False

    if pygame.init()[1] > 0:
        result

    canvas.screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption(title)

    result = True
    return result

def destroy_canvas(canvas: CanvasState):
    result = False

    if not canvas.screen:
        return result
    
    pygame.quit()

    result = True
    return result

def process_message(message: Message):
    result = True

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            result = False
        elif event.type == pygame.KEYDOWN:
            key = event.key
            
            message.keyboard_state[key] = True
        elif event.type == pygame.KEYUP:
            key = event.key
           
            message.keyboard_state[key] = False

    return result

def is_key_down(message: Message, key: str):
    result = False

    if ord(key) in message.keyboard_state and message.keyboard_state[ord(key)] == True:
        result = True

    return result

def swap_buffers(canvas: CanvasState):
    pygame.display.flip()

def draw_clear(canvas: CanvasState, color: Color):
    screen = canvas.screen
    color = color._convert_to_pygame_color()
    screen.fill(color)

def draw_rectangle(canvas: CanvasState, rectangle: Rectangle):
    screen = canvas.screen
    color = rectangle.color._convert_to_pygame_color()
    rectangle = rectangle._convert_to_pygame_rectangle()
    pygame.draw.rect(screen, color, rectangle)