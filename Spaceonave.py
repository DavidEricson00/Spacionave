import pygame
from sys import exit
from random import randint, choice

#Nave
class Ship(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        ship_1 = pygame.image.load('Sprites/Ship/ship1.png').convert_alpha()
        ship_2 = pygame.image.load('Sprites/Ship/ship2.png').convert_alpha()
        ship_shrink_1 = pygame.image.load('Sprites/Ship/tinyship.png').convert_alpha()
        ship_shrink_1 = pygame.transform.scale(ship_shrink_1, (ship_shrink_1.get_width() * 1.5, ship_shrink_1.get_height() * 1.5))
        ship_shrink_2 = pygame.image.load('Sprites/Ship/tinyship2.png').convert_alpha()
        ship_shrink_2 = pygame.transform.scale(ship_shrink_2, (ship_shrink_2.get_width() * 1.5, ship_shrink_2.get_height() * 1.5))

        self.ship_left = pygame.image.load('Sprites/Ship/shipleft.png').convert_alpha()
        self.ship_right = pygame.image.load('Sprites/Ship/shipright.png').convert_alpha()

        self.ship_shrink_sprites = [ship_shrink_1, ship_shrink_2]
        self.ship_sprites = [ship_1, ship_2]
        self.ship_index = 0
        self.movespeed = 3

        self.image = self.ship_sprites[self.ship_index]
        self.rect = self.image.get_rect(center=(150, 550))
        self.mask = pygame.mask.from_surface(self.image)
        self.default_rect = self.rect

    def ship_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.rect.y -= self.movespeed
        if keys[pygame.K_s]:
            self.rect.y += self.movespeed
        if keys[pygame.K_a]:
            self.rect.x -= self.movespeed
        if keys[pygame.K_d]:
            self.rect.x += self.movespeed

        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > 300:
            self.rect.right = 300
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > 600:
            self.rect.bottom = 600

    def ship_animation(self):
        keys = pygame.key.get_pressed()
        self.movespeed = 3
        if keys[pygame.K_SPACE]:
            self.movespeed = 5

            self.ship_index += 0.2
            if self.ship_index >= len(self.ship_sprites): 
                self.ship_index = 0
            self.image = self.ship_shrink_sprites[int(self.ship_index)]
            self.rect = self.image.get_rect(center=self.rect.center)
            self.mask = pygame.mask.from_surface(self.image)

        elif keys[pygame.K_a]:
            self.image = self.ship_left
            self.rect = self.image.get_rect(center=self.rect.center)
        elif keys[pygame.K_d]:
            self.image = self.ship_right
            self.rect = self.image.get_rect(center=self.rect.center)

        else:
            self.ship_index += 0.2
            if self.ship_index >= len(self.ship_sprites): 
                self.ship_index = 0
            self.image = self.ship_sprites[int(self.ship_index)]
            self.rect = self.image.get_rect(center=self.rect.center)
            self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        global playing
        self.ship_input()
        self.ship_animation()

        if playing == False:
            self.image = self.ship_sprites[int(self.ship_index)]
            self.rect = self.image.get_rect(center=(150, 550))

#Bricks
class Brick(pygame.sprite.Sprite):
    def __init__(self, sprite):
        super().__init__()
        scale_factor = 1.8
        if sprite == 1:
            self.original_image = pygame.image.load('Sprites/Bricks/brick1.png').convert_alpha()
        elif sprite == 2:
            self.original_image = pygame.image.load('Sprites/Bricks/brick2.png').convert_alpha()
        elif sprite == 3:
            self.original_image = pygame.image.load('Sprites/Bricks/brick3.png').convert_alpha()
        elif sprite == 4:
            self.original_image = pygame.image.load('Sprites/Bricks/brick4.png').convert_alpha()
        elif sprite == 5:
            self.original_image = pygame.image.load('Sprites/Bricks/brick5.png').convert_alpha()
        
        self.original_image = pygame.transform.scale(self.original_image, (int(self.original_image.get_width() * scale_factor), int(self.original_image.get_height() * scale_factor)))
        
        self.image = self.original_image
        self.rect = self.image.get_rect(center=(randint(50, 250), randint(-200, -50)))
        self.mask = pygame.mask.from_surface(self.image)
        self.angle = 0
        self.speed = randint(4, 9)

    def rotate(self):
        self.angle += 1.5
        if self.angle >= 360:
            self.angle = 0
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        self.rect.y += self.speed
        self.rotate()
        if self.rect.y > 700:
            self.kill()

#Colisão
def collision_sprite():
    if pygame.sprite.spritecollide(ship.sprite, bricks, False, pygame.sprite.collide_mask):
        bricks.empty()
        return False
    return True

#Score
def display_score ():
    
    #keys = pygame.key.get_pressed()
    #if keys[pygame.K_SPACE]:
        #time = int(pygame.time.get_ticks() / 1000) - start_time
        #currenttime = time
    #elif keys[pygame.K_SPACE]:
        #time = currenttime
        
    time = int(pygame.time.get_ticks() / 1000) - start_time
    score_surf = test_font.render(f'{time}',False,('WHITE'))
    score_rect = score_surf.get_rect(topleft = (120,10))
    screen.blit(score_surf,score_rect)

# Main
pygame.init()
screen = pygame.display.set_mode((300, 600))
pygame.display.set_caption('Spaceonave')
clock = pygame.time.Clock()
playing = False
icon = pygame.image.load('Sprites\icon.png').convert_alpha()
pygame.display.set_icon(icon)
test_font = pygame.font.Font('Font\Pixeltype.ttf', 50)
start_time = 0

# Space Ship
ship = pygame.sprite.GroupSingle()
ship.add(Ship())

# Bricks
bricks = pygame.sprite.Group()

# Background
background = pygame.image.load('Sprites/Backgorounds/Background.png').convert()

# Menu
play1 = pygame.image.load('Sprites/Play1.png').convert()
play2 = pygame.image.load('Sprites/Play2.png').convert()
play_sprites = [play1, play2]
play_index = 0

display = pygame.image.load('Sprites\Display\display.png').convert()
displayrect = display.get_rect(midtop=(150, 0))

scale_factor = 4
play_scaled = pygame.transform.scale(play_sprites[play_index], (play_sprites[play_index].get_width() * 4, play_sprites[play_index].get_height() * 4))
playrect = play_scaled.get_rect(center=(150, 400))

titlelogo = pygame.image.load('Sprites/title.png').convert()
titlerect = titlelogo.get_rect(center=(150, 150))

# Timers
brick_timer = pygame.USEREVENT + 1
pygame.time.set_timer(brick_timer, 600)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        
        elif event.type == pygame.MOUSEMOTION:
            if playrect.collidepoint(event.pos):
                play_index = 1
            else:
                play_index = 0

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if playrect.collidepoint(event.pos):
                ship.update()
                start_time = int(pygame.time.get_ticks() / 1000)
                playing = True

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r and not playing:
                ship.update()
                start_time = int(pygame.time.get_ticks() / 1000)
                playing = True

        if playing:
            if event.type == brick_timer:
                bricks.add(Brick(choice([1, 2, 3, 4, 5])))

    if playing:
        # Background
        screen.blit(background, (0, 0))

        # Bricks
        bricks.draw(screen)
        bricks.update()
            
        # Ship
        ship.draw(screen)
        ship.update()

        #Display
        screen.blit(display,displayrect)
        display_score()

        # Collision
        playing = collision_sprite()

    else:
        screen.blit(background, (0, 0))
        play_scaled = pygame.transform.scale(play_sprites[play_index], (play_sprites[play_index].get_width() * 4, play_sprites[play_index].get_height() * 4))
        screen.blit(play_scaled, playrect)
        screen.blit(titlelogo, titlerect)
    
    pygame.display.update()
    clock.tick(60)
