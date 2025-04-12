import pygame
import transformations as tf


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
            projected = tf.apply_perspective(transformed, d=camera.zoom)

            scale = min(width, height)
            screen_x = int(projected[0] * scale + width / 2)
            screen_y = int(-projected[1] * scale + height / 2)
            projected_points.append((screen_x, screen_y))

        for edge in edges:
            start, end = edge
            pygame.draw.line(surface, color, projected_points[start], projected_points[end], 1)

    font = pygame.font.SysFont("consolas", 20)
    text = f"Camera: {camera.position.round(2)} | Zoom: {round(camera.zoom, 2)}"
    info = font.render(text, True, (255, 255, 255))
    bg = pygame.Surface((info.get_width() + 10, info.get_height() + 6))
    bg.set_alpha(100)
    bg.fill((0, 0, 0))
    surface.blit(bg, (5, 5))
    surface.blit(info, (10, 8))
    pygame.display.flip()
