import numpy as np


def translate_matrix(dx, dy, dz):
    return np.array([
        [1, 0, 0, dx],
        [0, 1, 0, dy],
        [0, 0, 1, dz],
        [0, 0, 0, 1]
    ])


def rotate_matrix_x(angle):
    return np.array([
        [1, 0, 0, 0],
        [0, np.cos(angle), -np.sin(angle), 0],
        [0, np.sin(angle), np.cos(angle), 0],
        [0, 0, 0, 1]
    ])


def rotate_matrix_y(angle):
    return np.array([
        [np.cos(angle), 0, np.sin(angle), 0],
        [0, 1, 0, 0],
        [-np.sin(angle), 0, np.cos(angle), 0],
        [0, 0, 0, 1]
    ])


def rotate_matrix_z(angle):
    return np.array([
        [np.cos(angle), -np.sin(angle), 0, 0],
        [np.sin(angle), np.cos(angle), 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1]
    ])


def scale_matrix(sx, sy, sz):
    return np.array([
        [sx, 0, 0, 0],
        [0, sy, 0, 0],
        [0, 0, sz, 0],
        [0, 0, 0, 1]
    ])


def apply_transform(point3d, matrix):
    vec = np.array([point3d[0], point3d[1], point3d[2], 1])
    transformed = matrix @ vec
    return transformed[:3]


def combine_transforms(*matrices):
    result = np.identity(4)
    for m in matrices:
        result = result @ m
    return result


def apply_perspective(point3d, d=1.0):
    x, y, z = point3d
    if z <= 0.01:
        z = 0.01
    return np.array([x / z, y / z]) * d


def inverse_matrix(matrix):
    return np.linalg.inv(matrix)
