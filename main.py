import pygame
from camera import Camera
from scene import Scene
from objects.box import Box
from gui import render_scene

WIDTH, HEIGHT = 800, 600
FPS = 60
MOVE_SPEED = 0.1
ROTATE_SPEED = 0.02
ZOOM_SPEED = 0.1


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Wirtualna kamera 3D")
    clock = pygame.time.Clock()

    camera = Camera()
    scene = Scene()
    scene.add_object(Box(1, 1, 1, position=[0, 0, 0]))
    scene.add_object(Box(2, 1, 0.5, position=[3, 0, 0]))
    scene.add_object(Box(0.5, 3, 1, position=[-3, -1, 1]))
    scene.add_object(Box(1.5, 0.5, 2.5, position=[0, 2, 3]))

    running = True
    while running:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:   camera.move_local(-MOVE_SPEED, 0, 0)
        if keys[pygame.K_RIGHT]:  camera.move_local(MOVE_SPEED, 0, 0)
        if keys[pygame.K_UP]:     camera.move_local(0, MOVE_SPEED, 0)
        if keys[pygame.K_DOWN]:   camera.move_local(0, -MOVE_SPEED, 0)
        if keys[pygame.K_w]:      camera.move_local(0, 0, MOVE_SPEED)
        if keys[pygame.K_s]:      camera.move_local(0, 0, -MOVE_SPEED)

        if keys[pygame.K_i]:      camera.rotate_local(-ROTATE_SPEED, 0, 0)
        if keys[pygame.K_k]:      camera.rotate_local(ROTATE_SPEED, 0, 0)
        if keys[pygame.K_a]:      camera.rotate_local(0, -ROTATE_SPEED, 0)
        if keys[pygame.K_d]:      camera.rotate_local(0, ROTATE_SPEED, 0)
        if keys[pygame.K_q]:      camera.roll_local(ROTATE_SPEED)
        if keys[pygame.K_e]:      camera.roll_local(-ROTATE_SPEED)
        if keys[pygame.K_r]:      camera.rotation[2] = 0.0

        if keys[pygame.K_z]:  camera.zoom_in(ZOOM_SPEED)
        if keys[pygame.K_c]:  camera.zoom_out(ZOOM_SPEED)
        if keys[pygame.K_x]:  camera.reset_zoom()

        render_scene(screen, scene, camera)

    pygame.quit()


if __name__ == "__main__":
    main()
