from ..config import *

# Game Player Sprite, Logic, and Load
class player(pyg.sprite.Sprite):
    saveable = ['name','rect','debug']

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

    debug:bool = False

    # Shown status
    def __init__(self, SaveClass,*groups) -> None:
        """
        Create the player handler, and Sprite for the game&nbsp;

        ↑+ Control;
        
        ↑+ Easy;
        """
        super().__init__(*groups)
        self.SaveClass = SaveClass
        try:
            self.Camera = self.groups()[0]
        except Exception as e:
            print(f'[Save - Player - Init] {e}')
            pass

        self.size = (32,32)

        self.rect = Rect(0,0,*self.size)

        self.image = pyg.Surface(self.size,pyg.SRCALPHA)
        self.image.fill((255,0,0,100))

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
    
    def _get_magnitude(self) -> float:
        """Same as player speed"""
        vector_x:float = self.position_vec.x
        vector_y:float = self.position_vec.y

        magnitude:float = (vector_x**2 + vector_y**2)**0.5
        return magnitude

    def _manager_movment(self):
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
            sprites = self.Camera.sprites()

            for sprite in sprites:
                if sprite is not self.Camera.player:
                    if self.rect.colliderect(sprite.rect):
                        a = self.rect
                        b = sprite.rect
                        # if x_overlap > 0 then there is an overlap in the x-axis
                        x_overlap = min(a.right, b.right) - max(a.x, b.x)
                        # if y_overlap > 0 then there is an overlap in the y-axis
                        y_overlap = min(a.bottom, b.bottom) - max(a.y, b.y)

                        # overlapd in the x-axis
                        if x_overlap < y_overlap:
                            if a.x < b.x: # collision from right to left?
                                a.x -= x_overlap                                
                            else: # collision from left to right?
                                a.x += x_overlap

                            if self.position_vec.x > 0:
                                self.position_vec.x = 0
                        # overlapd in the y-axis
                        else:
                            if a.y < b.y: # collsion from bottom to top?
                                a.y -= y_overlap
                            else: # collision from top to bottom?
                                a.y += y_overlap 
                            
                            if self.position_vec.y > 0:
                                self.position_vec.y = 0
        else: # If Camera Group Has Not Defined
            if len(self.groups()) > 0: # If Player Has Groups
                self.Camera = self.groups()[0] # Set Camera Group

    def Isdebug(self):
        if self.debug:
            pme.draw_text(5*GAME_SCREEN_RATIO[0], 1*GAME_SCREEN_RATIO[1], 'DEBUG MODE', FONT_DOGICAPIXEL12, COLOR_WHITE)
            pme.draw_text(5*GAME_SCREEN_RATIO[0], 14*GAME_SCREEN_RATIO[1], f'Magnitude(Speed): {round(self._get_magnitude(),4)}', FONT_DOGICAPIXEL10, COLOR_WHITE)
            pme.draw_text(5*GAME_SCREEN_RATIO[0], 26*GAME_SCREEN_RATIO[1], f'Position(Real): ({round(self.rect.x)}, {round(self.rect.y)})         Position(Offset): ({round(self.offset_pos.x)}, {round(self.offset_pos.y)})', FONT_DOGICAPIXEL10, COLOR_WHITE)

    def update(self) -> None:
        self._manager_keyboard()
        self._manager_drag()
        self._manager_movment()
        self._manager_collision()
        self.Isdebug()

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