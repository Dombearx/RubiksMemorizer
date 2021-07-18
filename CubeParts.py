from vpython import box, vector
import numpy as np

class Panel:

    def __init__(self, pos, size, color, opacity):
        self.panel = box(pos=vector(*pos), size=vector(*size), color=color, opacity=opacity)

    def change_color(self, color):
        self.panel.color = color

    def rotate(self, angle):
        self.panel.rotate(angle)


class Side:

    def __init__(self, pos, size, color, opacity, gap):
        thickness, width, height = size
        x, y, z = pos

        panel_width = width // 3
        panel_height = height // 3

        self.panels = np.empty(shape=(3, 3), dtype=Panel)

        for line in range(3):
            for column in range(3):
                p = (Panel((x, y + column * panel_width, z + line * panel_height),
                                    (thickness, panel_width, panel_height), color, opacity))
                self.panels[line, column] = p

    def rotate(self, angle):
        for line in range(3):
            for column in range(3):
                self.panels[line, column].rotate(angle)
