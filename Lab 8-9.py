from math import e
import pygame as pg
from random import randint, choice

WIDTH, HEIGHT = 600, 500
FPS = 60

floor_heigth = 40

BG = (175, 218, 252)
WHEElS = (0, 0, 0)
GUN = (0, 0, 0)
BODY = (0, 128, 0)
FLOOR = (117, 51, 17)


class Tank:
    def __init__(self):
        self.pos = pg.Vector2(100, 430)
        self.velocity = pg.Vector2(2, 0)
        self.basic_color = GUN
        self.color = self.basic_color
        self.dC = 2

        self.gun_dir = pg.Vector2(1, 0)
        self.gun_length = 50
        self.gun_radius = 5

        self.body_width = 70
        self.body_height = 30

        self.wheel_radius = 15

        self.shoot_force = 0
        self.dF = 0.3

    def draw_gun(self, screen):
        ''' Функция отрисовывает башню танка. Рассчитывает вершины повернутого
        прямоугольника '''
        dir_perp = pg.Vector2(-self.gun_dir.y, self.gun_dir.x)
        gun_rect = (dir_perp*self.gun_radius,
                    self.gun_dir*self.gun_length + dir_perp*self.gun_radius,
                    self.gun_dir*self.gun_length - dir_perp*self.gun_radius,
                    -dir_perp*self.gun_radius)
        gun_rect = [self.pos + i for i in gun_rect]
        pg.draw.polygon(screen, self.color, gun_rect)

    def draw_body(self, screen):
        ''' Функция отрисовывает корпус танка '''
        body_rect = pg.Rect((self.pos.x - self.body_width / 2, self.pos.y - self.body_height / 2),
                            (self.body_width, self.body_height))
        pg.draw.rect(screen, BODY, body_rect)

    def draw_wheels(self, screen):
        ''' Функция отрисовывает два коллеса танка танка '''
        wheel_pos_left = pg.Vector2(-self.body_width* 3/8, self.body_height/2)
        wheel_pos_right = pg.Vector2(self.body_width * 3/8, self.body_height / 2)

        pg.draw.circle(screen, WHEElS, self.pos + wheel_pos_left, self.wheel_radius)
        pg.draw.circle(screen, WHEElS, self.pos + wheel_pos_right, self.wheel_radius)

    def draw(self, screen):
        ''' Функция вызывает все функции для отрисовки частей танка '''
        self.draw_gun(screen)
        self.draw_body(screen)
        self.draw_wheels(screen)

    def rotate_gun(self, mouse_pos):
        ''' Функция поворачивает башню, чтобы она следовала за мышью '''
        self.gun_dir = (mouse_pos - self.pos).normalize()

    def move(self, dir):
        ''' Функция двигает танк влево или вправо в зависимости от значения dir '''
        if dir == 'left':
            self.pos -= self.velocity
        elif dir == 'right':
            self.pos += self.velocity

    def update_color(self, start_shooting):
        ''' Функция изменяет цвет башни при нажатии мыши '''
        if start_shooting:
            self.color = (min(self.color[0]+self.dC, 255), self.color[1], self.color[2])
        else:
            self.color = self.basic_color

    def update_force(self, start_shooting):
        ''' Функция изменяет силу выстрела в зависимости от времени нажатия '''
        if start_shooting:
            self.shoot_force += self.dF
        else:
            self.shoot_force = 0

    def shoot(self):
        ''' Функция возвращает экземпляр класса "пули" при выстреле '''
        return Bullet(self.pos + self.gun_dir*self.gun_length, self.gun_dir*self.shoot_force)


class Bullet:
    def __init__(self, start_pos, velocity):
        self.pos = start_pos
        self.velocity = velocity
        self.friction = 0.6

        self.g_mag = 1
        self.g = pg.Vector2(0, 1)*self.g_mag

        self.radius = 10
        self.color = (randint(0, 255), randint(0, 255), randint(0, 255))

        self.life_time = 120
        self.time = 0
        self.time_to_die = False

    def update(self):
        ''' Функция двигает объект и удаляет его по истечению времени жизни '''
        self.velocity += self.g
        self.pos += self.velocity

        self.time += 1
        if self.time > self.life_time:
            self.time_to_die = True

    def draw(self, screen):
        ''' Функция отрисовывает снаряд '''
        pg.draw.circle(screen, self.color, self.pos, self.radius)

    def collide_border(self):
        ''' Функция проверяет столкновения с границами и отражает скорость при столкнивении '''
        if self.pos.x < self.radius:
            self.velocity.x *= -1
            self.velocity *= self.friction
            self.pos.x = self.radius
        elif self.pos.x >= WIDTH - self.radius:
            self.velocity.x *= -1
            self.velocity *= self.friction
            self.pos.x = WIDTH - self.radius

        if self.pos.y < self.radius:
            self.velocity.y *= -1
            self.velocity *= self.friction
            self.pos.y = self.radius
        elif self.pos.y >= HEIGHT - self.radius - floor_heigth:
            self.velocity.y *= -1
            self.velocity *= self.friction
            self.pos.y = HEIGHT - self.radius - floor_heigth


    def delete(self):
        ''' Функция возвращает себя же для удаления из списка '''
        self.time = 0
        self.time_to_die = False
        return self


class Target:
    def __init__(self):
        #self.pos = pg.Vector2(randint(51, WIDTH-51), randint(51, HEIGHT-51-floor_heigth))
        self.offset = 60
        self.movement_type = choice(['hor', 'ver'])

        if self.movement_type == 'hor':
            self.extreme_points = [randint(self.offset, WIDTH/2-self.offset), randint(WIDTH/2+self.offset, WIDTH-self.offset)]
            self.pos = pg.Vector2(randint(self.extreme_points[0], self.extreme_points[1]), randint(self.offset, HEIGHT-self.offset-floor_heigth))
            self.velocity = pg.Vector2(randint(-7, 7), 0)
        else:
            self.extreme_points = [randint(self.offset, HEIGHT/2-self.offset), randint(HEIGHT/2+self.offset, HEIGHT-self.offset-floor_heigth)]
            self.pos = pg.Vector2(randint(self.offset, WIDTH-self.offset), randint(self.extreme_points[0], self.extreme_points[1]))
            self.velocity = pg.Vector2(0, randint(-7, 7))

        self.color = choice([(155, 17, 30), (76, 187, 23), (18, 47, 170)])
        self.radius = randint(15, 30)
        self.time_to_die = False

    def update(self):
        ''' Функция двигает мишень по горизонтале или вертикали в зависимости о типа движения '''
        if self.movement_type == 'hor':
            if self.pos.x < self.extreme_points[0] or self.pos.x > self.extreme_points[1]:
                self.velocity *= -1
        else:
            if self.pos.y < self.extreme_points[0] or self.pos.y > self.extreme_points[1]:
                self.velocity *= -1

        self.pos += self.velocity

    def draw(self, screen):
        ''' Функция отрисовывает мишень '''
        pg.draw.circle(screen, self.color, self.pos, self.radius)

    def collide_bullet(self, bullets):
        ''' Функция проверяет столкновение со всеми снарядами '''
        for b in bullets:
            if pg.Vector2(b.pos - self.pos).length() <= b.radius + self.radius:
                self.time_to_die = True

    def delete(self):
        ''' Функция возвращает себя для удаления '''
        return self

pg.init()
screen = pg.display.set_mode((WIDTH, HEIGHT))
font = pg.font.Font(None, 30)
score_text = font.render('', True, (0, 0, 0))

tank = Tank()
bullets = []
targets = [Target()]

time = 0
delay = 150
score = 0
running = True
start_shooting = False

while running:
    screen.fill(BG)
    pg.time.Clock().tick(FPS)

    ''' Обработка всех нажатий '''
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1:
                start_shooting = True
        if event.type == pg.MOUSEBUTTONUP:
            if event.button == 1:
                start_shooting = False
                bullets.append(tank.shoot())

    # Движение танка
    if pg.key.get_pressed()[pg.K_LEFT] or pg.key.get_pressed()[pg.K_a]:
        tank.move('left')
    elif pg.key.get_pressed()[pg.K_RIGHT] or pg.key.get_pressed()[pg.K_d]:
        tank.move('right')
    # Поворот башни пушки
    tank.rotate_gun(pg.mouse.get_pos())
    # Обновление цвета и силы пушки
    tank.update_color(start_shooting)
    tank.update_force(start_shooting)
    # Отрисовка танка
    tank.draw(screen)

    # Обработка всех пуль
    for b in bullets:
        b.collide_border()
        b.update()
        b.draw(screen)
        if b.time_to_die:
            bullets.remove(b.delete())

    # Таймер для создания новых целей
    if time > delay:
        targets.append(Target())
        time = 0
    # Обработка всех целей
    for t in targets:
        t.collide_bullet(bullets)
        t.update()
        t.draw(screen)
        if t.time_to_die:
            targets.remove(t.delete())
            score += 1

    # Рисование пола
    pg.draw.rect(screen, FLOOR, pg.Rect(0, HEIGHT-floor_heigth, WIDTH, HEIGHT))

    # Отрисовка счета
    score_text = font.render('Счет:'+str(score), True, (0, 0, 0))
    screen.blit(score_text, (15, 15))

    pg.display.update()
    time += 1
