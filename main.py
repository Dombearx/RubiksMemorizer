import random
import time

from Scene import GameScene
from Cube import Cube

if __name__ == '__main__':

    # Config, should be in json
    title = "RubiksMemorizer"
    width = 1600
    height = 800

    game_scene = GameScene(title, width, height)
    cube = Cube()

    fps = 60
    animation_length = 0.5
    sound = 1
    sound_toggle = True

    # Map keyboard to rotate respective faces.
    while True:
        ev = game_scene.scene.waitfor('click keydown')
        if ev.event == 'click':
            sticker_number = random.randint(0, len(cube.stickers) - 1)

            t = time.time()
            # cube.animate_sticker(sticker_number, fps, animation_length)
            cube.animate_random_stickers(fps, animation_length)
            print("time", time.time() - t)