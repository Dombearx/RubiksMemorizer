from itertools import combinations
import pprint as pp
import random

from vpython import canvas, vector, color, button, winput, sleep, label

from Utils import save_to_file, read_pairs_file, read_cats_from_file, save_cats_to_file


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

    def read_pairs_from_file(self, filename):
        pairs, cats = read_cats_from_file(filename)

        self.pairs_cats = [
            {},
            {},
            {},
            {},
            {}
        ]

        for p, c in zip(pairs, cats):
            self.pairs_cats[c][p] = c

    def save_current_pairs_to_file(self, filename):

        data = []

        for dictionary in self.pairs_cats:
            for pair, cat in dictionary.items():
                data.append((pair, cat))

        save_cats_to_file(filename, data)

    def save_pairs_to_file_one(self):

        data = []

        for pair in self.corners_words.keys():
            data.append((pair, 0))
        for pair in self.sides_words.keys():
            data.append((pair, 0))

        save_cats_to_file("cats.txt", data)

    def read_pairs(self):
        filename = "words.txt"

        self.words = read_pairs_file(filename)

        self.corners_words = {}
        self.sides_words = {}

        # Remove count and categories rows
        del self.words[0]
        del self.words[0]
        for line in self.words:
            del line[0]

        column_number = 0
        for element_base in self.CORNERS_ORDER:
            corner_piece_base, sticker_base = element_base.split(":")
            if corner_piece_base not in self.PIECES_TO_IGNORE:
                row_number = 0
                for element_target in self.CORNERS_ORDER:
                    if not corner_piece_base == element_target.split(":")[0]:
                        corner_piece_target, sticker_target = element_target.split(":")
                        if corner_piece_target not in self.PIECES_TO_IGNORE:
                            self.corners_words[element_base + "-" + element_target] = self.words[row_number][
                                column_number]
                            row_number += 1
                column_number += 1

        column_number = 0
        for element_base in self.SIDES_ORDER:
            side_piece_base, sticker_base = element_base.split(":")
            if side_piece_base not in self.PIECES_TO_IGNORE:
                row_number = 0
                for element_target in self.SIDES_ORDER:
                    if not side_piece_base == element_target.split(":")[0]:
                        # print(element_base, element_target)
                        side_piece_target, sticker_target = element_target.split(":")
                        if side_piece_target not in self.PIECES_TO_IGNORE:
                            # print(element_base + "-" + element_target, row_number, column_number)
                            # self.cube.animate_pair_by_code(side_piece_base, side_piece_target, sticker_base, sticker_target, 60, 0.5)
                            self.sides_words[element_base + "-" + element_target] = self.words[row_number][
                                column_number]
                            row_number += 1
                column_number += 1

    def print_pieces(self, fps, animation_length):

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

    def play_round(self):
        p1, s1, p2, s2, label_pos = self.cube.animate_random_stickers(60, 0.5)
        self.label_pos = label_pos
        if len(p1) == 3:
            self.correct_word = self.corners_words[p1 + ":" + s1 + "-" + p2 + ":" + s2]
            words_to_draw = self.corners_words
        if len(p1) == 2:
            self.correct_word = self.sides_words[p1 + ":" + s1 + "-" + p2 + ":" + s2]
            words_to_draw = self.sides_words
        self.cwinput.disabled = False
        print("full code:", p1 + ":" + s1, p2 + ":" + s2)

        words = []
        words.append(self.correct_word)
        words.append(random.choice(list(words_to_draw.values())))
        words.append(random.choice(list(words_to_draw.values())))

        print(f"{self.correct_word = }")

        random.shuffle(words)

        print(words)

        self.b1.text = words[0]
        self.b2.text = words[1]
        self.b3.text = words[2]

    def get_user_input(self, v):
        print(v.text)

        self.cwinput.text = ""
        self.cwinput.disabled = True

        self.play_round()

    def check_answer(self, b):
        if b.text == "":
            return
        print("Your answer: ", b.text)
        if b.text == self.correct_word:
            self.correct()
        else:
            self.incorrect()
        self.b1.text = ""
        self.b2.text = ""
        self.b3.text = ""

        self.play_round()

    def correct(self):
        self.scene.background = color.green
        l = label(pos=self.label_pos, text=self.correct_word)
        sleep(1)
        l.visible = False
        self.scene.background = color.black

    def incorrect(self):
        self.scene.background = color.red
        l = label(pos=self.label_pos, text=self.correct_word)
        sleep(1)
        l.visible = False
        self.scene.background = color.black

    def __add_widgets(self):

        # cbutton = button(text='<b>Red</b>', color=color.red, background=color.cyan, pos=self.scene.title_anchor, bind=self.check_correction)
        self.cwinput = winput(bind=self.get_user_input, width=200)
        self.b1 = button(bind=self.check_answer, text="")
        self.b2 = button(bind=self.check_answer, text="")
        self.b3 = button(bind=self.check_answer, text="")
        self.start_button = button(bind=self.play_round, text="start game!")
