import numpy as np
import transformations as tf


class Camera:
    def __init__(self, position=None, rotation=None, zoom=1.0):
        self.position = position if position is not None else np.array([0.0, 0.0, -5.0])
        self.rotation = rotation if rotation is not None else np.array([0.0, 0.0, 0.0])
        self.zoom = zoom

    def get_view_matrix(self):
        s = tf.scale_matrix(self.zoom, self.zoom, self.zoom)

        yaw = tf.rotate_matrix_y(-self.rotation[1])
        pitch = tf.rotate_matrix_x(-self.rotation[0])
        roll = tf.rotate_matrix_z(-self.rotation[2])

        t = tf.translate_matrix(-self.position[0], -self.position[1], -self.position[2])

        view_rotation = tf.combine_transforms(pitch, yaw, roll)

        return tf.combine_transforms(s, view_rotation, t)

    def get_direction_vectors(self):
        rx = tf.rotate_matrix_x(self.rotation[0])
        ry = tf.rotate_matrix_y(self.rotation[1])
        rz = tf.rotate_matrix_z(self.rotation[2])
        rotation_matrix = tf.combine_transforms(rz, ry, rx)

        forward = tf.apply_transform(np.array([0, 0, 1]), rotation_matrix)
        right = tf.apply_transform(np.array([1, 0, 0]), rotation_matrix)
        up = tf.apply_transform(np.array([0, 1, 0]), rotation_matrix)

        return forward, right, up

    def move_local(self, dx, dy, dz):
        forward, right, up = self.get_direction_vectors()
        self.position += right * dx + up * dy + forward * dz

    def rotate_local(self, pitch, yaw, roll):
        self.rotation += np.array([pitch, yaw, roll])

    def roll_local(self, angle):
        rx = tf.rotate_matrix_x(self.rotation[0])
        ry = tf.rotate_matrix_y(self.rotation[1])
        rotation_matrix = tf.combine_transforms(ry, rx)

        forward = tf.apply_transform(np.array([0, 0, 1]), rotation_matrix)

        self.rotation[2] += angle

    def zoom_in(self, factor=0.1):
        self.zoom = min(self.zoom * (1 + factor), 5.0)

    def zoom_out(self, factor=0.1):
        self.zoom = max(self.zoom / (1 + factor), 0.3)

    def reset_zoom(self):
        self.zoom = 1.0
