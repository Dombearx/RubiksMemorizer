from vpython import *

import random

scene = canvas(title='RubiksMemorizer',
               x=0, y=0, width=1600, height=800,
               center=vector(0, 0, 0), background=color.black)

scene.autoscale = False

scene.camera.pos = vector(3.85882, 3.31492, 5.88981)
scene.camera.axis = vector(-3.85882, -3.31492, -5.88981)

scene.userzoom = False
scene.userpan = False
scene.userspin = False
scene.lights = []


def animate_sticker(sticker_number, fps):
    hsv_color = color.rgb_to_hsv(stickers[sticker_number][0].color)
    original_color = hsv_color
    original_opacity = stickers[sticker_number][0].opacity

    flag = False
    animation = True

    v_change = ((1 - hsv_color.z) / fps) * 2

    mul = ((1 - hsv_color.x) / v_change) // 2
    hsv_color += mul * vector(0, 0, v_change)
    hsv_color.x = 0.8
    counter = 0

    stickers[sticker_number][0].opacity = 0.7
    stickers[sticker_number][0].color = color.hsv_to_rgb(hsv_color)

    while animation:
        rate(fps)
        v = hsv_color.z

        if not flag:
            hsv_color += vector(0, 0, v_change)
            if v >= 1:
                flag = True

        if flag:
            counter += 1
        if flag and counter > fps / 8:
            hsv_color -= vector(0, 0, v_change)

        stickers[sticker_number][0].color = color.hsv_to_rgb(hsv_color)

        if hsv_color.z <= original_color.z:
            animation = False

    stickers[sticker_number][0].color = color.hsv_to_rgb(original_color)
    stickers[sticker_number][0].opacity = original_opacity


def make_walls():
    # length_wall
    box(color=color.black, pos=vector(0, 0, -25),
        length=55, height=25, width=5)

    # floor
    box(color=color.black, pos=vector(0, -15, 0),
        length=55, height=5, width=55)

    # width_wall
    box(color=color.black, pos=vector(-25, 0, 0),
        length=5, height=25, width=55)


def make_lights():
    scene.lights = []
    local_light(pos=vector(25, 15, 25), color=color.gray(0.6))
    # sphere(pos=(25, 15, 25), radius=0.5)

    local_light(pos=vector(-25, 15, -25), color=color.gray(0.4))
    # sphere(pos=(-15, 15, -15), radius=0.5)

    local_light(pos=vector(0, -12, 0), color=color.gray(0.4))
    # sphere(pos=(0, -12, 0), radius=0.5)

    local_light(pos=vector(0, 12, 0), color=color.gray(0.4))
    # sphere(pos=(0, 15, 0), radius=0.5)


# Map keyboard keys to respective faces.
faces = {'r': (color.red, vector(0, 0, -1)),
         'o': (color.orange, vector(0, 0, 1)),
         'y': (color.yellow, vector(0, 1, 0)),
         'b': (vector(0.2, 0.2, 0.8), vector(1, 0, 0)),
         'w': (color.white, vector(0, -1, 0)),
         'g': (vector(0.2, 0.8, 0.2), vector(-1, 0, 0))}

# Create colored stickers on each face, one layer at a time.
stickers = []
corner_pieces = {}
side_pieces = {}

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

            sticker = box(emissive=True, color=face_color, pos=vector(x, y, 1.52),
                          length=l, height=h, width=0.03, opacity=o, text="asdasd")

            cos_angle = dot(vector(0, 0, 1), axis)
            pivot = (cross(vector(0, 0, 1), axis) if cos_angle == 0 else vector(1, 0, 0))
            sticker.rotate(angle=acos(cos_angle), axis=vector(pivot), origin=vector(0, 0, 0))
            if x != 0 or y != 0:
                stickers.append((sticker, color_key, sticker.pos))

            # back = box(color=color.gray(0.1), shininess=0.1, pos=vector(x, y, 1),
            #            length=1, height=1, width=1)
            # back.rotate(angle=acos(cos_angle), axis=vector(pivot), origin=vector(0, 0, 0))
            # stickers.append(back)


def vector_dist(vector_1, vector_2):
    dist_sum = 0
    dist_sum += abs(vector_1.x - vector_2.x)
    dist_sum += abs(vector_1.y - vector_2.y)
    dist_sum += abs(vector_1.z - vector_2.z)

    return round(dist_sum, 1)


for index in range(len(stickers)):

    if index < len(stickers):
        sticker, color_key, sticker_vector = stickers[index]
        closest = None
        c = []
        sticker.color = color.red
        sticker.opacity = 0.8

        for sticker_2, color_key_2, sticker_vector_2 in stickers:
            if sticker != sticker_2:
                sticker_2.color = color.blue
                sticker_2.opacity = 0.8
                # print(vector_dist(sticker_vector_2, sticker_vector))
                # x = input()
                if closest is None:
                    closest = vector_dist(sticker_vector_2, sticker_vector)
                else:
                    if vector_dist(sticker_vector_2, sticker_vector) < closest:
                        closest = vector_dist(sticker_vector_2, sticker_vector)

                sticker_2.color = color.gray(0.4)
                sticker_2.opacity = 0.3

        # print(f"{closest = }")
        for sticker_2, color_key_2, sticker_vector_2 in stickers:
            if sticker != sticker_2:
                if vector_dist(sticker_vector_2, sticker_vector) == closest:
                    c.append((sticker_2, color_key_2))

        pieces_num = 0
        for st, ck in c:
            if ck != color_key:
                pieces_num += 1
                st.color = color.blue
                st.opacity = 0.8
        # TODO dodać klasę do elementów, która potrafi zwrocić klucz na podstawie kolorów i listę naklejek z tego
        #  elementu. dodatkowo kolor dla każdej naklejki osobno też. I dodawać to do odpowiednich dict. Jakby tego było
        #  mało to jeszcze trzeba poprawić, żeby na pewno nie iterowało po tych elementach które już są w słownikach
        # if pieces_num == 1:
        #
        # if pieces_num == 2:


        x = input()
        for st, ck in c:
            if ck != color_key:
                st.color = color.gray(0.4)
                st.opacity = 0.3
        sticker.color = color.gray(0.4)
        sticker.opacity = 0.3

# make_walls()

# make_lights()

fps = 60
sound = 1
sound_toggle = True

# Map keyboard to rotate respective faces.
while True:
    ev = scene.waitfor('click keydown')
    if ev.event == 'click':
        print(scene.camera.pos)
        print(scene.camera.axis)
        sticker_number = random.randint(0, len(stickers) - 1)

        animate_sticker(sticker_number, 60)

        # if ev.pos in faces:
        #     face_color, axis = faces[ev.pos]
        #     angle = ((pi / 2) if ev.pos.isupper() else -pi / 2)
        #     for r in arange(0, angle, angle / fps):
        #         rate(fps * 6)
        #         for sticker in stickers:
        #             if dot(sticker.pos, axis) > 0.5:
        #                 sticker.rotate(angle=angle / fps, axis=axis,
        #                                origin=(0, 0, 0))
