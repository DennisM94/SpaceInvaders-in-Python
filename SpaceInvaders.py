import pygame
import random
import os

pygame.init()
WIN_WIDTH = 1280
WIN_HEIGHT = 720
STAT_FONT = pygame.font.SysFont("comicsans", 50)

screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption("Space Invaders")

BG_IMG = pygame.transform.scale(pygame.image.load(os.path.join("img","bg.bmp")).convert_alpha(), (1280, 750))
PLAYER_IMG = pygame.transform.scale(pygame.image.load(os.path.join("img","ship.bmp")).convert_alpha(), (50, 30))
ALIEN_IMG = pygame.transform.scale(pygame.image.load(os.path.join("img","alien.bmp")).convert_alpha(), (50, 30))
BARRIER_IMG = pygame.transform.scale(pygame.image.load(os.path.join("img","barrier.bmp")).convert_alpha(), (70, 40))

PLAYERBULLET_IMG = pygame.Surface((5, 10))
PLAYERBULLET_IMG.fill((125, 255, 255))

ALIENBULLET_IMG = pygame.Surface((5, 10))
ALIENBULLET_IMG.fill((255, 255, 255))

player_rect = PLAYER_IMG.get_rect(center=(400, 550))
alien_rect = ALIEN_IMG.get_rect(center=(400, 50))

class GameObject:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Barrier(GameObject):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.image = BARRIER_IMG
        self.rect = self.image.get_rect(topleft=(x, y))

class PlayerBullet(GameObject):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.x = x
        self.y = y
        self.image = PLAYERBULLET_IMG
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = 5
        self.top = self.image.get_rect(center=(x, y)).centerx
        
    def move(self):
        self.rect.y -= self.speed

class Player(GameObject):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.image = PLAYER_IMG
        self.rect = self.image.get_rect(center=(x, y))
        self.bullets = []
        self.bullet_cooldown = 0
        self.bullet_rate = 30
        self.score = 0
        self.health = 3
        self.alive = True

    def move_left(self):
        self.rect.x -= 5

    def move_right(self):
        self.rect.x += 5

    def shoot(self):
        if self.bullet_cooldown <= 0:
            rnd = random.randint(1,2)
            if rnd % 2 == 0:
                bullet = PlayerBullet(self.rect.centerx-22, self.rect.bottom-30)
            else:
                bullet = PlayerBullet(self.rect.centerx+22, self.rect.bottom-30)
            self.bullets.append(bullet)
            self.bullet_cooldown = self.bullet_rate
    
    def update(self):
        self.bullet_cooldown -= 1
        if self.bullet_cooldown < 0:
            self.bullet_cooldown = 0
        for bullet in self.bullets:
            bullet.move()
            if bullet.top < 0:
                self.bullets.remove(bullet)
                self.bullet_cooldown = self.bullet_rate

    def hit(self):
        if self.health > 0:
            self.health -= 1
        if self.health == 0:
            self.alive = False


class AlienBullet(GameObject):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.x = x
        self.y = y
        self.image = ALIENBULLET_IMG
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = 5
        self.top = self.image.get_rect(center=(x, y)).centerx
        self.health = 30

    def move(self):
        self.rect.y += self.speed

class Alien:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.image = ALIEN_IMG
        self.rect = self.image.get_rect(center=(x, y))
        self.direction = 1
        self.speed = 2
        self.bullet_cooldown = 10
        self.bullet_rate = 3
        self.bullets = []

    def move(self):
        self.rect.x += self.direction * self.speed
        if self.rect.right > screen.get_width() or self.rect.left < 0:
            self.direction *= -1
            self.rect.y += 10

    def shoot(self):
        if self.bullet_cooldown <= 0: 
            # Use random number generator to determine if alien will shoot
            if random.randint(1, 100) < self.bullet_rate:
                alien_bullet = AlienBullet(self.rect.centerx, self.rect.bottom)
                self.bullets.append(alien_bullet)
                print(len(self.bullets))
                self.bullet_cooldown = 30
            else:
                self.bullet_cooldown -= 1   
    
    def update(self):
        self.bullet_cooldown -= 1
        if self.bullet_cooldown < 0:
            self.bullet_cooldown = 0
        for bullet in self.bullets:
            bullet.move()
            if bullet.top < 0:
                self.bullets.remove(bullet)
                self.bullet_cooldown = self.bullet_rate


player = Player(screen.get_width()/2, screen.get_height()-50)
covers = [Barrier(150, 550), Barrier(450, 550), Barrier(750, 550), Barrier(1050, 550)]
aliens = []
for i in range(5):
    for j in range(10):
        alien = Alien(23 + 50 * j, 20 + 50 * i)
        aliens.append(alien)
        screen.blit(alien.image, alien.rect)
    
screen.blit(PLAYER_IMG, player_rect)

clock = pygame.time.Clock()
running = True
while running:
    clock.tick(60) # 60 fps
    player.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_x] or keys[pygame.K_ESCAPE]:
        running = False
    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        player.move_left()
    if keys[pygame.K_RIGHT]or keys[pygame.K_d]:
        player.move_right()
    if keys[pygame.K_SPACE] and player.bullet_cooldown <= 0:
        player.shoot()
    
    # score
    score_label = STAT_FONT.render("Score: " + str(player.score),1,(125,125,125))
    score_rect = score_label.get_rect()
    score_rect.bottomleft = (10, screen.get_height() - 10)

    # player_health
    health = player.health
    health_label = STAT_FONT.render("Health: " + str(player.health),1,(125,125,125))
    health_rect = health_label.get_rect()
    health_rect.bottomright = (1200, screen.get_height() - 10)

    screen.fill((0, 0, 0)) # Clear the screen
    
    screen.blit(BG_IMG, (0,0))
    screen.blit(health_label, health_rect)
    screen.blit(score_label, score_rect)
    screen.blit(PLAYER_IMG, player.rect)
    
    for alien in aliens:
        alien.shoot()
        alien.move()
        alien.update()
        screen.blit(alien.image, alien.rect)

    for bullet in player.bullets:
        bullet.move()
        screen.blit(bullet.image, bullet)
        if bullet.top < 0:
            player.bullets.remove(bullet)
            
    for bullet in alien.bullets:
        bullet.move()
        screen.blit(bullet.image, bullet)
        if bullet.rect.colliderect(player.rect):
            player.hit()
            alien.bullets.remove(bullet)
        if bullet.top < 0:
            player.bullets.remove(bullet)
    
    for alien in aliens:
        for bullet in player.bullets:
            if alien.rect.colliderect(bullet):
                aliens.remove(alien)
                player.bullets.remove(bullet)
                player.score += 1
            if bullet.rect.colliderect(player.rect):
                player.hit()

    for cover in covers:
        screen.blit(cover.image, cover.rect)
        for bullet in player.bullets:
            if cover.rect.colliderect(bullet):
                player.bullets.remove(bullet)
        for bullet in alien.bullets:
            if cover.rect.colliderect(bullet):
                alien.bullets.remove(bullet)


    for alien in aliens:
        if alien.rect.colliderect(player.rect):
            running = False

    if len(aliens) == 0 or player.health == 0:
        running = False

    if not player.alive:
        print("Game Over")
        running = False

    pygame.display.update()