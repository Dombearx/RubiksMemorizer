from vpython import canvas, vector, color, box


class GameScene:

    def __init__(self, title, width, height):
        self.scene = canvas(title=title,
                       x=0, y=0, width=width, height=height,
                       center=vector(0, 0, 0), background=color.black)

        self.scene.autoscale = False

        # Hardcoded
        self.scene.camera.pos = vector(3.85882, 3.31492, 5.88981)
        self.scene.camera.axis = vector(-3.85882, -3.31492, -5.88981)

        self.scene.userzoom = False
        self.scene.userpan = False
        self.scene.userspin = False
        self.scene.lights = []


