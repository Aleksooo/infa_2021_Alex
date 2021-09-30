import pygame as pg

WIDTH, HEIGHT = 600, 500

pg.init()
screen = pg.display.set_mode((WIDTH, HEIGHT))


def bird(center, scale):
    p = [[-3.71429, 14.4286], [-30.7143, 0.428571], [-21.7143, -16.5714], [1.28571, 4.42857], [20.2857, -16.5714], [31.2857, -2.57143], [3.28571, 16.4286]]
    p = [[i[0]*scale, i[1]*scale] for i in p]
    pos = [i + center for i in p]
    pg.draw.polygon(screen, (0, 0, 0), pos)


running = True

# Переменные
bg = (253, 213, 165)
ping_line = (253, 213, 198)
sun = (252, 236, 63)
orange_mountain = (250, 152, 63)
red_mountain = (170, 68, 56)
purple_line = (178, 135, 148)
black_mountain = (48, 17, 38)

m = []

while running:

    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1:
                print(pg.mouse.get_pos(), end=', ')
                m.append(pg.mouse.get_pos())

        if event.type == pg.KEYDOWN:
            if event.key == pg.K_SPACE:
                x = 0
                y = 0
                for i in m:
                    x += i[0]
                    y += i[1]
                x /= len(m)
                y /= len(m)
                c = pg.Vector2(x, y)
                print()
                for j in m:
                    print(j - c, end=', ')

    screen.fill(bg)

    # Рисование розовой линии
    pg.draw.rect(screen, ping_line, (0, 100, WIDTH, 150))
    # Рисование солнца
    pg.draw.circle(screen, sun, (WIDTH/2, 130), 50)
    # Рисование оранжевых гор
    pg.draw.polygon(screen, orange_mountain, [[13, 266], [25, 222], [161, 93], [206, 98], [241, 176], [288, 208], [383, 209], [417, 252]], )
    pg.draw.polygon(screen, orange_mountain, [(318, 252), (318, 220), (384, 190), (408, 148), (463, 128), (517, 127), (544, 87), (576, 109), (594, 163), (594, 258)])
    # Рисование красных гор
    pg.draw.polygon(screen, red_mountain, [(12, 327), (59, 219), (134, 196), (153, 270), (211, 290), (275, 294), (335, 277), (396, 270), (403, 229), (439, 246), (447, 223), (484, 234), (506, 203), (546, 219), (597, 155), (594, 289)])
    # Рисование фиолетовой линии
    pg.draw.polygon(screen, purple_line, [(12, 327), (594, 289), (600, 500), (0, 500)])
    # Рисование черных гор
    pg.draw.polygon(screen, black_mountain, [(7, 262), (66, 262), (86, 293), (104, 343), (128, 408), (146, 451), (190, 477), (269, 477), (310, 446), (334, 409), (368, 401), (410, 417), (432, 432), (471, 446), (522, 441), (547, 410), (556, 384), (565, 325), (572, 306), (598, 271), (596, 491), (2, 491)])

    # Отрисовка всех птиц
    bird(pg.Vector2(253, 201), 0.5)
    bird(pg.Vector2(169, 167), 0.5)
    bird(pg.Vector2(338, 241), 0.5)
    bird(pg.Vector2(426, 177), 0.5)
    bird(pg.Vector2(515, 137), 0.5)

    pg.display.update()
