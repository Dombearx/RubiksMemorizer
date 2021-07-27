from itertools import combinations

from vpython import canvas, vector, color, button, winput


class GameScene:
    PIECES_TO_IGNORE = ["gry", "by"]

    CORNERS_ORDER = [
        "gry:y",
        "bry:y",
        "boy:y",
        "goy:y",
        "goy:o",
        "boy:o",
        "bow:o",
        "gow:o",
        "gry:g",
        "goy:g",
        "gow:g",
        "grw:g",
        "boy:b",
        "bry:b",
        "brw:b",
        "bow:b",
        "gow:w",
        "bow:w",
        "brw:w",
        "grw:w",
        "bry:r",
        "gry:r",
        "grw:r",
        "brw:r"
    ]

    SIDES_ORDER = [
        "ry:y",
        "by:y",
        "oy:y",
        "gy:y",
        "oy:o",
        "bo:o",
        "ow:o",
        "go:o",
        "gy:g",
        "go:g",
        "gw:g",
        "gr:g",
        "by:b",
        "br:b",
        "bw:b",
        "bo:b",
        "ow:w",
        "bw:w",
        "rw:w",
        "gw:w",
        "ry:r",
        "gr:r",
        "rw:r",
        "br:r"
    ]

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

    def print_pieces(self, fps, animation_length):
        corners_codes = sorted(self.cube.corner_pieces.keys())

        side_codes = sorted(self.cube.side_pieces.keys())

        print(corners_codes)
        print(side_codes)

        c = []
        s = []
        for element in self.CORNERS_ORDER:
            corner_piece, sticker = element.split(":")
            if corner_piece not in self.PIECES_TO_IGNORE:
                c.append(element)
                self.cube.animate_sticker_by_code(corner_piece, sticker, fps, animation_length)

        for element in self.SIDES_ORDER:
            corner_piece, sticker = element.split(":")
            if corner_piece not in self.PIECES_TO_IGNORE:
                s.append(element)
                self.cube.animate_sticker_by_code(corner_piece, sticker, fps, animation_length)

        print(c)
        print(s)

    def all_stickers(self, fps, animation_length):

        corners_codes = sorted(self.cube.corner_pieces.keys())

        for code1 in corners_codes:
            if code1 not in self.PIECES_TO_IGNORE:
                for s1 in code1:
                    for code2 in corners_codes:
                        if code2 not in self.PIECES_TO_IGNORE:
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
