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
        self.color = color

    def get_transformed_vertices(self):
        t = tf.translate_matrix(*self.position)
        return [tf.apply_transform(v, t) for v in self.base_vertices]

    def get_edges(self):
        return self.edges

    def get_color(self):
        return self.color
