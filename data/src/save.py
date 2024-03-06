from ..config import *

class player(pyg.sprite.Sprite):
    saveable = []

    name = 'Zord'
    layer = 2

    can_collide = True
    type = 'player'

    offset_pos:pyg.math.Vector2
    def __init__(self, SaveClass,*groups) -> None:
        super().__init__(*groups)
        self.SaveClass = SaveClass

        self.size = (32,32)

        self.rect = Rect(0,0,*self.size)

    def save(self) -> dict:
        d = {}
        for key in self.__dict__:
            if key in self.saveable:
                d[key] = self.__dict__[key]
        return d
    
    def load(self, data) -> None:
        for key in self.saveable:
            if key in data:
                self.__dict__[key] = data[key]

class Save():
    saveable = ['difficultyIndex','difficultyList','SaveIndex']
    def __init__(self,SaveIndex:int,difficulty:int) -> None:
        self.difficultyIndex = difficulty
        self.difficultyList = ['Easy','Normal','Hard']
        
        self.SaveIndex = SaveIndex

        self.player = player(self)

    def createPlayer(self) -> player:
        p = player(self)
        return p
    
    def save(self) -> dict:
        d = {}
        for key in self.__dict__:
            if key in self.saveable:
                d[key] = self.__dict__[key]

        d['player'] = self.player.save()


        db.add_values('saves',columns=['data'],values=[d])
        db.save()
        return d
    
    def load(self, data) -> None:
        for key in self.saveable:
            if key in data:
                self.__dict__[key] = data[key]

        self.player.load(data['player'])        