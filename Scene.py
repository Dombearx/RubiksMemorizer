from itertools import combinations

from vpython import canvas, vector, color, button, winput


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

        self.__add_widgets()

    def set_cube(self, cube):
        self.cube = cube

    def check_correction(self, b):
        print("checking?", b.text)
        print(self.cwinput.text)

    def all_stickers(self, fps, animation_length):
        pieces_to_ignore = ["gry", "by"]

        corners_codes = sorted(self.cube.corner_pieces.keys())

        for code1 in corners_codes:
            if code1 not in pieces_to_ignore:
                for s1 in code1:
                    for code2 in corners_codes:
                        if code2 not in pieces_to_ignore:
                            if code1 != code2:
                                for s2 in code2:
                                    self.cube.animate_pair_by_code(code1, code2, s1, s2, fps, animation_length)



    def get_user_input(self, v):
        print(v.text)

        self.cwinput.text = ""
        self.cwinput.disabled = True
        p1, s1, p2, s2 = self.cube.animate_random_stickers(60, 0.5)
        self.cwinput.disabled = False
        print("full code:", p1 + ":" + s1, p2 + ":" + s2)

    def __add_widgets(self):

        # cbutton = button(text='<b>Red</b>', color=color.red, background=color.cyan, pos=self.scene.title_anchor, bind=self.check_correction)
        self.cwinput = winput(bind=self.get_user_input, width=200)

