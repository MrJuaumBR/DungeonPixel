from pygame.locals import *
import pygame as pyg
import os
import sys

E_ONLY_FULLSCREEN = -2147483648
E_FULLSCREEN_SCALED = -2147483136
MOUSE_BUTTON_LEFT = 0
MOUSE_BUTTON_RIGHT = 2
MOUSE_BUTTON_MIDDLE = 1

class Position():
    x = 0
    y = 0

    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y

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


    # Engine Base Functions
    def create_window(self, width:int, height:int, flags:int=0) -> pyg.Surface:
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
    
    def create_font(self, font_name:str, font_size:int, is_bold:bool=False, is_italic:bool=False) -> list[pyg.font.FontType, int]:
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
        f = pyg.font.SysFont(font_name, font_size, is_bold, is_italic)
        if not (f in self.fonts):
            print('[Engine] Font created')
            self.fonts.append(f)
        else:
            print('[Engine] Font already exists')
            font_index = self.fonts.index(f)
            return self.fonts[font_index], font_index
        return f,self.fonts.index(f)
    
    def create_font_from_file(self, file_path:str, font_size:int) -> list[pyg.font.FontType, int]:
        """
        Create a Font object, and add to array

        Parameters:
            font file (str): The file of the font.
            size (int): The font size.
        Returns:
            list[pyg.font.Font, int]: The font object and its index
        """
        f = pyg.font.Font(file_path, font_size)
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
    
    def set_window_title(self, title:str):
        """
        Set the title of the screen

        Parameters:
            title (str): The title of the screen
        Returns:
            None
        """
        pyg.display.set_caption(title)

    def destroy_window(self):
        """
        Quit the game

        Parameters:
            None
        Returns:
            None
        """
        pyg.quit()
        sys.exit()

    def debug_draw_lines_for_rectangular_shape(self, surface: pyg.Surface, rectangle: pyg.Rect):
        r = rectangle
        pyg.draw.line(surface, (255, 0, 0), (r.x, r.y), (r.x + r.width - 1, r.y))
        pyg.draw.line(surface, (255, 0, 0), (r.x, r.y + r.height - 1), (r.x + r.width - 1, r.y + r.height - 1))
        pyg.draw.line(surface, (255, 0, 0), (r.x, r.y), (r.x, r.y + r.height - 1))
        pyg.draw.line(surface, (255, 0, 0), (r.x + r.width - 1, r.y), (r.x + r.width - 1, r.y + r.height - 1))
        
    def parse_ini(self, file_path: str) -> dict:
        result = {}
        current_section = None
        with open(file_path, 'r') as file:
            for line in file:
                line = line.strip()

                if not line or line.startswith(";"):
                    continue

                if line.startswith("[") and line.endswith("]"):
                    current_section = line[1:-1]
                    result[current_section] = {}
                    continue

                if current_section != None:
                    key, value = line.split("=")           
                    key = key.strip()
                    value = value.strip()
                    result[current_section][key] = value
        
        return result

    def ini_get_boolean(self, dictionary: dict, section: str, key: str):
        result = False

        value = dictionary[section][key]

        if value.lower() == "true":
            result = True
        elif value.lower() == "false":
            result = False
        else:
            raise ValueError("the value is not 'true' or 'false'")        

        return result
    
    def ini_get_integer(self, dictionary: dict, section: str, key: str):
        result = 0

        value = dictionary[section][key]

        result = int(value)

        return result

    def ini_get_string(self, dictionary: dict, section: str, key: str):
        result = ""

        result = dictionary[section][key]
        result = result[1:-1]

        return result
    
    def hot_load_game_config(self, game_config):
        game_config.dictionary = self.parse_ini("./data/config.ini")
        game_config.game_title_x = self.ini_get_integer(game_config.dictionary, "GUI", "game_title_x")
        game_config.game_title_y = self.ini_get_integer(game_config.dictionary, "GUI", "game_title_y")

        game_config.play_button_x = self.ini_get_integer(game_config.dictionary, "GUI", "play_button_x")
        game_config.play_button_y = self.ini_get_integer(game_config.dictionary, "GUI", "play_button_y")
        game_config.settings_button_x = self.ini_get_integer(game_config.dictionary, "GUI", "settings_button_x")
        game_config.settings_button_y = self.ini_get_integer(game_config.dictionary, "GUI", "settings_button_y")
        game_config.quit_button_x = self.ini_get_integer(game_config.dictionary, "GUI", "quit_button_x")
        game_config.quit_button_y = self.ini_get_integer(game_config.dictionary, "GUI", "quit_button_y")

        game_config.settings_x = self.ini_get_integer(game_config.dictionary, "GUI", "settings_x")
        game_config.settings_y = self.ini_get_integer(game_config.dictionary, "GUI", "settings_y")
        game_config.volume_x = self.ini_get_integer(game_config.dictionary, "GUI", "volume_x")
        game_config.volume_y = self.ini_get_integer(game_config.dictionary, "GUI", "volume_y")
        game_config.slider_x = self.ini_get_integer(game_config.dictionary, "GUI", "slider_x")
        game_config.slider_y = self.ini_get_integer(game_config.dictionary, "GUI", "slider_y")
        #game_config.slider_circle_x = self.ini_get_integer(game_config.dictionary, "GUI", "slider_circle_x")
        #game_config.slider_circle_y = self.ini_get_integer(game_config.dictionary, "GUI", "slider_circle_y")
        game_config.screen_size_x = self.ini_get_integer(game_config.dictionary, "GUI", "screen_size_x")
        game_config.screen_size_y = self.ini_get_integer(game_config.dictionary, "GUI", "screen_size_y")
        #game_config.screen_size_left_arrow_x = self.ini_get_integer(game_config.dictionary, "GUI", "screen_size_left_arrow_x")
        #game_config.screen_size_left_arrow_y = self.ini_get_integer(game_config.dictionary, "GUI", "screen_size_left_arrow_y")
        game_config.window_dimension_x = self.ini_get_integer(game_config.dictionary, "GUI", "window_dimension_x")
        game_config.window_dimension_y = self.ini_get_integer(game_config.dictionary, "GUI", "window_dimension_y")
        #game_config.screen_size_right_arrow_x = self.ini_get_integer(game_config.dictionary, "GUI", "screen_size_right_arrow_x")
        #game_config.screen_size_right_arrow_y = self.ini_get_integer(game_config.dictionary, "GUI", "screen_size_right_arrow_y")
        game_config.fps_x = self.ini_get_integer(game_config.dictionary, "GUI", "fps_x")
        game_config.fps_y = self.ini_get_integer(game_config.dictionary, "GUI", "fps_y")
        #game_config.fps_left_arrow_x = self.ini_get_integer(game_config.dictionary, "GUI", "fps_left_arrow_x")
        #game_config.fps_left_arrow_y = self.ini_get_integer(game_config.dictionary, "GUI", "fps_left_arrow_y")
        #game_config.fps_number_x = self.ini_get_integer(game_config.dictionary, "GUI", "fps_number_x")
        #game_config.fps_number_y = self.ini_get_integer(game_config.dictionary, "GUI", "fps_number_y")
        #game_config.fps_right_arrow_x = self.ini_get_integer(game_config.dictionary, "GUI", "fps_right_arrow_x")
        #game_config.fps_right_arrow_y = self.ini_get_integer(game_config.dictionary, "GUI", "fps_right_arrow_y")
        game_config.show_fps_x = self.ini_get_integer(game_config.dictionary, "GUI", "show_fps_x")
        game_config.show_fps_y = self.ini_get_integer(game_config.dictionary, "GUI", "show_fps_y")
        game_config.show_fps_checkbox_x = self.ini_get_integer(game_config.dictionary, "GUI", "show_fps_checkbox_x")
        game_config.show_fps_checkbox_y = self.ini_get_integer(game_config.dictionary, "GUI", "show_fps_checkbox_y")

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
                
        self.debug_draw_lines_for_rectangular_shape(self.screen, surf)
        
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
        if surface == None:
            surface = self.screen

        result = pyg.draw.circle(surface, color, (x, y), radius)
        return result

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
        result = False

        re:pyg.rect.RectType = self.draw_text(x, y, text, font, color, bg_color, surface)
        if self.is_mouse_hover(re):
            if self.is_mouse_button_pressed(MOUSE_BUTTON_LEFT):
                pyg.time.delay(self.button_click_delay) #@HACK
                result = True
        
        return result

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
            pyg.time.delay(self.select_click_delay) #@HACK
        if nextBtn:
            index += 1
            pyg.time.delay(self.select_click_delay) #@HACK
        if index > len(selectList)-1:
            index = 0
        if index < 0:
            index = len(selectList)-1

        return index

    def draw_checkbox(self,x:int,y:int,font:int or pyg.font.FontType,text:str,checked:bool,colors:list[tuple[int,int,int]],surface:pyg.Surface=None) -> bool: # type: ignore

        font:pyg.font.FontType = self._convert_font(font) # Convert font
        w,h = font.size(f'{text}') # Width & HEight
        bw = w//4

        m_pos = self.get_mouse_position()

        ColorSelect = lambda: colors[1] if checked else colors[2]

        b2:pyg.rect.RectType = self.draw_text(x+bw+5,y,text,font,ColorSelect(),surface)

        b1 = pyg.draw.rect(surface or self.screen,colors[0],(x,y,bw,h))
        r = 0
        if checked:
            r = pyg.draw.rect(surface or self.screen,colors[1],(x+2,y+2,bw-4,h-4))
            
        if b1.collidepoint(m_pos.x, m_pos.y) or b2.collidepoint(m_pos.x, m_pos.y):
            if self.is_mouse_button_pressed(MOUSE_BUTTON_LEFT):
                checked = not checked
                pyg.time.delay(self.select_click_delay) #@HACK

        self.debug_draw_lines_for_rectangular_shape(self.screen, b1)
        if type(r) == pyg.Rect:
            self.debug_draw_lines_for_rectangular_shape(self.screen, r)

        return checked
    
    def draw_slider(self, x:int, y:int, width:int, colors:list[tuple[int,int,int]],curPosX:int, Slider_VolumePercentage, surface:pyg.Surface=None, detail:bool=False) -> tuple[int, float]:
        slider_percentage = Slider_VolumePercentage
        slider_x = curPosX
        
        background_rectangle = pyg.draw.rect(self.screen, colors[0], pyg.Rect(x, y, width, self.slider_height + 8))
        
        circle_radius = 5        
        circle_y = y + circle_radius
        circle_color = colors[1]
        circle_x = ((Slider_VolumePercentage * width) - 1) + x #curPosX    
        circle_rectangle = self.draw_circle(circle_x, circle_y, circle_color, circle_radius, surface=surface)

        mouse_position = self.get_mouse_position()
        if background_rectangle.collidepoint(mouse_position.x, mouse_position.y):
            if self.is_mouse_button_pressed(MOUSE_BUTTON_LEFT):
                slider_percentage = ((mouse_position.x - x) + 1) / width
                slider_x = mouse_position.x

        self.debug_draw_lines_for_rectangular_shape(self.screen, background_rectangle)
        self.debug_draw_lines_for_rectangular_shape(self.screen, circle_rectangle)

        return slider_x, slider_percentage
    
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
        
        m_pos = self.get_mouse_position()
        return surface.collidepoint(m_pos.x, m_pos.y)

    def is_mouse_button_pressed(self, button:int, mouse_type:int=3) -> bool:
        """
        Check if the mouse button is pressed

        Parameters:
            button (int): The button who is pressed
            mouse_type (int): The mouse type(3 Buttons, 5 Buttons, 6, ...)
        Returns:
            bool: The result
        """
        return pyg.mouse.get_pressed(mouse_type)[button]

    def get_mouse_position(self) -> Position:
        """
        Get the mouse pos

        Parameters:
            None
        Returns:
            tuple[int,int]: The mouse pos
        """
        position_tuple = pyg.mouse.get_pos()
        result = Position(position_tuple[0], position_tuple[1])
        
        return result

    # Engine Need Functions
    def load_image(self, image_path:str) -> pyg.surface:
        return pyg.image.load(image_path)
    def _convert_font(self, font:int or pyg.font.Font) -> pyg.font.FontType: # type: ignore
        if type(font) == int:
            return self.fonts[font]
        else:
            return font
        
class SelectMenu():
    Buttons = []
    Buttons_Actions = {}
    Button_Fonts = 0
    def __init__(self, engine:Engine,screen:pyg.Surface, buttons:list[tuple, ], Button_Fonts:int) -> None:
        self.screen = screen
        self.add_buttons(buttons)
        self.Engine = engine
        self.Button_Fonts = Button_Fonts

    def add_buttons(self, buttons:list[str,]):
        for button in buttons:
            self.add_button(button[0], button[1])

    def add_button(self, name:str, function):
        self.Buttons.append(name)
        self.Buttons_Actions[name] = function

    def update(self):
        pass

    def draw(self):
        for x,button in enumerate(self.Buttons):
            font_height = self.Engine._convert_font(self.Button_Fonts).size(button)[1]
            font_height = font_height + 64 * (x+1)# Font Height + Start Y * Index
            self.Engine.draw_button(64,font_height, button, self.Button_Fonts, (255,255,255), (0,0,0), self.screen)

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