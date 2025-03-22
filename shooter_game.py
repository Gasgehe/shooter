#Создай собственный Шутер!
from pygame import *
from random import randint
H = 500
W = 700
window = display.set_mode((W, H))
display.set_caption('Шутер')
bg = transform.scale(image.load('galaxy.jpg'), (W, H))


FPS = 120
clock = time.Clock()

score = 0
lost = 0

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (size_x, size_y))    
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y


    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_a] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_d] and self.rect.x < W - 85:
            self.rect.x += self.speed
    
    def fire(self):
        bullet = Bullet('bullet.png', self.rect.centerx, self.rect.top, 15, 20, 15)
        bullets.add(bullet)

class Enemy(GameSprite):
    def update(self):
        global lost
        self.rect.y += self.speed
        if self.rect.y > H:
            self.rect.y = 0
            self.rect.x = randint(80, W-80)
            lost += 1

class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()


mixer.init()
mixer.music.load('space.ogg')
mixer.music.set_volume(0.1)
mixer.music.play()

fire_sound = mixer.Sound('fire.ogg')

font.init()
font1 = font.SysFont('Arial', 36)
font2 = font.SysFont('Arial', 72)
text_lose = font2.render('YOU LOSE', 1, (245, 66, 66))
text_win = font2.render('YOU WIN', 1, (69, 245, 66) )

ship = Player('rocket.png', W//2, H-110, 80, 100, 5)
monsters = sprite.Group()
for i in range(5):
    monster = Enemy('ufo.png', randint(80, W - 80), - 40, 80, 50, randint(1, 3))
    monsters.add(monster)


bullets = sprite.Group()


game = True 
finish = False
while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                fire_sound.play()
                ship.fire()
    
    if finish != True:
        window.blit(bg, (0, 0))
  
        ship.reset()
        ship.update()
        bullets.update()
        monsters.update() 
        ship.reset()
        monsters.draw(window)
        bullets.draw(window)

        sprites_list = sprite.groupcollide(monsters, bullets, True, True)

        for i in sprites_list:
            score += 1
            monster = Enemy('ufo.png', randint(80, W - 80), - 40, 80, 50, randint(1, 3))
            monsters.add(monster)


        text_score = font1.render('Счет: ' + str(score), 1, (255, 255, 255))
        text_lost = font1.render('Пропущено: ' + str(lost), 1, (255, 255, 255))
        window.blit(text_score, (10, 20))
        window.blit(text_lost, (10, 50))



        if lost >= 3:
            window.blit(text_lose, (W//2 - 130, H/2 - 30))
            finish = True
        
        if score >= 10:
            window.blit(text_win, (W//2 - 130, H/2 - 30))
            finish = True 

        display.update()
    clock.tick(FPS)







