///jihaoya
import pygame
from pygame.locals import *
import time
import random


# 创建飞机的基类
class BasePlane(object):
    def __init__(self, screen, x, y, image):
        self.x = x
        self.y = y
        self.screen = screen
        self.image = pygame.image.load(image)
        self.is_hit = False  # 此标志用来表示飞机是否被击中了
        self.bullets = []

    def test(self, bullets):
        # 检测飞机被击中，子弹处于飞机的上
        for bullet in bullets:
            if self.x < bullet.x < self.x + self.image.get_width() and self.y < bullet.y < self.y + self.image.get_height():
                self.is_hit = True
        # 检测子弹碰撞
        for item in self.bullets:
            for bullet in bullets:
                if item.x < bullet.x < item.x + item.image.get_width() and item.y < bullet.y < item.y + item.image.get_height():
                    item.isHit = True
                    bullet.isHit = True


# 创建我方飞机
class HeroPlane(BasePlane):
    def __init__(self, screen, image="./feiji/hero1.png"):
        super().__init__(screen, 210, 700, image)
        # 控制飞机移动的函数

    def keyHander(self, keyValue):
        if keyValue == 'left':
            self.x -= 20
            if self.x <= 0:
                self.x = 0
        elif keyValue == 'right':
            self.x += 20
            if self.x >= 380:
                self.x = 380
        elif keyValue == "space":
            self.bullets.append(HeroBullet(self.screen, self.x + 40, self.y - 15))

    def display(self):
        self.screen.blit(self.image, (self.x, self.y))
        for bullet in self.bullets:
            if bullet.isHit:
                self.bullets.remove(bullet)
            else:
                bullet.display()
                bullet.move()
            if bullet.y <= 0:
                self.bullets.remove(bullet)


# 创建敌机类
class EnermyPlane(BasePlane):
    def __init__(self, screen, ):
        self.direciton = "right"
        self.bullets = []
        super().__init__(screen, 250, 0, "./feiji/enemy0.png")

    def display(self):
        self.screen.blit(self.image, (self.x, self.y))
        for item in self.bullets:
            if item.isHit:
                self.bullets.remove(item)
            else:
                item.display()
                item.move()
            if item.y > 852:
                self.bullets.remove(item)

    def move(self):
        if self.direciton == "right":
            self.x += 3
        elif self.direciton == "left":
            self.x -= 3
        if self.x > 430:
            self.direciton = "left"
        elif self.x <= 0:
            self.direciton = "right"

    def fire(self):
        num = random.randint(0, 150)
        if num in [0, 75]:
            self.bullets.append(EnermyBullet(self.screen, self.x + 25, self.y + 20))


# 创建子弹基类
class BaseBullet(object):
    def __init__(self, screen, x, y, image):
        self.x = x
        self.y = y
        self.screen = screen
        self.isHit = False
        self.image = pygame.image.load(image)

    def display(self):
        self.screen.blit(self.image, (self.x, self.y))


# 创建我方子弹类
class HeroBullet(BaseBullet):
    def __init__(self, screen, x, y):
        super().__init__(screen, x, y, "./feiji/bullet.png")

    def move(self):
        self.y -= 5


# 创建敌机子弹类
class EnermyBullet(BaseBullet):
    def __init__(self, screen, x, y):
        super().__init__(screen, x, y, "./feiji/bullet1.png")

    def move(self):
        self.y += 5


# 键盘控制飞机的坐标
def key_control(hero):
    for event in pygame.event.get():
        if event.type == QUIT:
            print("退出")
            exit()
        elif event.type == KEYDOWN:
            if event.key == K_a or event.key == K_LEFT:
                hero.keyHander("left")
                print("left")
            elif event.key == K_d or event.key == K_RIGHT:
                hero.keyHander("right")
                print("right")
            elif event.key == K_SPACE:
                hero.keyHander("space")
                print("space")


def main():
    # 创建一个窗口
    screen = pygame.display.set_mode((480, 852), 0, 32)
    # 设置背景图片
    bgImageFile = "./feiji/background.png"
    background = pygame.image.load(bgImageFile)
    pygame.display.set_caption('飞机大战')
    hero = HeroPlane(screen)
    enermy = EnermyPlane(screen)
    ''
    hero_nums = 0
    enermy_nums = 0
    while True:
        screen.blit(background, (0, 0))
        # 显示我方飞机
        hero.display()
        hero.test(enermy.bullets)
        if hero.is_hit:
            hero_nums += 1
            if hero_nums == 10:
                hero.image = pygame.image.load("./feiji/hero_blowup_n1.png")
            elif hero_nums == 20:
                hero.image = pygame.image.load("./feiji/hero_blowup_n2.png")
            elif hero_nums == 30:
                hero.image = pygame.image.load("./feiji/hero_blowup_n3.png")
            elif hero_nums == 40:
                hero.image = pygame.image.load("./feiji/hero_blowup_n4.png")
            elif hero_nums > 50:
                break
        # 显示敌机
        enermy.display()
        enermy.test(hero.bullets)
        if enermy.is_hit:
            enermy_nums += 1
            if enermy_nums == 10:
                enermy.image = pygame.image.load("./feiji/enemy0_down1.png")
            elif enermy_nums == 20:
                enermy.image = pygame.image.load("./feiji/enemy0_down2.png")
            elif enermy_nums == 30:
                enermy.image = pygame.image.load("./feiji/enemy0_down3.png")
            elif enermy_nums == 40:
                enermy.image = pygame.image.load("./feiji/enemy0_down4.png")
            elif enermy_nums > 50:
                enermy = EnermyPlane(screen)
                enermy_nums = 0
        else:
            enermy.move()
            enermy.fire()
        # 控制飞机的飞行方向
        key_control(hero)
        pygame.display.update()
        time.sleep(0.01)


if __name__ =='__main__':
    main()
