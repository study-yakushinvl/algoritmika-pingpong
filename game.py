from pygame import *
from random import randint
from time import sleep


window = display.set_mode((700,500))
display.set_caption('Ping-pong game')

background = transform.scale(image.load("background.jpeg"), (700,500))
clock = time.Clock()
FPS = 60
game = True

mixer.init()

font.init()
font2 = font.Font(None, 16)
font1 = font.Font(None, 36)
font = font.Font(None, 74)

win1 = font.render('Победа игрока 1', True, (0,0,200))
win2 = font.render('Победа игрока 2', True, (0,0,200))

mask = transform.scale(image.load('mask.png'), (700, 500))

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, wight, height, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (wight, height))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image,(self.rect.x, self.rect.y))



class Player(GameSprite):
    def update1(self):
        keys_pressed = key.get_pressed()
        if keys_pressed[K_w] and self.rect.y > 0:
            self.rect.y -= self.speed
        if keys_pressed[K_s] and self.rect.y < 500-129:
            self.rect.y += self.speed
        
    def update2(self, player22):
        if player22 == 'player':
            keys_pressed = key.get_pressed()
            if keys_pressed[K_UP]and self.rect.y > 0:
                self.rect.y -= self.speed
            if keys_pressed[K_DOWN] and self.rect.y < 500-129:
                self.rect.y += self.speed
        if player22 == 'bot':
            self.rect.y = ball.rect.y


player1 = Player('bar.png', 5, 500//2-(1280//10)//2, 318//5, (1280//10), 5)
player2 = Player('bar.png', (700-318//5)-5, 500//2-(1280//10)//2, 318//5, (1280//10), 5)
ball = GameSprite('ball.png', 330, 150, 100, 100, 0)
ball_x = 3
ball_y = 3


modes = False
finish = False
player22 = 'player'

while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
            finish = False
        if e.type == KEYDOWN:
            if e.key == K_ESCAPE:
                game = False
                finish = False
            if e.key == K_m and modes == False:
                modes = True
            elif e.key == K_m and modes == True:
                modes = False
            if e.key == K_p and player22 == 'player':
                player22 = 'bot'
            elif e.key == K_p and player22 == 'bot':
                player22 = 'player'
                
    window.blit(background, (0, 0))

    if modes:
        mode_text_player22 = font2.render('Второй игрок: '+str(player22), True, (150, 150, 150))
        window.blit(mode_text_player22, (5, 485))

    if ball.rect.y > 400 or ball.rect.y < 0:
        ball_y *= -1

    if sprite.collide_rect(ball, player1) or sprite.collide_rect(ball, player2):
        ball_x *= -1

    if ball.rect.x < -100:
        window.blit(win2, (135, 200))
        game = False
        finish = True
    elif ball.rect.x > 600:
        window.blit(win1, (135, 200))
        game = False
        finish = True

    ball.rect.x += ball_x
    ball.rect.y += ball_y
    player1.update1()
    player2.update2(player22)
    player1.reset()
    player2.reset()
    ball.reset()

    display.update()
    clock.tick(FPS)

    if game == False and finish:
        sleep(3)