import pygame
import random

pygame.init()

screen = pygame.display.set_mode((800, 600))

alien_image = pygame.Surface((30, 20))
alien_image.fill((255, 0, 0))

alien_rect = alien_image.get_rect(center=(400, 50))

screen.blit(alien_image, alien_rect)

clock = pygame.time.Clock()

bullets = []
aliens  = []
bullet_count = 0
max_bullets = 5
bullet_cooldown = 0
bullet_rate = 30

for row in range(5):
    for col in range(10):
        alien = alien_image.get_rect(x=col*50, y=row*40)
        aliens.append(alien)


class GameObject:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        
class Player(GameObject):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.player_image = pygame.Surface((50, 40))
        self.player_image.fill((255, 255, 255))
        self.player_rect = self.player_image.get_rect(center=(400, 550))
        self.draw(self.player_image, self.player_rect)
    
    def draw(self, player_image, player_rect):
        screen.blit(player_image, player_rect)


class Bullet(GameObject):
    x = 0
    y = 0
    bullet_image = pygame.Surface((5, 10))
    bullet_image.fill((255, 255, 255))
    bullet_count = 0
    bullet_cooldown = 0
    bullet = bullet_image.get_rect(center = (x, y))

    def __init__(self,x, y, top):
        super().__init__(x, y)
        self.bullet_image = pygame.Surface((5, 10))
        self.bullet_image.fill((255, 255, 255))
        self.bullet_image.get_rect(center = player.player_rect.center, width = 5, height = 10)
        self.bullet_count = 0
        bullet_cooldown = 0
        self.bullet = self.bullet_image.get_rect(center = (self.x, self.y))
        self.bullet_count += 1
        self.top = top
        self.draw()

    def draw(self):
        screen.blit(self.bullet_image, self.bullet)

    def move(self, x, y):
        self.x = x
        self.y = y


running = True
while running:
    player = Player(150, 550)
    bullet = Bullet(player.player_rect.center[0], player.player_rect.center[1], player.player_rect.top)
    clock.tick(60) # 60 fps
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player.x += -5
        player.player_rect.x -= 5
    if keys[pygame.K_RIGHT]:
        player.x += 5
        player.player_rect.x +=5
    if keys[pygame.K_SPACE] and bullet.bullet_cooldown <= 0: # and bullet_count < max_bullets 
        bullet = Bullet(player.player_rect.center[0], player.player_rect.center[1], player.player_rect.top)
        bullets.append(bullet)
        bullet.bullet_count += 1
        bullet.bullet_cooldown = bullet_rate

    bullet.bullet_cooldown -= 1
    if bullet.bullet_cooldown < 0:
        bullet.bullet_cooldown = 0
    # Clear the screen
    screen.fill((0, 0, 0)) 

    for alien in aliens:
        screen.blit(alien_image, alien)

    for alien in aliens:
        if random.randint(1,2) % 2:
            alien.x += 2
        else:
            alien.x -=2

    screen.blit(player.player_image, player.player_rect)
    screen.blit(alien_image, alien_rect)

    for bullet in bullets:
            bullet.move(0, -5)
            bullet.draw()
            if bullet.top < 0:
                bullets.remove(bullet)
    pygame.display.update()


