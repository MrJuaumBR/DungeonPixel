import ini
import canvas
import engine

import sys
import os

class CanvasRender:
    rectangle: canvas.Rectangle

class Entity:
    #@TODO: use canvas_render.rectangle for x,y,width,height for now but later change to entity.position, entity.dimension, etc...
    position: engine.VectorInteger
    velocity: engine.VectorInteger
    canvas_render: CanvasRender

class GameConfig:
    last_write_time = 0

class GameState:
    main_character: Entity
    static_entity: Entity
    config_file: GameConfig

def main():
    result = 1
    ini_file_path = "./data/chosenbit/data/config.ini"
    ini_dictionary = ini.parse_file(ini_file_path)
    #@TODO: when nesting classes I got the same ref for certain class in the class chain. so i'm creating the classes manually
    game_state = GameState()
    game_state.config_file = GameConfig()
    game_state.config_file.last_write_time = os.path.getmtime(ini_file_path)
    game_state.main_character = Entity()
    game_state.main_character.canvas_render = CanvasRender()
    game_state.main_character.canvas_render.rectangle = canvas.Rectangle(100, 100, 100, 50, canvas.Color(1.0, 0.0, 0.0, 0.0))
    game_state.main_character.velocity = engine.VectorInteger(1, 1)
    game_state.main_character.position = engine.VectorInteger(0, 0)
    game_state.static_entity = Entity()
    game_state.static_entity.canvas_render = CanvasRender()
    game_state.static_entity.canvas_render.rectangle = canvas.Rectangle(300, 100, 100, 50, canvas.Color(1.0, 1.0, 0.0, 0.0))    
    game_state.static_entity.velocity = engine.VectorInteger(0, 0)
    game_state.static_entity.position = engine.VectorInteger(0, 0)
    #@TODO:Duplicate code
    ini_dictionary = ini.parse_file(ini_file_path)    
    game_state.static_entity.position.x = ini.read_integer(ini_dictionary, "GUI", "static_entity_x")
    game_state.static_entity.position.y = ini.read_integer(ini_dictionary, "GUI", "static_entity_y")

    canvas_state = canvas.CanvasState
    canvas.create_canvas(canvas_state, "My Window", 800, 600)
    
    is_running = True
    message = canvas.Message
    while is_running:
        if not canvas.process_message(message):
            break

        current_ini_last_write_time = os.path.getmtime(ini_file_path)
        if current_ini_last_write_time != game_state.config_file.last_write_time:
            #@TODO:Duplicate code
            ini_dictionary = ini.parse_file(ini_file_path)
            game_state.static_entity.position.x = ini.read_integer(ini_dictionary, "GUI", "static_entity_x")
            game_state.static_entity.position.y = ini.read_integer(ini_dictionary, "GUI", "static_entity_y")

            game_state.config_file.last_write_time = os.path.getmtime(ini_file_path)

        if canvas.is_key_down(message, "w"):
            pass
        elif canvas.is_key_down(message, "s"):
            pass
        else:
            pass

        if canvas.is_key_down(message, "a"):
            pass
        elif canvas.is_key_down(message, "d"):
            pass
        else:
            pass
        
        main_character_entity = game_state.main_character
        main_character_rectangle = main_character_entity.canvas_render.rectangle
        main_character_rectangle.x += main_character_entity.velocity.x
        main_character_rectangle.y += main_character_entity.velocity.y    
        
        if (main_character_rectangle.x <= 0) or (main_character_rectangle.x >= (800 - main_character_rectangle.width)):
            main_character_entity.velocity.x *= -1
        if (main_character_rectangle.y <= 0) or (main_character_rectangle.y >= (600 - main_character_rectangle.height)):
            main_character_entity.velocity.y *= -1

        canvas.draw_clear(canvas_state, canvas.Color(0.0, 0.0, 0.0, 0.0))
        canvas.draw_rectangle(canvas_state, main_character_rectangle)
        static_entity_rectangle = game_state.static_entity.canvas_render.rectangle
        static_entity_rectangle.x = game_state.static_entity.position.x
        static_entity_rectangle.y = game_state.static_entity.position.y
        canvas.draw_rectangle(canvas_state, static_entity_rectangle)
        canvas.swap_buffers(canvas_state)

    canvas.destroy_canvas(canvas_state)

    result = 0
    return result

if __name__ == "__main__":
    sys.exit(main())