from pygame.locals import *
import pygame as pyg
import os
import sys
import ctypes

MoveWindowTo = ctypes.windll.user32.MoveWindow
MoveWindowTo.argtypes = [ctypes.wintypes.HWND, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.wintypes.BOOL]
MoveWindowTo.restype = ctypes.wintypes.BOOL

E_ONLY_FULLSCREEN = -2147483648
E_FULLSCREEN_SCALED = -2147483136

class Engine():
    """
    PyGame Engine
    """
    VERSION = '0.0.1'

    screen = None

    fonts = []

    slider_height = 10 # px
    select_click_delay = 100 # ms
    button_click_delay = 25 # ms

    def __init__(self, screen:pyg.Surface=None):
        """
        Startup Engine & PyGame

        Parameters:
            screen (pyg.Surface): The screen object
        Returns:
            Engine: The Engine object
        """
        if screen:
            self.screen = screen
        pyg.init()

    def set_window_position(self, x: int, y: int):
        # Call it after pygame.display.set_mode()
        window_info = pyg.display.get_wm_info()
        if "window" in window_info:
            window = window_info["window"]
            window_rect = ctypes.wintypes.RECT()
            ctypes.windll.user32.GetWindowRect(window, ctypes.byref(window_rect))
            client_rect = ctypes.wintypes.RECT()
            ctypes.windll.user32.GetClientRect(window, ctypes.byref(client_rect))
            window_width = window_rect.right - window_rect.left
            client_width = client_rect.right - client_rect.left
            border_width = (window_width - client_width) // 2
            MoveWindowTo(window, x - border_width, y, 800, 600, True)
        else:
            print("Could not set the window position")

    def get_title_bar_height(self) -> int:
        result = 0

        window_info = pyg.display.get_wm_info()
        if "window" in window_info:
            window = window_info["window"]
            window_rect = ctypes.wintypes.RECT()
            ctypes.windll.user32.GetWindowRect(window, ctypes.byref(window_rect))
            client_rect = ctypes.wintypes.RECT()
            ctypes.windll.user32.GetClientRect(window, ctypes.byref(client_rect))
            window_height = window_rect.bottom - window_rect.top
            client_height = client_rect.bottom - client_rect.top
            result = (window_height - client_height) // 2
        else:
            print("Could not get the title bar position")

        return result

    # Engine Base Functions
    def create_screen(self, width:int, height:int, flags:int=0) -> pyg.Surface:
        """
        Create the screen object, and return it

        Parameters:
            width (int): The width of the screen
            height (int): The height of the screen
            flags (int): The flags of the screen
        Returns:
            pyg.Surface: The screen object
        """
        if flags == E_ONLY_FULLSCREEN:
            print('[Engine] Scaled Fullscreen')
            flags = E_FULLSCREEN_SCALED
        
        self.screen = pyg.display.set_mode((width, height), flags)
        window_width = pyg.display.get_desktop_sizes()[0][0]
        window_height = pyg.display.get_desktop_sizes()[0][1]
        self.set_window_position((window_width - width) // 2, ((window_height - height) // 2) - self.get_title_bar_height())
        return self.screen
    
    def get_events(self) -> list[pyg.event.Event,]:
        """
        Get the list of events from pygame

        Parameters:
            None
        Returns:
            list[pyg.event.Event,]: The list of events
        """
        return pyg.event.get()
    
    def create_font(self, font:str, size:int,bold:bool=False, italic:bool=False) -> list[pyg.font.FontType, int]:
        """
        Create a SysFont object, and add to array

        Parameters:
            font (str): The name of the font.
            size (int): The font size.
            bold (bool): Whether the font is bold.
            italic (bool): Whether the font is italic.
        Returns:
            list[pyg.font.Font, int]: The font object and its index
        """
        f = pyg.font.SysFont(font, size, bold, italic)
        if not (f in self.fonts):
            print('[Engine] Font created')
            self.fonts.append(f)
        else:
            print('[Engine] Font already exists')
            font_index = self.fonts.index(f)
            return self.fonts[font_index], font_index
        return f,self.fonts.index(f)
    
    def create_font2(self, font_file:str, size:int) -> list[pyg.font.FontType, int]:
        """
        Create a Font object, and add to array

        Parameters:
            font file (str): The file of the font.
            size (int): The font size.
        Returns:
            list[pyg.font.Font, int]: The font object and its index
        """
        f = pyg.font.Font(font_file, size)
        if not (f in self.fonts):
            print('[Engine] Font created')
            self.fonts.append(f)
        else:
            print('[Engine] Font already exists')
            font_index = self.fonts.index(f)
            return self.fonts[font_index], font_index
        return f,self.fonts.index(f)

    def flip(self):
        """
        Flip Screen

        Parameters:
            None
        Returns:
            None
        """
        pyg.display.flip()

    def update(self):
        """
        Update Screen

        Parameters:
            None
        Returns:
            None
        """
        pyg.display.update()
    
    def screen_set_title(self, title:str):
        """
        Set the title of the screen

        Parameters:
            title (str): The title of the screen
        Returns:
            None
        """
        pyg.display.set_caption(title)

    def quit(self):
        """
        Quit the game

        Parameters:
            None
        Returns:
            None
        """
        pyg.quit()
        sys.exit()
    
    # Draw Functions
    def draw_text(self,x:int,y:int, text:str, font:int or pyg.font.FontType, color:tuple[int,int,int], bg_color:tuple[int,int,int]=None, surface:pyg.Surface=None)-> Rect: # type: ignore
        """
        Draw text with the specified font, in the topleft pos, specified color, bg color

        Parameters:
            x (int): The x pos
            y (int): The y pos
            text (str): The text
            font (int or pyg.font.FontType): The font
            color (tuple[int,int,int]): The color
            bg_color (tuple[int,int,int]): The background color
            surface (pyg.Surface): The surface(Screen/Surface)
        Returns:
            text surface(Rect): The rect of text surface
        """
        font:pyg.font.FontType = self._convert_font(font)
        if bg_color:
            text_render = font.render(text, True, color, bg_color)
        else:
            text_render = font.render(text, True, color)
        if surface:
            surf = surface.blit(text_render, (x, y))
        else:
            surf:pyg.rect.RectType = self.screen.blit(text_render, (x, y))
        return surf
    
    def draw_rect(self,x:int,y:int, color:tuple[int,int,int,],size:tuple[int,int],border_width:int=0,border_color:tuple[int,int,int,]=None,surface:pyg.Surface=None) -> Rect: # type: ignore
        """
        Draw a rectangle, it can have border or not, and alpha color

        Parameters:
            x (int): The x pos
            y (int): The y pos
            color (tuple[int,int,int,]): The color
            size (tuple[int,int]): The size
            border_width (int): The border width
            border_color (tuple[int,int,int,]): The border color
            surface (pyg.Surface): The surface
        Returns:
            rect surface(Rect): The rect of rect surface
        """
        # Preset
        HAS_BORDER = False
        HAS_ALPHA = False

        if border_width or border_width != 0:
            HAS_BORDER = True
        if len(color) == 4:
            HAS_ALPHA = True
        if surface:
            surf = surface
        else:
            surf = self.screen
        if not HAS_ALPHA:
            # If Not Has alpha, then draw with normal method
            if HAS_BORDER:
                border = pyg.draw.rect(surf, border_color, Rect(x-(border_width//2), y-(border_width//2), size[0], size[1]), border_width)
            rect = pyg.draw.rect(surf, color, Rect(x, y, size[0], size[1]))
        else:
            # If Has alpha, then draw with alpha method
            rect = pyg.Surface((size[0], size[1]),SRCALPHA)
            rect.fill(color)
            if HAS_BORDER:
                border = pyg.Surface((size[0]+border_width, size[1]+border_width),SRCALPHA)
                border.fill(border_color)
                surf.blit(border, (x-(border_width//2), y-(border_width//2)))# Draw border
            
            surf.blit(rect, (x, y)) # Draw internal rect
        returnF = lambda: rect if not HAS_ALPHA else rect.get_rect()
        return returnF()

    def draw_circle(self, x:int, y:int, color:tuple[int,int,int], radius:int, surface:pyg.Surface=None) -> Rect: # type: ignore
        """
        Draw a circle

        Parameters:
            x (int): The x pos
            y (int): The y pos
            color (tuple[int,int,int]): The color
            radius (int): The radius
            surface (pyg.Surface): The surface
        Returns:
            circle surface(Rect): The rect of circle surface
        """
        if surface:
            surf = surface
        else:
            surf = self.screen

        c = pyg.draw.circle(surf, color, (x, y), radius)
        return c

    def draw_button(self,x:int,y:int,text:str, font:int or pyg.font.FontType, color:tuple[int,int,int], bg_color:tuple[int,int,int], surface:pyg.Surface=None) -> bool: # type: ignore
        """
        Draw a button and return button state(bool)

        Parameters:
            x (int): The x pos
            y (int): The y pos
            text (str): The text
            font (str): The font
            color (tuple[int,int,int]): The color
            bg_color (tuple[int,int,int]): The background color
            surface (pyg.Surface): The surface
        Returns:
            bool: The button state
        """
        re:pyg.rect.RectType = self.draw_text(x, y, text, font, color, bg_color, surface)
        if self.is_mouse_hover(re):
            if self.mouse_pressed(0):
                pyg.time.delay(self.button_click_delay)
                return True
            else:
                return False
        return False

    def draw_select(self, x:int, y:int, font:int or pyg.font.FontType, colors:list[tuple[int,int,int]],selectList:list[any,],index:int, surface:pyg.Surface=None) -> int: # type: ignore
        """
        Draw a select list

        Parameters:
            x (int): The x pos
            y (int): The y pos
            font (str): The font
            colors (list[tuple[int,int,int]]): The color
            selectList (list[any]): The select list
            index (int): The index
            surface (pyg.Surface): The surface
        Returns:
            int: The index
        """
        font:pyg.font.FontType = self._convert_font(font) # Convert font
        w,_ = font.size(f'{selectList[index]}') # Width & HEight

        backBtn_w, _ =font.size('<')

        backBtn = self.draw_button((x-w)+backBtn_w,y,f'<',font,colors[0],colors[1],surface)
        nextBtn = self.draw_button(x+w,y,f'>',font,colors[0],colors[1],surface)
        text = self.draw_text(x,y,str(selectList[index]),font,colors[1],surface)

        if backBtn:
            index -= 1
            pyg.time.delay(self.select_click_delay)
        if nextBtn:
            index += 1
            pyg.time.delay(self.select_click_delay)
        if index > len(selectList)-1:
            index = 0
        if index < 0:
            index = len(selectList)-1

        return index

    def draw_checkbox(self,x:int,y:int,font:int or pyg.font.FontType,text:str,checked:bool,colors:list[tuple[int,int,int]],surface:pyg.Surface=None) -> bool: # type: ignore

        font:pyg.font.FontType = self._convert_font(font) # Convert font
        w,h = font.size(f'{text}') # Width & HEight
        bw = w//4

        m_pos = self.mouse_pos()

        ColorSelect = lambda: colors[1] if checked else colors[2]

        b2:pyg.rect.RectType = self.draw_text(x+bw+5,y,text,font,ColorSelect(),surface)

        b1 = pyg.draw.rect(surface or self.screen,colors[0],(x,y,bw,h))
        if checked:
            pyg.draw.rect(surface or self.screen,colors[1],(x+2,y+2,bw-4,h-4))
            
        if b1.collidepoint(m_pos) or b2.collidepoint(m_pos):
            if self.mouse_pressed(0):
                checked = not checked
                pyg.time.delay(self.select_click_delay)

        

        return checked

    def draw_slider(self, x:int, y:int, width:int, colors:list[tuple[int,int,int]],curPosX:int, surface:pyg.Surface=None,detail:bool=False) -> tuple[int, float]:
        """
        Draw a slider and return the value and percentage

        Parameters:
            x (int): The x pos
            y (int): The y pos
            width (int): The width
            colors (list[tuple[int,int,int]]): The colors
            maxValue (int): The max value
            surface (pyg.Surface): The surface
        Returns:
            tuple[int, float]: The value and percentage
        """
        if not curPosX:
            curPosX = x
        m_pos = self.mouse_pos()
        MaxX = x + width
        percentage = curPosX/ MaxX
        if percentage < 0:
            percentage = 0
        if percentage > 1:
            percentage = 1

        # Background
        self.draw_rect(x,y,colors[0],(width,self.slider_height),surface=surface)

        # Detail
        if detail:
            pyg.draw.line(surface or self.screen,colors[2],(x+5,y+(self.slider_height//2)),((x+width)-5,y+(self.slider_height//2)),2)

        b = self.draw_circle(curPosX,y+(self.slider_height//2),colors[1],5,surface=surface)
        if b.collidepoint(m_pos):
            if self.mouse_pressed(0):
                curPosX = m_pos[0]
                if curPosX < x:
                    curPosX = x
                if curPosX > MaxX:
                    curPosX = MaxX
        
        return curPosX, percentage

    # Logic Functions
    def keys_pressed(self) -> pyg.key.ScancodeWrapper:
        """
        Get the list of keys pressed

        Parameters:
            None
        Returns:
            list[pyg.key.Key]: The list of keys
        """
        return pyg.key.get_pressed()

    def key_pressed(self, key:int) -> bool:
        """
        Check if the key is pressed

        Parameters:
            key (pyg.key.Key): The key
        Returns:
            bool: The result
        """
        return self.keys_pressed()[key]

    def is_mouse_hover(self, surface:pyg.Surface or pyg.rect.RectType) -> bool: # type: ignore
        """
        Check if the mouse is hovering

        Parameters:
            surface (pyg.Surface or pyg.rect.RectType): The surface
        Returns:
            bool: The result
        """
        if type(surface) == pyg.Surface:
            surface:pyg.rect.RectType = surface.get_rect()
        
        m_pos = self.mouse_pos()
        return surface.collidepoint(m_pos[0], m_pos[1])

    def mouse_pressed(self, button:int, mouse_type:int=3) -> bool:
        """
        Check if the mouse button is pressed

        Parameters:
            button (int): The button who is pressed
            mouse_type (int): The mouse type(3 Buttons, 5 Buttons, 6, ...)
        Returns:
            bool: The result
        """
        return pyg.mouse.get_pressed(mouse_type)[button]

    def mouse_pos(self) -> tuple[int,int]:
        """
        Get the mouse pos

        Parameters:
            None
        Returns:
            tuple[int,int]: The mouse pos
        """
        return pyg.mouse.get_pos()

    # Engine Need Functions
    def load_image(self, image_path:str) -> pyg.surface:
        return pyg.image.load(image_path)
    def _convert_font(self, font:int or pyg.font.Font) -> pyg.font.FontType: # type: ignore
        if type(font) == int:
            return self.fonts[font]
        else:
            return font

class spritesheet():
    active:bool = True
    def __init__(self, path:str) -> None:
        self.path = path
        self.file_type = path.strip('.')[-1]
        try:
            self.sheet = pyg.image.load(path).convert()
        except Exception as e:
            print(f'[Engine - Spritesheet - Error] {e}')
            self.active = False

    def image_at(self, rectangle:tuple[int,int,int,int], colorkey=None) -> pyg.surface:
        """
        Loads image from x,y,x+offset,y+offset

        Parameters:
            rectangle (tuple[int,int,int,int]): The rectangle
            colorkey (tuple[int,int,int]): The colorkey
        Returns:
            pyg.surface: The surface
        """
        if self.active:
            rect = pyg.Rect(rectangle)
            image = pyg.Surface(rect.size).convert()
            image.blit(self.sheet,(0,0),rect)
            if colorkey:
                if colorkey == -1:
                    colorkey = image.get_at((0,0))
                image.set_colorkey(colorkey,pyg.RLEACCEL)
            return image
        else:
            print(f'[Engine - Spritesheet - Info] Spritesheet({self.path}) not active')
            return None
        
    def images_at(self, rects:list[tuple[int,int,int,int]], colorkey=None) -> list[pyg.Surface,]:
        """
        Loads multiple images, supply a list of coordinates

        Parameters:
            rects (list[tuple[int,int,int,int]]): The list of rectangles
            colorkey (tuple[int,int,int]): The colorkey
        Returns:
            list[pyg.surface]: The list of surfaces
        """
        return [self.image_at(rect, colorkey) for rect in rects]
            
    
    def load_strip(self, rect:tuple[int,int,int,int], image_count:int, colorkey=None) -> list[pyg.Surface,]:
        """
        Loads a strip of images and return them as list

        Parameters:
            rect (tuple[int,int,int,int]): The rectangle
            image_count (int): The image count
            colorkey (tuple[int,int,int]): The colorkey
        Returns:
            list[pyg.surface]: The list of surfaces
        """
        tups = [(rect[0]+rect[2]*x, rect[1], rect[2], rect[3])
                for x in range(image_count)]
        return self.images_at(tups, colorkey)


class Button():
    engine:Engine
    font:int or pyg.font.Font # type: ignore
    text:str
    rect:pyg.rect.Rect
    image_surface:pyg.surface
    pos:tuple[int,int]
    size:tuple[int,int]
    def __init__(self,engine:Engine, x:int,y:int,text:str, font:int or pyg.font.FontType, button_image, size:tuple=None,screen:pyg.Surface=None) -> None: # type: ignore
        self.engine = engine
        self.pos = (x,y)
        self.text = text
        self.font = self.engine._convert_font(font)
        s = self.font.size(text)
        self.size = (s[0]*1.2,s[1]*1.2)

        if type(button_image) == str:
            self.image_surface = self.engine.load_image(button_image)
        else:
            self.image_surface = button_image
        self.define_scales()

        if screen:
            self.screen = screen
        else:
            self.screen = self.engine.screen

    def define_scales(self):
        self.image_surface = pyg.transform.scale(self.image_surface, self.size)

    def draw(self):
        self.screen.blit(self.image_surface, self.pos)
        self.engine.draw_text(self.pos[0], self.pos[1], self.text, self.font, (255,255,255), surface=self.screen)