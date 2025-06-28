from random import randint

from numpy.ma.core import angle
from pygame import *

img_hero = "rocket.png"
img_bg = "galaxy.png"
img_enemy = "ufo.png"

WHITE = (255,255,255)

font.init()
font2 = font.Font(None, 28)

score = 0
lost = 0

# ==============
#  CLASSES
# ==============

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        sprite.Sprite.__init__(self)
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed

        self.original_image = self.image

        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image, (self.rect.x , self.rect.y))

class Player (GameSprite):
    def update(self):
        keys = key.get_pressed()
        angle = 0

        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
            angle = 15

        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed
            angle = -15

        self.image = transform.rotate(self.original_image, angle)
        old_center = self.rect.center
        self.rect = self.image.get_rect()
        self.rect.center = old_center

    def fire(self):  #TODO
        ...

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost

        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width-80)
            self.rect.y = -80
            self.speed = randint(2, 5)
            lost += 1

win_width = 900
win_height = 500
window = display.set_mode((win_width, win_height))
display.set_caption("SHOOT SHOOT SHOOT")
background = transform.scale(image.load(img_bg), (win_width, win_height))

player = Player(img_hero, win_width/2, win_height-100, 110, 100, 10)

monsters = sprite.Group()
count_of_monsters = 6

for i in range(count_of_monsters):
    monster = Enemy(img_enemy, randint(80, win_width-80),
                    -80, 60, 50, randint(2, 5))
    monsters.add(monster)

game = True
while game:
    for e in event.get():
        if e.type == QUIT:
            game = False

    window.blit(background, (0,0))

    text_score = font2.render(f"Рахунок: {score}", True, WHITE)
    window.blit(text_score, (10,20))

    text_lost = font2.render(f"Пропусків: {lost}", True, WHITE)
    window.blit(text_lost, (10, 50))

    player.update()
    player.reset()

    monsters.update()
    monsters.draw(window)

    display.update()