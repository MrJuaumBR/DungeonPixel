from typing import List
from pygame import Surface
from pygame.rect import Rect
from ..config import *
from ..src.save import player as G_Player

class CameraGroup(pyg.sprite.Group):
    player:G_Player = None
    def __init__(self, *sprites, player:G_Player) -> None:
        super().__init__(*sprites)
        self.player = player

        self.add(player)

        self.display_surface = pyg.display.get_surface()

        self.offset = pyg.math.Vector2()
        self.half_w = self.display_surface.get_size()[0]//2
        self.half_h = self.display_surface.get_size()[1]//2

        # Zoom
        self.zoom = 1

        self.internal_surf_size = GAME_MAP_SIZE
        self.internal_surf = pyg.Surface(self.internal_surf_size,pyg.SRCALPHA)
        self.internal_rect = self.internal_surf.get_rect(center=(self.half_w,self.half_w))
        self.internal_surf_size_vector = pyg.math.Vector2(self.internal_surf_size)
        self.internal_offset = pyg.math.Vector2()
        self.internal_offset.x = self.internal_surf_size[0] // 2 - self.half_w
        self.internal_offset.y = self.internal_surf_size[1] // 2 - self.half_h

    def center_target_camera(self, target):
        self.offset.x = target.rect.centerx - self.half_w
        self.offset.y = target.rect.centery - self.half_h

    def zoom_keyboard_control(self):
        # More Zoom
        if (pme.key_pressed(K_PLUS) or pme.key_pressed(K_i)) or (pme.key_pressed(K_KP_PLUS) or pme.key_pressed(K_PAGEUP)):
            self.zoom += 0.05
            if self.zoom > 1.55:
                self.zoom = 1.55
        elif (pme.key_pressed(K_MINUS) or pme.key_pressed(K_o)) or (pme.key_pressed(K_KP_MINUS) or pme.key_pressed(K_PAGEDOWN)):
            self.zoom -= 0.05
            if self.zoom < 0.8:
                self.zoom = 0.8
        elif (pme.key_pressed(K_EQUALS) or pme.key_pressed(K_KP_EQUALS)):
            self.zoom = 1

    def convert2offset(self, sprite:pyg.sprite.Sprite=None, pos:tuple[float, float]=None) -> pyg.math.Vector2:
        if sprite is not None: # Sprite exists
            return tuple(sprite.rect.topleft) - self.offset + self.internal_offset
        elif pos is not None: # Position exists
            return pos - self.offset + self.internal_offset
        else:
            print("[CameraGroup - c2off] You need to pass a sprite or a position")
            return None

    def update(self):
        # Center the camera on the player
        self.center_target_camera(self.player)
        
        # Control the zoom level using keyboard input
        self.zoom_keyboard_control()

        # Update all sprites inside
        for sprite in self.sprites():
            try:
                if str.lower(sprite.type) != 'player':
                    sprite.update(self.player)
                else:
                    sprite.update()
            except Exception as e:
                print(e)

    def draw(self):

        # Fill the internal surface with a black color
        self.internal_surf.fill(COLOR_BLACK)


        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.y+sprite.layer): # Order by Y + layer
            try:
                offset_pos = self.convert2offset(sprite)
                self.internal_surf.blit(sprite.image, offset_pos)
                sprite.offset_pos = offset_pos
            except Exception as e:
                print(e)


         # Scale the internal surface based on the zoom scale
        scaled_surf = pyg.transform.scale(self.internal_surf, self.internal_surf_size_vector * self.zoom)
        scaled_rect = scaled_surf.get_rect(center=(self.half_w, self.half_h))

        # Blit the scaled surface onto the display surface
        self.display_surface.blit(scaled_surf, scaled_rect)

            
        