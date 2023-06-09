from pygame import *
from time import time as timer
from random import *
'''Шрифт'''
font.init()
font = font.SysFont('Times New Roman', 50)
win = font.render('YOU WIN!', True, (237,0, 8))
lose = font.render('YOU LOSE!', True, (237, 0, 8))
'''Переменные для картинок'''
img_back = 'back.jpg'
img_hero = 'hero1.png'
img_enemy = 'monster1.png'
img_goal = 'moneta.png'
img_bullet = 'bullet.png'
img_rock = 'rocket.png'
'''Музыка'''
#mixer.init()
#mixer.music.load('') #загружаем файл
#mixer.music.play()

'''Классы'''
#класс-родитель для других спрайтов
class GameSprite(sprite.Sprite):
    # конструктор класса
    def __init__(self, player_image, player_x, player_y, width, height, player_speed):
        #Вызываем конструктор класса (Sprite):
        sprite.Sprite.__init__(self)
        # каждый спрайт должен хранить свойство image - изображение
        self.image = transform.scale(image.load(player_image), (width, height))
        self.speed = player_speed
        # каждый спрайт должен хранить свойство rect - прямоугольник, в который он вписан
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    # метод, отрисовывающий героя на окне
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
class Player(GameSprite):
    def update(self):
        keys = key.get_pressed() # подключаем клавиатуру.
        if keys[K_a] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_d] and self.rect.x < win_width - 80:
            self.rect.x += self.speed
        if keys[K_w] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys[K_s] and self.rect.y < win_height - 80:
            self.rect.y += self.speed
    # метод 'выстрел' (используем место игрока, чтобы создать там пулю)
    def fire(self):
        bullet = Bullet(img_bullet, self.rect.right, self.rect.centery, 24, 25, 10)
        bullets.add(bullet)
    def fire2(self):
        bullet = Bullet(img_rock, self.rect.right, self.rect.centery, 24, 25, 10)
        bullets.add(bullet)

class Enemy(GameSprite):
    side = 'left'
    def update(self):
        if self.rect.x <= 470:
            self.side = 'right'
        if self.rect.x >= win_width - 85:
            self.side = 'left'
        if self.side == 'left':
            self.rect.x -= self.speed
        else:
            self.rect.x += self.speed
class Enemy2(GameSprite):
    side = 'up'
    def update(self):
        if self.rect.y <= 130:
            self.side = 'up'
        if self.rect.y >= win_height - 100:
            self.side = 'down'
        if self.side == 'down':
            self.rect.y -= self.speed
        else:
            self.rect.y += self.speed

class Wall(sprite.Sprite):
    def __init__(self, red, green, blue, wall_x, wall_y, wall_width, wall_height):
        super().__init__()
        self.red = red
        self.green = green
        self.blue = blue
        self.w = wall_width
        self.h = wall_height
        # каждый спрайт должен хранить свойство image - изображение
        self.image = Surface((self.w, self.h))
        self.image.fill((red, green, blue))
        # каждый спрайт должен хранить свойство rect - прямоугольник, в который он вписан
        self.rect = self.image.get_rect()
        self.rect.x = wall_x
        self.rect.y = wall_y
    def draw_wall(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Bullet(GameSprite):
    def update(self):
        self.rect.x += self.speed
        if self.rect.x > win_width + 10:
            self.kill()

'''Окно игры'''
#Создаём окошко
win_width = 800
win_height = 500
display.set_caption('Лабиринт')
window = display.set_mode((win_width, win_height))
back = transform.scale(image.load(img_back), (win_width, win_height))
'''Персонажи'''
hero = Player(img_hero, 5, win_height - 80, 65, 65, 10)
enemy = Enemy(img_enemy, win_width - 80, 280, 100, 65, 2)
enemy2 = Enemy2(img_enemy, 70, 200,100, 65, 2)
final = GameSprite(img_goal, win_width - 120, win_height - 80, 65, 65, 0)


'''Стены'''
w1 = Wall(154, 205, 50, 100, 20, 450, 10)
w2 = Wall(154, 205, 50, 100, 480, 350, 10)
w4 = Wall(154, 205, 50, 200, 130, 10, 200)
w5 = Wall(154, 205, 50, 450, 130, 10, 360)
w6 = Wall(154, 205, 50, 300, 20, 10, 30)
w7 = Wall(154, 205, 50, 390, 120, 130, 10)
w8 = Wall(154, 205, 50, 300, 130, 10, 200)
w9 = Wall(154, 205, 50, 200, 280, 10, 200)

'''Группы спрайтов'''
monsters = sprite.Group()
walls = sprite.Group()
bullets = sprite.Group()
'''Добавление спрайтов в группу'''
monsters.add(enemy)
monsters.add(enemy2)
walls.add(w2)
walls.add(w2)

walls.add(w4)
walls.add(w5)
walls.add(w6)
walls.add(w7)
walls.add(w8)
walls.add(w9)
points = 0
'''Игровй цикл'''
run = True
finish = False
clock = time.Clock()
FPS = 60
while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                hero.fire()
            elif e.key == K_TAB:
                hero.fire2()
    if finish != True:
        window.blit(back, (0, 0))
        walls.draw(window)
        monsters.update()
        monsters.draw(window)
        hero.reset()
        hero.update()
        final.reset()
        bullets.draw(window)
        bullets.update()
        sprite.groupcollide(bullets, walls, True, False)
        if sprite.groupcollide(bullets, monsters, True, True):
            points += 1
        x = font.render(str(points), True, (255, 255, 255))
        window.blit(x, (20, 20))

        if sprite.spritecollide(hero, walls, False):
            finish = True
            window.blit(lose, (200, 200))
        
        if sprite.spritecollide(hero, monsters, False):
            finish = True
            window.blit(lose, (200, 200))

        if sprite.collide_rect(hero, final):
            finish = True
            window.blit(win, (200, 200))
        
    display.update()
    clock.tick(FPS)