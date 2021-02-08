#Game skeleton
#imports everything
import pygame
import os
import time
import random
WIDTH = 800
HEIGHT = 700
FPS = 100
#initializes pygame and prepares the window
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("My Game Is Below!")
Clock = pygame.time.Clock()
game_folder = os.path.dirname(__file__)
game_folder = os.path.join(game_folder,"Images")
bullet_folder = os.path.join(game_folder,"Items")
img_folder = os.path.join(game_folder,"Player")
eni_folder = os.path.join(game_folder,"Enemies")
move_folder = os.path.join(img_folder,"p1_walk")
print(move_folder)
move_images = ["p1_walk01.png","p1_walk02.png","p1_walk03.png","p1_walk04.png","p1_walk05.png","p1_walk06.png","p1_walk07.png"]
#list of colors
#RED,BLUE,GREEN
WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
YELLOW = (255,255,0)
CYAN = (0,255,255)
MAGENTA = (255,0,255)
running = True

#PLAYER IS DEIFINED,SHAPE,COLOR,ETC.

class Player(pygame.sprite.Sprite):
    #sprite for the user/player
    def __init__(self):

        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join(img_folder,"p1_jump.png")).convert()

        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH/2 , HEIGHT/2)

        self.image2 = pygame.image.load(os.path.join(bullet_folder,"bomb.png")).convert()
        self.rect2 = self.image2.get_rect()
        self.rect.center = ((WIDTH/2)+100  , (HEIGHT/2)+-100)


    def update(self):
        self.x = 0
        self.y = 0
        keystate = pygame.key.get_pressed()
        #Moving it
        if keystate[pygame.K_LEFT]:
            self.x = - 3
        if keystate[pygame.K_RIGHT]:
            self.x =  3
        if keystate[pygame.K_UP]:
            self.y = - 3
        if keystate[pygame.K_DOWN]:
            self.y =  3
        #bounce detection
        if self.rect.right > WIDTH  :

            self.rect.right = WIDTH
        if self.rect.left <= 0  :
            self.rect.x = 0
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= HEIGHT:
            self.rect.bottom = HEIGHT
        self.rect.x += self.x

        self.rect.top += self.y
        self.rect2.x +=self.x
    def shoot(self):
        bullet = Bullet(self.rect.centerx,self.rect.y)
        bullet.update()
        all_sprites.add(bullet)
        bullets.add(bullet)
class Mob(pygame.sprite.Sprite):
    def __init__(self):

        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join(eni_folder,"blockerMad.png")).convert()


        self.rect = self.image.get_rect()
        self.rect.center = (random.randrange(0,WIDTH),0)

        self.rect.x = random.randrange(0,WIDTH)
        self.rect.y = random.randrange(0,HEIGHT)

        self.speedy = random.randrange(-2,2)
        self.speedx = random.randrange(-1,1)
    def update(self):

        self.rect.y += self.speedy
        if self.rect.bottom > HEIGHT:
            self.rect.top = 0
        if self.rect.top < 0:
            self.rect.bottom = HEIGHT

        self.rect.x += self.speedx
        if self.rect.left > WIDTH:
            self.rect.right = 0
        if self.rect.right < 0:
            self.rect.left = WIDTH

time.sleep(0.5)
class Bullet(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join(bullet_folder,"gemGreen.png")).convert()

        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -5
    def update(self):
        self.rect.y +=self.speedy

        if self.rect.bottom < 0:
            self.kill()



player = Player()

all_sprites = pygame.sprite.Group()
all_sprites.add(player)
bullets  = pygame.sprite.Group()
mobs =      pygame.sprite.Group()
for i in range(3):
    m = Mob()
    all_sprites.add(m)
    mobs.add(m)
c = 0
#GAME LOOP
while running:
    Clock.tick(FPS)
    #PROCESS INPUT

    for event in pygame.event.get():
        #checks for closing window
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key  == pygame.K_SPACE:
                player.shoot()


    #UPDATE
    all_sprites.update()
    mobs.update()
    #checking for collision
    hits = pygame.sprite.groupcollide(mobs,bullets,True,True)
    for hit in hits:
        m = Mob()
        mobs.add(m)
        all_sprites.add(m)
    hits =  pygame.sprite.spritecollide(player,mobs, False)

    if hits:

        running = False
    #DRWA/RENDER
    screen.fill(BLACK)
    all_sprites.draw(screen)
    #flipping the board so that we draw on the other side while everyone sees the other side
    pygame.display.flip()
time.sleep(1)
pygame.quit()
