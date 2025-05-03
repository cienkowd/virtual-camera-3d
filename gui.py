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

    for obj in scene.get_objects():
        vertices = obj.get_transformed_vertices()
        edges = obj.get_edges()

        projected_points = []
        for v in vertices:
            transformed = tf.apply_transform(v, view_matrix)
            if transformed[2] <= 0.01:
                projected_points.append(None)
                continue
            projected = tf.apply_perspective(transformed, d=camera.zoom)

            scale = min(width, height)
            screen_x = int(projected[0] * scale + width / 2)
            screen_y = int(-projected[1] * scale + height / 2)
            projected_points.append((screen_x, screen_y))

        for edge in edges:
            i1, i2 = edge
            v1 = tf.apply_transform(vertices[i1], view_matrix)
            v2 = tf.apply_transform(vertices[i2], view_matrix)

            clipped = clip_line_z(np.array(v1), np.array(v2))
            if clipped is None:
                continue
            c1, c2 = clipped

            p1 = tf.apply_perspective(c1, d=camera.zoom)
            p2 = tf.apply_perspective(c2, d=camera.zoom)

            scale = min(width, height)
            x1 = int(p1[0] * scale + width / 2)
            y1 = int(-p1[1] * scale + height / 2)
            x2 = int(p2[0] * scale + width / 2)
            y2 = int(-p2[1] * scale + height / 2)

            pygame.draw.line(surface, color, (x1, y1), (x2, y2), 1)

    font = pygame.font.SysFont("consolas", 20)
    text = f"Camera: {camera.position.round(2)} | Zoom: {round(camera.zoom, 2)}"
    info = font.render(text, True, (255, 255, 255))
    bg = pygame.Surface((info.get_width() + 10, info.get_height() + 6))
    bg.set_alpha(100)
    bg.fill((0, 0, 0))
    surface.blit(bg, (5, 5))
    surface.blit(info, (10, 8))
    pygame.display.flip()
