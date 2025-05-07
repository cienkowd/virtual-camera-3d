import numpy as np
import pygame
import transformations as tf


def clip_line_z(p1, p2, z_clip=0.01):
    z1, z2 = p1[2], p2[2]
    if z1 > z_clip and z2 > z_clip:
        return p1, p2
    if z1 <= z_clip and z2 <= z_clip:
        return None

    t = (z_clip - z1) / (z2 - z1)
    interp = p1 + t * (p2 - p1)
    if z1 <= z_clip:
        return interp, p2
    else:
        return p1, interp


def render_scene(surface, scene, camera, color=(255, 255, 255)):
    width, height = surface.get_size()
    surface.fill((0, 0, 0))

    view_matrix = camera.get_view_matrix()
    faces_to_render = []

    for obj in scene.get_objects():
        vertices = obj.get_transformed_vertices()
        faces = obj.get_faces()
        face_colors = obj.get_face_colors()

        for face_index, face in enumerate(faces):
            face_vertices = [tf.apply_transform(vertices[i], view_matrix) for i in face]
            if any(v[2] <= 0.01 for v in face_vertices):
                continue

            normal = tf.face_normal(face_vertices[0], face_vertices[1], face_vertices[2])
            camera_vector = -face_vertices[0]
            if np.dot(normal, camera_vector) >= 0:
                continue  # Back-face culling

            projected = [tf.apply_perspective(v, d=camera.zoom) for v in face_vertices]
            screen_coords = [(int(p[0] * min(width, height) + width / 2),
                              int(-p[1] * min(width, height) + height / 2)) for p in projected]

            min_z = min(v[2] for v in face_vertices)
            faces_to_render.append((min_z, screen_coords, face_colors[face_index]))

    for _, points, color in sorted(faces_to_render, key=lambda x: x[0], reverse=True):
        pygame.draw.polygon(surface, color, points, width=0)
        pygame.draw.polygon(surface, (0, 0, 0), points, width=1)  # Optional outline for clarity

    font = pygame.font.SysFont("consolas", 20)
    text = f"Camera: {camera.position.round(2)} | Zoom: {round(camera.zoom, 2)}"
    info = font.render(text, True, (255, 255, 255))
    bg = pygame.Surface((info.get_width() + 10, info.get_height() + 6))
    bg.set_alpha(100)
    bg.fill((0, 0, 0))
    surface.blit(bg, (5, 5))
    surface.blit(info, (10, 8))
    pygame.display.flip()
