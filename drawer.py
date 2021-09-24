import pygame as pg

WIDTH, HEIGHT = 600, 500

def refill():
    screen.fill((100, 100, 150))


pg.init()
screen = pg.display.set_mode((WIDTH, HEIGHT))
screen.fill((100, 100, 150))

running = True

colors = [(240, 0, 0), (0, 240, 0), (0, 0, 240), (255, 255, 255), (0, 0, 0), (200, 200, 0)]
picked_color = colors[0]

radius = 5

while running:

    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_SPACE:
                refill()

            if event.key == pg.K_UP:
                radius += 1
            elif event.key == pg.K_DOWN:
                radius -= 1

            if event.key == pg.K_1:
                picked_color = colors[0]
            elif event.key == pg.K_2:
                picked_color = colors[1]
            elif event.key == pg.K_3:
                picked_color = colors[2]
            elif event.key == pg.K_4:
                picked_color = colors[3]
            elif event.key == pg.K_5:
                picked_color = colors[4]
            elif event.key == pg.K_6:
                picked_color = colors[5]

    pressed = pg.mouse.get_pressed()
    pos = pg.mouse.get_pos()
    if pressed[0]:
        pg.draw.circle(screen, picked_color, pos, radius)
        pg.draw.line(screen, picked_color, pr_pos, pos, 2*radius+1)

    surface = pg.Surface((2*radius, 2*radius))
    surface.set_alpha(100)
    pg.draw.circle(surface, picked_color, (radius, radius), radius)

    pr_pos = pos

    screen.blit(surface, (20, 20))
    pg.display.flip()
    pg.display.update()
