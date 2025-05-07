import numpy as np
import transformations as tf


class Box:
    def __init__(self, width=1.0, height=1.0, depth=1.0, position=None, color=(255, 255, 255)):
        w = width / 2
        h = height / 2
        d = depth / 2

        self.base_vertices = [
            np.array([w,  h,  d]),
            np.array([-w,  h,  d]),
            np.array([-w, -h,  d]),
            np.array([w, -h,  d]),
            np.array([w,  h, -d]),
            np.array([-w,  h, -d]),
            np.array([-w, -h, -d]),
            np.array([w, -h, -d])
        ]

        self.edges = [
            [0, 1], [1, 2], [2, 3], [3, 0],
            [4, 5], [5, 6], [6, 7], [7, 4],
            [0, 4], [1, 5], [2, 6], [3, 7]
        ]

        self.position = np.array(position if position is not None else [0.0, 0.0, 0.0])
        self.face_colors = [
            (255, 0, 0),  # front – czerwony
            (0, 255, 0),  # back – zielony
            (0, 0, 255),  # right – niebieski
            (255, 255, 0),  # left – żółty
            (0, 255, 255),  # top – cyan
            (255, 0, 255)  # bottom – magenta
        ]

    def get_transformed_vertices(self):
        t = tf.translate_matrix(*self.position)
        return [tf.apply_transform(v, t) for v in self.base_vertices]

    def get_edges(self):
        return self.edges

    def get_color(self):
        return self.color

    def get_faces(self):
        return [
            [3, 2, 1, 0],  # front — poprawiona
            [4, 5, 6, 7],  # back
            [0, 4, 7, 3],  # right
            [1, 2, 6, 5],  # left
            [1, 5, 4, 0],  # top
            [3, 7, 6, 2],  # bottom
        ]

    def get_face_colors(self):
        return [
            (255, 0, 0),  # front – czerwony
            (0, 255, 0),  # back – zielony
            (0, 0, 255),  # top – niebieski
            (255, 255, 0),  # bottom – żółty
            (0, 255, 255),  # right – cyan
            (255, 0, 255),  # left – magenta
        ]