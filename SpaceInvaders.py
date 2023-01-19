import pygame
import random
import os

pygame.init()
WIN_WIDTH = 800
WIN_HEIGHT = 600

screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption("Space Invaders")

BG_IMG = pygame.transform.scale(pygame.image.load(os.path.join("img","bg.bmp")).convert_alpha(), (600, 900))
PLAYER_IMG = pygame.transform.scale(pygame.image.load(os.path.join("img","ship.bmp")).convert_alpha(), (50, 30))
ALIEN_IMG = pygame.transform.scale(pygame.image.load(os.path.join("img","alien.bmp")).convert_alpha(), (50, 30))

bullet_image = pygame.Surface((5, 10))
bullet_image.fill((255, 255, 255))

player_rect = PLAYER_IMG.get_rect(center=(400, 550))
alien_rect = ALIEN_IMG.get_rect(center=(400, 50))

class GameObject:
    def __init__(self, x, y):
        self.x = x
        self.y = y
class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.image = PLAYER_IMG
        self.rect = self.image.get_rect(center=(x, y))
        self.bullets = []
        self.bullet_cooldown = 0
        self.bullet_rate = 30

    def move_left(self):
        self.rect.x -= 5

    def move_right(self):
        self.rect.x += 5

    def shoot(self):
        if self.bullet_cooldown <= 0:
            bullet = bullet_image.get_rect(center = self.rect.center)
            self.bullets.append(bullet)
            self.bullet_cooldown = self.bullet_rate
    
    def update(self):
        self.bullet_cooldown -= 1
        if self.bullet_cooldown < 0:
            self.bullet_cooldown = 0
        for bullet in self.bullets:
            bullet.move_ip(0, -5)
            if bullet.top < 0:
                self.bullets.remove(bullet)
                self.bullet_cooldown = self.bullet_rate

    
screen.blit(PLAYER_IMG, player_rect)
screen.blit(ALIEN_IMG, alien_rect)

clock = pygame.time.Clock()

aliens = []
for row in range(5):
    for col in range(10):
        alien = ALIEN_IMG.get_rect(x=col*50, y=row*40)
        aliens.append(alien)

player = Player(screen.get_width()/2, screen.get_height()-50)
running = True
while running:
    clock.tick(60) # 60 fps

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT]:
        player.move_left()
    if keys[pygame.K_RIGHT]:
        player.move_right()
    if keys[pygame.K_SPACE] and player.bullet_cooldown <= 0:
        player.shoot()

    screen.fill((0, 0, 0)) # Clear the screen
    screen.blit(PLAYER_IMG, player.rect)
    
    for alien in aliens:
        rnd = random.randint(1,2)
        screen.blit(ALIEN_IMG, alien)
        for alien in aliens:
            if rnd % 2 == 0:
                alien.x = alien.x + 2 if alien.x > 10 else alien.x - 2
            else:
                alien.x = alien.x - 2 if alien.x > 10 else alien.x + 2
        

    for bullet in player.bullets:
        bullet.move_ip(0, -5)
        screen.blit(bullet_image, bullet)
        if bullet.top < 0:
            player.bullets.remove(bullet)

    pygame.display.update()





