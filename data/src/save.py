from ..config import *

# Game Player Sprite, Logic, and Load
# Load Player Sprite
p_s = spritesheet(PATH_TEXTURES+"player.png")
Player_Sprite_Frames = {
    'idle':[*p_s.images_at([(0,0,32,32),(32,0,32,32),(64,0,32,32)],colorkey=0)],
    'walk':{
        'x':[*p_s.images_at([(0,32,32,32),(32,32,32,32),(64,32,32,32)],colorkey=0)],
        'y':[*p_s.images_at([(0,64,32,32),(32,64,32,32),(64,64,32,32)],colorkey=0)],
    },
}

class player(pyg.sprite.Sprite):
    saveable = ['name','rect','debug', 'position_vec', 'health', 'maxhealth', 'defense', 'agility', 'strength', 'luck', 'level', 'experience']

    name = 'Zord'
    layer = 2

    can_collide = True
    type = 'player'

    Camera = None
    rect:pyg.rect.RectType

    offset_pos:pyg.math.Vector2 = pyg.math.Vector2()

    # Hidden Status

    speed:int = 3
    drag:float = 0.65
    max_speed: int = 5
    position_vec:pyg.math.Vector2 = pyg.math.Vector2()
    
    state:str = 'idle'
    animate_frame:float = 0

    sprinting:bool = False
    sprint_time:int = 0
    debug:bool = False
    debug_tool_shown:bool = False
    dead:bool = False

    # Shown status
    # Attributes
    defense:int = 1
    agility:int = 1
    strength:int = 1
    luck:int = 1
    level:int = 1
    experience:int = 0

    maxhealth:int = 100 + (defense*2)
    health:int = maxhealth
    max_speed:int = 5 + (agility*2)
    
    def __init__(self, SaveClass,*groups) -> None:
        """
        Create the player handler, and Sprite for the game&nbsp;

        ↑+ Control;
        
        ↑+ Easy;
        """
        super().__init__(*groups)
        self.SaveClass = SaveClass
        try:
            from .camera import CameraGroup as Camera_Type
            self.Camera:Camera_Type = self.groups()[0]
        except Exception as e:
            print(f'[Save - Player - Init] {e}')
            pass

        self.size = (32,32)

        self.rect = Rect((GAME_MAP_SIZE[0]/2)-(self.size[0]/2),(GAME_MAP_SIZE[1]/2)-(self.size[1]/2),*self.size)

        self.image = pyg.Surface(self.size,pyg.SRCALPHA)
        self.animate()

    def _manager_keyboard(self):
        # Mov Up
        # Keys = w, Arrow Up, Numpad 8
        Mov_Up:bool = pme.key_pressed(K_w) or pme.key_pressed(K_UP) or pme.key_pressed(K_KP8)
        # Mov Down
        # Keys = s, Arrow Down, Numpad 2
        Mov_Down:bool = pme.key_pressed(K_s) or pme.key_pressed(K_DOWN) or pme.key_pressed(K_KP2)
        # Mov Left
        # Keys = a, Arrow Left, Numpad 4
        Mov_Left:bool = pme.key_pressed(K_a) or pme.key_pressed(K_LEFT) or pme.key_pressed(K_KP4)
        # Mov Right
        # Keys = d, Arrow Right, Numpad 6
        Mov_Right:bool = pme.key_pressed(K_d) or pme.key_pressed(K_RIGHT) or pme.key_pressed(K_KP6)


        # Mov X Axis
        if Mov_Left:
            self.position_vec.x -= self.speed
        elif Mov_Right:
            self.position_vec.x += self.speed

        # Mov Y Axis
        if Mov_Up:
            self.position_vec.y -= self.speed
        elif Mov_Down:
            self.position_vec.y += self.speed
        
        # Others Keys
        Sprinting = pme.key_pressed(K_LSHIFT) or pme.key_pressed(K_RSHIFT)

        if Sprinting:
            self.sprinting = True
            self.sprint_time += 1
        else:
            self.sprinting = False
            self.sprint_time = 0

        self.sprint()
    
    def sprint(self):
        """Sprint Control, changes Max Speed"""
        if self.sprinting and self.sprint_time > 3:
            self.max_speed = round(self.max_speed * 1.8)
        else:
            self.max_speed = 5

    def _get_magnitude(self) -> float:
        """Same as player speed"""
        vector_x:float = self.position_vec.x
        vector_y:float = self.position_vec.y

        magnitude:float = (vector_x**2 + vector_y**2)**0.5
        return magnitude

    def animate(self):
        """Update player animation based on state and movement vectors."""
        state, x, y = self.state, self.position_vec.x, self.position_vec.y
        image_seq = Player_Sprite_Frames[state]

        if state == 'idle':
            image = image_seq[int(self.animate_frame)]
        else:
            image_keys = 'x' if abs(x) >= 0.15 else 'y'
            image = image_seq[image_keys][int(self.animate_frame)]
            if image_keys == 'x' and x < 0:
                image = pyg.transform.flip(image, True, False)
        self.image = pyg.transform.scale(image, self.size)

        self.animate_frame = (self.animate_frame + 0.35) % (
            len(image_seq) if state == 'idle' else len(image_seq[image_keys]))
                

    def _manager_movment(self):
        if not self.dead: # If the player is not dead
            if (self.position_vec.x != 0 or self.position_vec.y != 0) and (abs(self.position_vec.x) >= 0.15 or abs(self.position_vec.y) >= 0.15):
                self.state = 'walk'
            else:
                self.state = 'idle'
            # Calculate the magnitude of the movement vector
            magnitude = self._get_magnitude()

            # limit the magnitude of the movement vector to the maximum speed
            if magnitude >= self.max_speed:
                scale_factor = self.max_speed / magnitude
                self.position_vec.x *= scale_factor
                self.position_vec.y *= scale_factor

            # Apply movement with or no the scale factor
            if self.position_vec.x != 0:
                self.rect.x += self.position_vec.x
            if self.position_vec.y != 0:
                self.rect.y += self.position_vec.y
        else:
            self.state = 'dead'

        self.animate()

    def _manager_drag(self):
        # Get Vectors to only > 1
        # Set Vectors to only positive values, if negative, set to positive too
        X_Vec = round(abs(self.position_vec.x),3)
        Y_Vec = round(abs(self.position_vec.y),3)

        # Apply Drag
        # If X Vector > 0.02 Then Apply Drag Else Set X Vector to 0
        if X_Vec > 0.02:
            self.position_vec.x *= self.drag
        else:
            self.position_vec.x = 0
        # If Y Vector > 0.02 Then Apply Drag Else Set Y Vector to 0
        if Y_Vec > 0.02:
            self.position_vec.y *= self.drag
        else:
            self.position_vec.y = 0

    def _handle_x_collision(self,sprites:list[pyg.sprite.Sprite,]) -> list:
        x_collision = []
        # Handle collision logic for X Direction
        # Add collision sprites to x_collision list
        for sprite in sprites:
            if str(sprite.type).lower() != str(self.type).lower(): # Ignore Player
                if self.rect.colliderect(sprite.rect):
                    # If Vector X Was changing
                    if self.position_vec.x != 0:
                        # X from Screen Starts at left and goes to right
                        # Player Right > Sprite Left
                        if self.rect.right > sprite.rect.left and self.position_vec.x > 0: # if right side of player is touching left side of sprite and is moving
                            x_collision.append(sprite)
                        # Player Left < Sprite Right
                        if self.rect.left < sprite.rect.right and self.position_vec.x < 0: # if left side of player is touching right side of sprite and is moving
                            x_collision.append(sprite)
        return x_collision

    def _handle_y_collision(self,sprites:list[pyg.sprite.Sprite,]) -> list:
        y_collision = []
        # Handle collision logic for Y Direction
        # Add collision sprites to y_collision list
        for sprite in sprites:
            if str(sprite.type).lower() != str(self.type).lower(): # Ignore Player
                if self.rect.colliderect(sprite.rect):
                    # If Vector Y Was changing
                    if self.position_vec.y != 0:
                        # Y from Screen Starts at top and goes to bottom
                        # Player Bottom > Sprite Top
                        if self.rect.bottom > sprite.rect.top and self.position_vec.y > 0: # if bottom side of player is touching top side of sprite and is moving
                            y_collision.append(sprite)
                        # Player Top < Sprite Bottom
                        if self.rect.top < sprite.rect.bottom and self.position_vec.y < 0: # if top side of player is touching bottom side of sprite and is moving
                            y_collision.append(sprite)
        return y_collision

    def _resolve_x_collision(self,x_col:list[pyg.sprite.Sprite,]):
         # For each sprite colliding
            for sprite in x_col:
                # make sure they are colliding
                if self.rect.colliderect(sprite.rect):
                    # If Vector X Was changing + 1
                    if self.position_vec.x > 0: # Then is going to right side
                        self.rect.right = min(sprite.rect.left, sprite.rect.left)
                    elif self.position_vec.x < 0: # Then is going to left side
                        self.rect.left = max(sprite.rect.right, sprite.rect.right)

    def _resolve_y_collision(self,y_col:list[pyg.sprite.Sprite,]):
        # For each sprite colliding
            for sprite in y_col:
                # make sure they are colliding
                if self.rect.colliderect(sprite.rect):
                    # If Vector Y Was changing + 1
                    if self.position_vec.y > 0: # Then is going to bottom side
                        self.rect.bottom = min(sprite.rect.top, sprite.rect.top)
                    elif self.position_vec.y < 0: # Then is going to top side
                        self.rect.top = max(sprite.rect.bottom, sprite.rect.bottom)

    def _manager_collision(self):
        if self.Camera: # If Camera Group Has Defined
            s = self.Camera.sprites()
            x_col = self._handle_x_collision(s)
            y_col = self._handle_y_collision(s)

            if len(x_col) > 0:
                self._resolve_x_collision(x_col)
            if len(y_col) > 0:
                self._resolve_y_collision(y_col)
        else: # If Camera Group Has Not Defined
            if len(self.groups()) > 0: # If Player Has Groups
                self.Camera = self.groups()[0] # Set Camera Group

    def _limit_player(self):
        if self.rect.right >= GAME_MAP_SIZE[0]: # Right of Player >= Left of Screen
            # Teleport to Left of Screen
            self.teleport(x=0)
        elif self.rect.left <= 0: # Left of Player <= Left of Screen
            # Teleport to Right of Screen
            self.teleport(x=GAME_MAP_SIZE[0]-self.rect.width)
        
        if self.rect.bottom >= GAME_MAP_SIZE[1]: # Bottom of Player >= Top of Screen
            # Teleport to Top of Screen
            self.teleport(y=0)
        elif self.rect.top <= 0: # Top of Player <= Top of Screen
            # Teleport to Bottom of Screen
            self.teleport(y=GAME_MAP_SIZE[1]-self.rect.height)

    def teleport(self, x:float=None, y:float=None, convert_offset:bool = False):
        if convert_offset:
            if x is not None:
                self.offset_pos.x = x
            if y is not None:
                self.offset_pos.y = y
        else:
            if x is not None:
                self.rect.x = x
            if y is not None:
                self.rect.y = y

    def take_damage(self, damage:int):
        if self.health > 0:
            self.health -= damage
            if self.health <= 0:
                self.health = 0
                self.dead = True

    def Isdebug(self):
        if self.debug:
            m_pos = pme.mouse_pos()
            pme.draw_text(5*GAME_SCREEN_RATIO[0], 1*GAME_SCREEN_RATIO[1], 'DEBUG MODE', FONT_DOGICAPIXEL12, COLOR_WHITE)
            pme.draw_text(5*GAME_SCREEN_RATIO[0], 14*GAME_SCREEN_RATIO[1], f'Magnitude(Speed): {round(self._get_magnitude(),4)}', FONT_DOGICAPIXEL10, COLOR_WHITE)
            pme.draw_text(5*GAME_SCREEN_RATIO[0], 26*GAME_SCREEN_RATIO[1], f'Position(Real): ({round(self.rect.x)}, {round(self.rect.y)}),         Position(Offset): ({round(self.offset_pos.x)}, {round(self.offset_pos.y)})', FONT_DOGICAPIXEL10, COLOR_WHITE)
            pme.draw_text(5*GAME_SCREEN_RATIO[0], 38*GAME_SCREEN_RATIO[1], f'Mouse Position: ({round(m_pos[0])}, {round(m_pos[1])}),         Mouse Buttons: ({pyg.mouse.get_pressed(5)})', FONT_DOGICAPIXEL10, COLOR_WHITE)
            # Requires Camera Setted
            if self.Camera:
                pme.draw_text(5*GAME_SCREEN_RATIO[0], 50*GAME_SCREEN_RATIO[1], f'Zoom: {self.Camera.zoom}', FONT_DOGICAPIXEL10, COLOR_WHITE) 
                # Draw Barriers
                # Top Barrier = Red
                pme.draw_rect(*self.Camera.convert2offset(pos=(0,0)),color=COLOR_RED,size=(GAME_MAP_SIZE[0],32),surface=self.Camera.internal_surf)

    def draw_menu(self):
        pme.draw_rect(0,472*GAME_SCREEN_RATIO[1],(50,50,50,128),(256*GAME_SCREEN_RATIO[0],128*GAME_SCREEN_RATIO[1]),border_width=3,border_color=(125,125,125,128))
        pme.draw_bar(5*GAME_SCREEN_RATIO[0],480*GAME_SCREEN_RATIO[1], (248, 18), [(90, 80, 65), (150, 70, 70), (255,250,250), (255,255,255)], self.health, self.maxhealth,text_font=FONT_DOGICAPIXEL12, text=f'{round(self.health)}/{round(self.maxhealth)}({round(self.health/self.maxhealth*100)}%)', border_thickness=3)
        pme.draw_text(5*GAME_SCREEN_RATIO[0], 502*GAME_SCREEN_RATIO[1], f'Level: {self.level}', FONT_DOGICAPIXEL12, COLOR_WHITE)
        pme.draw_text(5*GAME_SCREEN_RATIO[0], 522*GAME_SCREEN_RATIO[1], f'Experience: {round(self.experience)}/{round(self.level*100)}({round(self.experience/(self.level*100)*100)}%)', FONT_DOGICAPIXEL12, COLOR_WHITE)
        self.Isdebug()

    def update(self) -> None:
        self._manager_keyboard()
        self._manager_drag()
        self._manager_movment()
        self._manager_collision()
        self._limit_player()

    def save(self) -> dict:
        """
        Save all the important data of the player

        Parameters
            None
        Returns
            dict: data of the Player.
        """
        d = {}
        for key in self.__dict__:
            if key in self.saveable:
                d[key] = self.__dict__[key]
        return d
    
    def load(self, data:dict) -> None:
        """
        Load data from Database

        Parameters
            data (dict): data of the Player from the specified Save.
        Returns
            None
        """
        for key in self.saveable:
            if key in data:
                self.__dict__[key] = data[key]

# Save Class, Save, Load Everything in the game state
class Save():
    saveable = ['difficultyIndex','difficultyList','SaveIndex']

    # Define Types
    plr:player
    SaveIndex:int
    difficultyIndex:int
    difficultyList:list = ['Easy','Normal','Hard']

    def __init__(self,SaveIndex:int,difficulty:int) -> None:
        """
        Save Class, for Saving and Loading &nbsp;

        ↑+ Control
        """
        self.difficultyIndex = difficulty
        
        self.SaveIndex = SaveIndex

        self.plr = player(self)

    def createPlayer(self) -> player:
        """
        Create the player Object

        Parameters
            None
        Returns
            player: The player Object
        """
        p = player(self)
        return p
    
    def save(self) -> dict:
        """
        Get Player Data, and the own data, and finally, saves to Database, then return the data.

        Parameters
            None
        Returns
            dict: data of the Save.
        """
        d = {}
        for key in self.__dict__:
            if key in self.saveable:
                d[key] = self.__dict__[key]

        d['player'] = self.plr.save()


        db.add_values('saves',columns=['data'],values=[d])
        db.save()
        return d
    
    def load(self, data:dict) -> None:
        """
        Load the data from Database

        Parameters
            data (dict): data of the Save.
        Returns
            None
        """
        for key in self.saveable:
            if key in data:
                self.__dict__[key] = data[key]

        self.plr.load(data['player'])        