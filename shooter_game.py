#Создай собственный Шутер!
from pygame import *
from random import randint
from time import time as timer
#ГЛАВНЫЙ КЛАСС
class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y ,player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
#класс ракеты
class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_widht - 100:
            self.rect.x += self.speed
    def fire(self):
        bullet = Bullet('bullet.png', self.rect.centerx, self.rect.top, 15, 20, 15)
        bullets.add(bullet)
lost = 0
score = 0
#Класс врагов
class Enemy(GameSprite):
    def update(self):
       self.rect.y +=self.speed
       global lost
       if self.rect.y > win_height:
           self.rect.x = randint(80, win_widht - 80)
           self.rect.y = 0
           lost = lost + 1
#Класс пуль
class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()
#Класс астероидов 
class Asteroid(GameSprite):
    def update(self):
       self.rect.y +=self.speed
       global lost
       if self.rect.y > win_height:
           self.rect.x = randint(80, win_widht - 80)
           self.rect.y = 0
           lost = lost + 1
asteroids = sprite.Group() #группа астероидов
for i in range(1, 3):
    asteroid = Asteroid('asteroid.png', randint(100, 600), -30, 80, 100, randint(2, 4))
    asteroids.add(asteroid)
monsters = sprite.Group() #группа монстров         
ship = Player('rocket.png', 330, 395, 80, 100, 9)
for i in range(1, 6):
    monster = Enemy('ufo.png', randint(100, 600), -30, 80, 100, randint(4, 6))
    monsters.add(monster) 
bullets = sprite.Group() #группа пуль
#!ШРИФТ
font.init()
font1 = font.SysFont('Arial', 30)
font2 = font.SysFont('Arial', 80)
win = font2.render('ТЫ ПОБЕДИЛ ! ! !', 1, (255, 255, 0))
lose = font2.render('ТЫ ПРОИГРАЛ', 1, (170, 0, 0))
life_color = (255, 255, 255)

win_widht = 700 #размеры окна
win_height = 500
display.set_caption('CS 3')
window = display.set_mode((win_widht, win_height))
background = transform.scale(image.load('galaxy.jpg'), (win_widht, win_height))
finish = False
run = True
#TODOМУЗЫКА
mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
sound_fire = mixer.Sound('fire.ogg')
#Счётчик жизней
life = 3
#Перезарядка
num_fire = 0
rel_time = False
#Цикл игры
while run != False:
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                if num_fire < 5 and rel_time == False:
                    num_fire += 1
                    sound_fire.play()
                    ship.fire()
                    if num_fire >= 5 and rel_time == False:
                        last_time = timer()
                        rel_time = True
                
    if not finish:
        window.blit(background,(0, 0)) #фон
        #текст
        text_lose = font1.render('Пропущено:' + str(lost), 1, (255, 0 ,0))
        window.blit(text_lose, (10, 15))
        text_score = font1.render('Счёт:' + str(score), 1, (0, 255, 0))
        window.blit(text_score, (10, 45))
        text_life = font1.render('Количество жизней:' + str(life), 1, (life_color))
        window.blit(text_life, (405, 15))
        #Перезарядка
        if rel_time == True:
            now_time = timer()
            if now_time - last_time < 3:
                reload = font2.render('Wait, reload. . .', 1, (150, 0, 0))
                window.blit(reload, (220, 390))
            else:
                num_fire = 0
                rel_time = False
        asteroids.update()
        asteroids.draw(window)
        bullets.update()
        bullets.draw(window)
        monsters.update()
        monsters.draw(window)
        ship.update()
        ship.reset()
        sprite_list = sprite.groupcollide(monsters, bullets, True, True)
        collided_monsters = sprite.spritecollide(ship, monsters, True)
        collided_asteroids = sprite.spritecollide(ship, asteroids, True)
        if collided_monsters or collided_asteroids:
            life -= 1
            if life == 2:
                life_color = (255, 255, 0)
                text_life = font1.render('Количество жизней:' + str(life), 1, (life_color))
            if life == 1:
                life_color = (255, 0, 0)
                text_life = font1.render('Количество жизней:' + str(life), 1, (life_color))

        for i in sprite_list:
            score += 1
            monster = Enemy('ufo.png', randint(100, 600), -30, 80, 100, randint(4, 6))
            monsters.add(monster)
        if sprite.spritecollide(ship, monsters, False) or lost >= 10:
            window.blit(lose, (150, 240))
            finish = True
        if sprite.spritecollide(ship, asteroids, False):
            window.blit(lose, (150, 240))
            finish = True
        if score >= 20:
            window.blit(win, (110, 230))
            finish = True
        if life == 0:
            window.blit(lose, (110, 230))
            finish = True
        display.update()
    else:
        finish = False
        lost = 0
        score = 0
        life = 3
        life_color = (255, 255, 255)
        for b in bullets:
            b.kill()
        for m in monsters:
            m.kill()
        for a in asteroids:
            a.kill()
        time.delay(3000)
        for i in range(1, 6):
            monster = Enemy('ufo.png', randint(100, 600), -30, 80, 100, randint(4, 6))
            monsters.add(monster)
        for i in range(1, 3):
            asteroid = Asteroid('asteroid.png', randint(100, 600), -30, 80, 100, randint(2, 4))
            asteroids.add(asteroid)

   
    time.delay(50)