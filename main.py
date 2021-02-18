import pymunk
import pymunk.pygame_util
from color import *
from random import *
from game import *
from pygame.locals import *


class Window(game):
    def __init__(self, width, height, title='game'):
        game.__init__(self, width, height, title)
        self.__state = 1
        pygame.init()
        self.size = [
            [10, yellow, 0],
            [15, blue, 1],
            [20, pink, 2],
            [25, red, 4],
            [30, gold, 8],
            [35, purple, 16],
            [40, gray, 32],
            [45, orange, 64],
            [50, green, 128],
            [55, white, 256]
        ]
        self.click = 0
        self.time = 0
        self.t = 0
        self.x = 0
        self.b = 0
        self.big = 0
        self.ball = []
        self.static_lines = []
        self.space = pymunk.Space()
        self.space.gravity = (0, 900)
        self.add_static()
        self.draw_options = pymunk.pygame_util.DrawOptions(self.screen)
        self.clock = pygame.time.Clock()
        self.update()

    def random(self):
        return randint(0, self.big)

    def fraction(self):
        text = pygame.font.SysFont("宋体", 30)
        text_fmt = text.render(str(self.t), True, white)
        self.screen.blit(text_fmt, (5, 5))

    def add_ball(self):
        mass = self.size[self.b][0]
        radius = self.size[self.b][0]
        inertia = pymunk.moment_for_circle(mass, 0, radius)
        body = pymunk.Body(mass, inertia)
        body.position = self.x, self.size[self.b][0]
        shape = pymunk.Circle(body, radius, (0, 0))
        shape.elasticity = 0.8
        shape.color = pygame.Color(self.size[self.b][1])
        shape.friction = 0.8
        self.space.add(body, shape)
        return shape

    def new_ball(self, x, y, t):
        if t < 55:
            t += 5
        mass = t  # mass是物体的质量
        radius = t  # radius是球体的半径
        inertia = pymunk.moment_for_circle(mass, 0, radius)  # 根据质量半径计算物体的惯性
        body = pymunk.Body(mass, inertia)  # 根据质量和惯性生成一个物体
        body.position = x, y  # 设置物体的生成位置
        shape = pymunk.Circle(body, radius, (0, 0))  # 给物体赋予球形
        shape.elasticity = 0.8  # 弹性系数 0-1,0为没有弹性
        for i in self.size:
            if i[0] == t:
                if 5 > self.size.index(i) > self.big:
                    self.big += 1
                shape.color = pygame.Color(i[1])
                self.t += i[2]
        shape.friction = 0.8  # 摩擦系数 0-1,0为无摩擦
        self.space.add(body, shape)  # 把实体,形状添加到物理空间
        return shape

    def add_static(self):
        static_lines = [
            pymunk.Segment(self.space.static_body, (0, self.height), (self.width, self.height), 0),
            pymunk.Segment(self.space.static_body, (-1, 0), (-1, self.height), 0),
            pymunk.Segment(self.space.static_body, (self.width, 0), (self.width, self.height), 0),
            pymunk.Segment(self.space.static_body, (0, -1), (self.width, 0), 0)
        ]
        for i in static_lines:
            i.elasticity = 0.8
            i.friction = 0.8
            self.space.add(i)
            self.static_lines.append(i)

    def interface(self):
        pygame.draw.circle(self.screen, self.size[self.b][1], [self.x, self.size[self.b][0]], self.size[self.b][0], 0)

    def key(self):
        if self.click == 1:
            self.time += 1
            if self.time >= 50:
                self.click = 0
        for event in pygame.event.get():
            self.x = pygame.mouse.get_pos()[0]
            if self.x < 0 + self.size[self.b][0]:
                self.x = 0 + self.size[self.b][0]
            if self.x > self.width - self.size[self.b][0]:
                self.x = self.width - self.size[self.b][0]
            if event.type == QUIT:
                self.__state = 0
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if self.click == 0:
                        self.click = 1
                        self.ball.append(self.add_ball())
                        self.b = self.random()

    def collision(self):
        dell_ball = []
        new_x = -100
        new_y = -100
        t = 0
        for i in self.ball:
            x, y = i.body.position.x, i.body.position.y
            for u in self.ball:
                a, b = u.body.position.x, u.body.position.y
                if (x, y) == (a, b):
                    continue
                if (x - a) ** 2 + (y - b) ** 2 < (i.body.mass + u.body.mass) ** 2 and u.body.mass == i.body.mass:
                    t = int(u.body.mass)
                    dell_ball.append(u)
                    if y > b:
                        new_x, new_y = x, y
                    else:
                        new_x, new_y = a, b
        if new_x > 0:
            self.ball.append(self.new_ball(new_x, new_y, t))
        dell_ball = set(dell_ball)
        for i in dell_ball:
            self.ball.remove(i)
            self.space.remove(i, i.body)

    def update(self):
        while self.__state:
            self.collision()
            self.key()
            self.screen.fill((0, 0, 0))
            self.interface()
            self.draw_options = pymunk.pygame_util.DrawOptions(self.screen)
            self.space.debug_draw(self.draw_options)
            self.fraction()
            self.space.step(1 / 60)
            pygame.display.flip()
            self.clock.tick(60)
        pygame.quit()


if __name__ == '__main__':
    Window(250, 400, '合成大球球')
