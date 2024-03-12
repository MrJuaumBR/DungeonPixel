import ini
import canvas
import engine

import sys

class CanvasRender:
    rectangle: canvas.Rectangle

class Entity:
    #@TODO: use canvas_render.rectangle for x,y,width,height for now but later change to entity.position, entity.dimension, etc...
    velocity: engine.VectorInteger
    canvas_render: CanvasRender

class GameState:
    main_character: Entity
    static_entity: Entity

def main():
    result = 1

    dictionary = ini.parse_ini("./data/chosenbit/data/config.ini")
    #@TODO: when nesting classes I got the same ref for certain class in the class chain. so i'm creating the classes manually
    game_state = GameState()
    game_state.main_character = Entity()
    game_state.main_character.canvas_render = CanvasRender()
    game_state.main_character.canvas_render.rectangle = canvas.Rectangle(100, 100, 100, 50, canvas.Color(1.0, 0.0, 0.0, 0.0))
    game_state.main_character.velocity = engine.VectorInteger(1, 1)
    game_state.static_entity = Entity()
    game_state.static_entity.canvas_render = CanvasRender()
    game_state.static_entity.canvas_render.rectangle = canvas.Rectangle(300, 100, 100, 50, canvas.Color(1.0, 1.0, 0.0, 0.0))    
    game_state.static_entity.velocity = engine.VectorInteger(0, 0)

    canvas_state = canvas.CanvasState
    canvas.create_canvas(canvas_state, "My Window", 800, 600)
    
    is_running = True
    message = canvas.Message
    while is_running:
        if not canvas.process_message(message):
            break

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
        canvas.draw_rectangle(canvas_state, static_entity_rectangle)
        canvas.swap_buffers(canvas_state)

    canvas.destroy_canvas(canvas_state)

    result = 0
    return result

if __name__ == "__main__":
    sys.exit(main())