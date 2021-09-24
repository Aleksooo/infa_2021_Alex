import pygame as pg
from random import random, randint

class ball:
    def __init__(self, pos, radius, color):
        self.pos = pos
        self.radius = radius
        self.color = color

        self.velocity = pg.Vector2(random()-0.5, random()-0.5).normalize() * 3
        self.dr = 0.1

    def update(self):
        self.pos += self.velocity
        self.radius += self.dr

    def collide_border(self):
        if self.pos.x <= self.radius or self.pos.x >= WIDTH-self.radius:
            self.velocity.x *= -1

        if self.pos.y <= self.radius or self.pos.y >= HEIGHT-self.radius:
            self.velocity.y *= -1

    def collide(self, obj):
        if pg.Vector2(self.pos - obj.pos).length() <= self.radius + obj.radius:
            dir = (obj.pos - self.pos).normalize()
            self.velocity = (self.velocity.normalize()-dir).normalize()*pg.Vector2(self.velocity).length()
            self.radius /= 2


    def draw(self, display):
        pg.draw.circle(display, self.color, self.pos, self.radius)


WIDTH, HEIGHT = 600, 500

pg.init()
screen = pg.display.set_mode((WIDTH, HEIGHT))

running = True
balls = [ball(pg.Vector2(randint(0, WIDTH), randint(0, HEIGHT)), randint(5, 15), (randint(0, 255), randint(0, 255), randint(0, 255))) for i in range(50)]

while running:
    screen.fill((100, 100, 150))

    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

    for b in balls:
        for obj in balls:
            if b != obj:
                b.collide(obj)

        b.collide_border()
        b.update()
        b.draw(screen)

    pg.display.update()
