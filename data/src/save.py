from ..config import *
import math

# Game Player Sprite, Logic, and Load
class player(pyg.sprite.Sprite):
    saveable = ['name','rect']

    name = 'Zord'
    layer = 2

    can_collide = True
    type = 'player'

    Camera = None
    rect:pyg.rect.RectType

    offset_pos:pyg.math.Vector2 = pyg.math.Vector2()

    # Hidden Status

    speed:float = 0.3 # speed:int = 2
    drag:float = 0.65
    position_vec:pyg.math.Vector2 = pyg.math.Vector2()

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
        
    def _manager_movment(self):
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

    def _manager_collision(self):
        if self.Camera: # If Camera Group Has Defined
            for sprite in self.Camera.sprites(): # For Sprite in Camera Group
                if sprite.can_collide: # If Sprite can Collide with Player
                    if sprite.type != self.type: # If Sprite is not Player
                        if self.rect.colliderect(sprite.rect): # If Player collides with Sprite
                            dx = self.rect.x - sprite.rect.x
                            dy = self.rect.y - sprite.rect.y
                            angle = math.atan2(dy, dx)
                            adjustment_to_prevent_overlap = self.speed * 4.0
                            self.rect.x += self.position_vec.x + adjustment_to_prevent_overlap * math.cos(angle)
                            self.rect.y += self.position_vec.y + adjustment_to_prevent_overlap * math.sin(angle)
        else: # If Camera Group Has Not Defined
            if len(self.groups()) > 0: # If Player Has Groups
                self.Camera = self.groups()[0] # Set Camera Group

    def update(self) -> None:
        self._manager_keyboard()
        self._manager_drag()
        self._manager_movment()
        self._manager_collision()

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