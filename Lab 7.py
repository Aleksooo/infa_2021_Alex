import pygame as pg
from random import randint, random, choice

FPS = 60
WIDTH, HEIGHT = 680, 480
BG = (0, 68, 106)

class ball():
    def __init__(self):
        self.r = randint(30, 40)
        self.pos = pg.Vector2(randint(self.r, WIDTH-self.r), randint(self.r, HEIGHT/2))
        colors = {'red': (189, 30, 30),
                  'green': (37, 186, 37),
                  'brown': (227, 126, 64)}
        self.color_key = choice(['red', 'green', 'brown'])
        self.color = colors[self.color_key]
        velocity_mag = randint(5, 10)
        self.velocity = pg.Vector2(random()-0.5, -random()).normalize() * velocity_mag
        g_mag = 0.8
        self.g = pg.Vector2(0, 1) * g_mag

    def update(self):
        self.velocity += self.g
        self.pos += self.velocity

    def draw(self, screen):
        pg.draw.circle(screen, self.color, self.pos, self.r)

    def collide(self):
        if not(self.r < self.pos.x < WIDTH - self.r):
            self.velocity.x *= -1
            if self.pos.x < self.r:
                self.pos.x = self.r
            elif self.pos.x > WIDTH - self.r:
                self.pos.x = WIDTH - self.r
        if not(self.r < self.pos.y < HEIGHT - self.r):
            self.velocity.y *= -1
            if self.pos.y < self.r:
                self.pos.y = self.r
            elif self.pos.y > HEIGHT - self.r:
                self.pos.y = HEIGHT - self.r

    def click(self):
        if pg.Vector2(pg.mouse.get_pos()-self.pos).magnitude() <= 2*self.r:
            return True
        return False

    def score_value(self):
        if self.color_key == 'red':
            return 3
        elif self.color_key == 'green':
            return 2
        elif self.color_key == 'brown':
            return 1


pg.init()

screen = pg.display.set_mode((WIDTH, HEIGHT))
clock = pg.time.Clock()
score_text = pg.font.Font(None, 25)

finished = False
balls = []
tick = 0
last_tick = 0
delay = 1500

with open('data.txt', 'r') as data:
    score = int(data.readline())

while not finished:
    screen.fill(BG)
    clock.tick(FPS)

    for event in pg.event.get():
        if event.type == pg.QUIT:
            finished = True
            with open('data.txt', 'w') as data:
                data.write(str(score))
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_SPACE:
                balls.append(ball())
            if event.key == pg.K_ESCAPE:
                finished = True
                with open('data.txt', 'w') as data:
                    data.write(str(score))
        elif event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1:
                for i in balls:
                    if i.click():
                        score += i.score_value()
                        balls.remove(i)

    if tick - last_tick >= delay:
        balls.append(ball())
        last_tick = tick

    for i in balls:
        i.update()
        i.collide()
        i.draw(screen)

    text = score_text.render('Score:' + str(score), True, (255, 255, 255))
    screen.blit(text, (10, 10))
    pg.display.update()

    tick = pg.time.get_ticks()
