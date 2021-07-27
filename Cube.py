import copy
import time
import random

from vpython import vector, color, box, dot, cross, acos, rate


class Sticker:

    def __init__(self, element, side_color_key, position_vector):
        self.element = element
        self.side_color_key = side_color_key
        self.position_vector = position_vector

    def get_all_data(self):
        return self.element, self.side_color_key, self.position_vector

    def animate(self, fps, animation_length):
        dt = 1 / fps

        hsv_color = color.rgb_to_hsv(self.element.color)
        original_color = copy.copy(hsv_color)
        original_opacity = self.element.opacity

        original_v = hsv_color.z

        hsv_color.z = 1
        hsv_color.x = 0.8
        counter = 0

        self.element.opacity = 0.7
        self.element.color = color.hsv_to_rgb(hsv_color)

        v_change = (((hsv_color.z - original_v) / (1 / dt)) * 2) / animation_length

        # while not hsv_color.z <= original_color.z:
        #     rate(1 / dt)
        #     counter += dt
        #
        #     if counter >= animation_length / 2:
        #         hsv_color -= vector(0, 0, v_change)
        #
        #     self.element.color = color.hsv_to_rgb(hsv_color)

        t = time.time()
        animation_steps = animation_length * fps / 2

        one_step_length = (animation_length / 2) / animation_steps
        while not hsv_color.z <= original_color.z:

            rate(1 / dt)
            real_dt = time.time() - t

            counter += real_dt

            if counter >= animation_length / 2:
                # print("change")
                v_c = v_change * (real_dt / one_step_length)
                # print(f"{v_c=}")
                # print(f"{one_step_length=}")
                # print(f"{real_dt=}")
                hsv_color -= vector(0, 0, v_c)

            self.element.color = color.hsv_to_rgb(hsv_color)
            t = time.time()

        self.element.color = color.hsv_to_rgb(original_color)
        self.element.opacity = original_opacity

    def get_code(self):
        return self.side_color_key


class Piece:

    def __init__(self, *args):
        self.stickers = {}
        for sticker in args:
            self.stickers[sticker.side_color_key] = sticker

    def get_code(self):
        code = ""
        for sticker in self.stickers.values():
            code += sticker.side_color_key

        code = "".join(sorted(code))

        return code

    def get_random_sticker(self):
        return random.choice(list(self.stickers.values()))

    def get_sticker_by_code(self, code):
        return self.stickers[code]


class Cube:
    def __init__(self):
        # Map keyboard keys to respective faces.
        faces = {'r': (color.red, vector(0, 0, -1)),
                 'o': (color.orange, vector(0, 0, 1)),
                 'y': (color.yellow, vector(0, 1, 0)),
                 'b': (vector(0.2, 0.2, 0.8), vector(1, 0, 0)),
                 'w': (color.white, vector(0, -1, 0)),
                 'g': (vector(0.2, 0.8, 0.2), vector(-1, 0, 0))}

        # Create colored stickers on each face, one layer at a time.

        self.stickers = {}
        self.corner_pieces = {}
        self.side_pieces = {}

        i = 0
        for color_key, (side_color, axis) in faces.items():
            for x in (-1, 0, 1):
                for y in (-1, 0, 1):
                    face_color = color.gray(0.4)
                    l = 0.85
                    h = 0.85
                    o = 0.3
                    if x == y == 0:
                        face_color = side_color
                        l = 0.25
                        h = 0.25
                        o = 1

                    element = box(emissive=True, color=face_color, pos=vector(x, y, 1.52),
                                  length=l, height=h, width=0.03, opacity=o)

                    cos_angle = dot(vector(0, 0, 1), axis)
                    pivot = (cross(vector(0, 0, 1), axis) if cos_angle == 0 else vector(1, 0, 0))
                    element.rotate(angle=acos(cos_angle), axis=vector(pivot), origin=vector(0, 0, 0))
                    if x != 0 or y != 0:
                        self.stickers[i] = Sticker(element, color_key, element.pos)
                        i += 1

        self.__assign_pieces()

    def __vector_dist(self, vector_1, vector_2):
        dist_sum = 0
        dist_sum += abs(vector_1.x - vector_2.x)
        dist_sum += abs(vector_1.y - vector_2.y)
        dist_sum += abs(vector_1.z - vector_2.z)

        return round(dist_sum, 1)



    def __assign_pieces(self):

        keys = list(self.stickers.keys())

        while len(keys) > 0:

            sticker = self.stickers[keys[0]]

            element, color_key, position_vector = sticker.get_all_data()
            closest = None
            chosen_pieces = [sticker]

            for key, sticker_2 in self.stickers.items():
                element_2, color_key_2, sticker_vector_2 = sticker_2.get_all_data()
                if element != element_2:
                    if closest is None:
                        closest = self.__vector_dist(sticker_vector_2, position_vector)
                    else:
                        if self.__vector_dist(sticker_vector_2, position_vector) < closest:
                            closest = self.__vector_dist(sticker_vector_2, position_vector)

            for key, sticker_2 in self.stickers.items():
                element_2, color_key_2, sticker_vector_2 = sticker_2.get_all_data()
                if element != element_2:
                    if self.__vector_dist(sticker_vector_2, position_vector) == closest:
                        if color_key_2 != color_key:
                            chosen_pieces.append(Sticker(element_2, color_key_2, sticker_vector_2))
                            keys.remove(key)

            piece = Piece(*[stc for stc in chosen_pieces])

            if len(chosen_pieces) == 2:
                self.side_pieces[piece.get_code()] = piece
            if len(chosen_pieces) == 3:
                self.corner_pieces[piece.get_code()] = piece

            keys.remove(keys[0])

    def animate_sticker(self, sticker_number, fps, animation_length):
        self.stickers[sticker_number].animate(fps, animation_length)

    def animate_sticker_by_code(self, piece_code, sticker_code, fps, animation_length):
        if len(piece_code) == 3:
            self.corner_pieces[piece_code].get_sticker_by_code(sticker_code).animate(fps, animation_length)
        if len(piece_code) == 2:
            self.side_pieces[piece_code].get_sticker_by_code(sticker_code).animate(fps, animation_length)

    def animate_pair_by_code(self, piece_code1, piece_code2, sticker_code1, sticker_code2, fps, animation_length):
        if len(piece_code1) == 3:
            self.corner_pieces[piece_code1].get_sticker_by_code(sticker_code1).animate(fps, animation_length)
        if len(piece_code1) == 2:
            self.side_pieces[piece_code1].get_sticker_by_code(sticker_code1).animate(fps, animation_length)

        if len(piece_code2) == 3:
            self.corner_pieces[piece_code2].get_sticker_by_code(sticker_code2).animate(fps, animation_length)
        if len(piece_code2) == 2:
            self.side_pieces[piece_code2].get_sticker_by_code(sticker_code2).animate(fps, animation_length)

    def get_random_stickers(self):
        if random.randint(0, 1) == 0:
            # corner pieces
            random_piece1, random_piece2 = random.sample(list(self.corner_pieces.values()), 2)

        else:
            # side pieces
            random_piece1, random_piece2 = random.sample(list(self.side_pieces.values()), 2)

        print(random_piece1.get_code(), random_piece2.get_code())
        return random_piece1.get_random_sticker(), random_piece2.get_random_sticker(), random_piece1.get_code(), \
               random_piece2.get_code()

    def animate_random_stickers(self, fps, animation_length):
        random_sticker_1, random_sticker_2, code_1, code_2 = self.get_random_stickers()
        random_sticker_1.animate(fps, animation_length)
        random_sticker_2.animate(fps, animation_length)

        return code_1, random_sticker_1.get_code(), code_2, random_sticker_2.get_code()
