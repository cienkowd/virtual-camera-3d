import numpy as np
import transformations as tf


class Camera:
    def __init__(self, position=None, zoom=1.0):
        self.position = position if position is not None else np.array([0.0, 0.0, -5.0])
        self.rotation_matrix = np.identity(4)
        self.zoom = zoom

    def get_view_matrix(self):
        s = tf.scale_matrix(self.zoom, self.zoom, self.zoom)
        t = tf.translate_matrix(-self.position[0], -self.position[1], -self.position[2])
        rot = tf.inverse_matrix(self.rotation_matrix)
        return tf.combine_transforms(s, rot, t)

    def get_direction_vectors(self):
        forward = tf.apply_transform(np.array([0, 0, 1]), self.rotation_matrix)
        right = tf.apply_transform(np.array([1, 0, 0]), self.rotation_matrix)
        up = tf.apply_transform(np.array([0, 1, 0]), self.rotation_matrix)
        return forward, right, up

    def move_local(self, dx, dy, dz):
        forward, right, up = self.get_direction_vectors()
        self.position += right * dx + up * dy + forward * dz

    def rotate_local(self, pitch, yaw, roll):
        pitch_matrix = tf.rotate_matrix_x(pitch)
        yaw_matrix = tf.rotate_matrix_y(yaw)
        roll_matrix = tf.rotate_matrix_z(roll)
        rotation_delta = tf.combine_transforms(roll_matrix, pitch_matrix, yaw_matrix)
        self.rotation_matrix = self.rotation_matrix @ rotation_delta

    def roll_local(self, angle):
        roll_matrix = tf.rotate_matrix_z(angle)
        self.rotation_matrix = self.rotation_matrix @ roll_matrix

    def zoom_in(self, factor=0.1):
        self.zoom = min(self.zoom * (1 + factor), 5.0)

    def zoom_out(self, factor=0.1):
        self.zoom = max(self.zoom / (1 + factor), 0.3)

    def reset_zoom(self):
        self.zoom = 1.0
