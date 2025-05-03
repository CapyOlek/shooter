from pygame import *
from random import *
from time import time as timer
win_height = 500
win_width = 700
win = display.set_mode((win_width, win_height))
display.set_caption('shooter')
galaxy = transform.scale(image.load('galaxy.png'), (win_width, win_height))

lost = 0
score = 0
lives = 3
goal = 10
full_lost = 3


# text
font.init()
font1 = font.Font(None, 80)
font = font.Font(None, 35)

lose_txt = font1.render("YOU LOSE! ", 1, (250, 250, 250))

# music
mixer.init()
mixer.music.load('space.ogg')
mixer.music.set_volume(0.3)
mixer.music.play()
fire_sound = mixer.Sound('fire.ogg')


# class parent
class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        win.blit(self.image, (self.rect.x, self.rect.y))


class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width-70:
            self.rect.x += self.speed

    def fire(self):
        bullet = Bullet('bullet.png', self.rect.centerx, self.rect.top, 10, 20, -15)
        bullets.add(bullet)


class Enemy(GameSprite):

    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > win_height:
            self.rect.x = randint(70, win_width-70)
            self.rect.y = 0
            lost += 1


class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()


class Asteroid(GameSprite):

    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > win_height:
            self.rect.x = randint(70, win_width-70)
            self.rect.y = 0

# our sprites


asteroids = sprite.Group()
enemies = sprite.Group()
for i in range(1, 6):
    enemy = Enemy('enemy.png', randint(70, win_width-70), 0, 70, 35, randint(1, 6))
    enemies.add(enemy)
bullets = sprite.Group()
for i in range(1, 4):
    asteroid = Asteroid('asteroid.png', randint(70, win_width - 70), 0, 70, 35, randint(1, 5))
    asteroids.add(asteroid)


player = Player('rocket.png', 5, win_height - 100, 60, 90, 10)


game = True
finish = False
real_time = False
fire_num = 0
current_time = 0


while game:
    for i in event.get():
        if i.type == QUIT:
            game = False
        elif i.type == KEYDOWN:
            if i.key == K_SPACE:
                if fire_num < 5 and real_time == False:
                    fire_num += 1
                    fire_sound.play()
                    player.fire()
                if fire_num >= 5 and real_time == False:
                    last_time = timer()
                    real_time = True
    if not finish:
        win.blit(galaxy, (0, 0))
        # производим движения спрайтов
        player.update()
        bullets.update()
        asteroids.update()
        enemies.update()

        # обновляем их в новом местоположении при каждой итерации цикла
        player.reset()
        enemies.draw(win)
        asteroids.draw(win)
        bullets.draw(win)

        # change bullet

        if real_time == True:
            current_time = timer()
            if current_time - last_time < 3:
                reload = font1.render('WAIT, RELOAD', 1, (250, 250, 250))
                win.blit(reload, (100, 100))
            else:
                real_time = False
                fire_num = 0
        if sprite.spritecollide(player, asteroids, False) or sprite.spritecollide(player, enemies, False):
            sprite.spritecollide(player, enemies, True)
            sprite.spritecollide(player, asteroids, True)
            lives -= 1
        collides = sprite.groupcollide(enemies, bullets, True, True)

        for c in collides:
            score += 1
            enemy = Enemy('enemy.png', randint(70, win_width - 70), 0, 70, 35, randint(1, 5))
            enemies.add(enemy)

        if lives == 0 or lost >= full_lost:
            finish = True
            win.blit(lose_txt, (200, 200))
        if score >= goal:
            finish = True
            win_text = font1.render("YOU WON! ", 1, (250, 250, 250))
            win_text2 = font1.render("SCORE: " + str(score), 1, (250, 250, 250))
            win.blit(win_text, (200, 200))
            win.blit(win_text2, (200, 280))

        lose = font.render('MISSED: ' + str(lost), 1, (100, 100, 150))
        score_txt = font.render("SCORE: " + str(score), 1, (250, 250, 250))
        win.blit(lose, (20, 30))
        win.blit(score_txt, (20, 60))
        if lives == 3:
            life_color = (0, 200, 0)
        if lives == 2:
            life_color = (150, 150, 0)
        if lives == 1:
            life_color = (200, 0, 0)
        life_txt = font1.render(str(lives), 1, life_color)
        win.blit(life_txt, (650, 10))
        display.update()
    else:
        finish = False
        lost = 0
        score = 0
        lives = 3
        goal = 10
        full_lost = 3
        fire_num = 0
        for d in bullets:
            d.kill()
        for x in enemies:
            x.kill()
        for r in asteroids:
            r.kill()
        time.delay(3000)
        for i in range(1, 6):
            enemy = Enemy('enemy.png', randint(70, win_width - 70), 0, 70, 35, randint(1, 6))
            enemies.add(enemy)
        for i in range(1, 4):
            asteroid = Asteroid('asteroid.png', randint(70, win_width - 70), 0, 70, 35, randint(1, 5))
            asteroids.add(asteroid)
    # clock.tick(fps)
    time.delay(50)
