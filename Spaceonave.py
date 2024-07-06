import pygame
from sys import exit
from random import randint, choice

# Ship
class Ship(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        # Sprites
        ship_1 = pygame.image.load('Sprites/Ship/ship1.png').convert_alpha()
        ship_2 = pygame.image.load('Sprites/Ship/ship2.png').convert_alpha()
        ship_shrink_1 = pygame.image.load('Sprites/Ship/tinyship.png').convert_alpha()
        ship_shrink_1 = pygame.transform.scale(ship_shrink_1, (ship_shrink_1.get_width() * 1.5, ship_shrink_1.get_height() * 1.5))
        ship_shrink_2 = pygame.image.load('Sprites/Ship/tinyship2.png').convert_alpha()
        ship_shrink_2 = pygame.transform.scale(ship_shrink_2, (ship_shrink_2.get_width() * 1.5, ship_shrink_2.get_height() * 1.5))

        self.ship_left = pygame.image.load('Sprites/Ship/shipleft.png').convert_alpha()
        self.ship_right = pygame.image.load('Sprites/Ship/shipright.png').convert_alpha()

        # Animation
        self.ship_shrink_sprites = [ship_shrink_1, ship_shrink_2]
        self.ship_sprites = [ship_1, ship_2]
        self.ship_index = 0

        # Ship Variables
        self.movespeed = 3
        self.image = self.ship_sprites[self.ship_index]
        self.rect = self.image.get_rect(center=(150, 550))
        self.mask = pygame.mask.from_surface(self.image)
        self.default_rect = self.rect

    def ship_input(self): # Inputs
        keys = pygame.key.get_pressed()

        # Controls
        if keys[pygame.K_w]:
            self.rect.y -= self.movespeed
        if keys[pygame.K_s]:
            self.rect.y += self.movespeed
        if keys[pygame.K_a]:
            self.rect.x -= self.movespeed
        if keys[pygame.K_d]:
            self.rect.x += self.movespeed

        # Screen Hitbox
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > 300:
            self.rect.right = 300
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > 600:
            self.rect.bottom = 600

    def ship_animation(self): # Animation
        keys = pygame.key.get_pressed()
        self.movespeed = 3
        shrink = pygame.mixer.Sound('SFX\shrink.mp3')
        shrink_sound_played = 0

        if keys[pygame.K_LSHIFT]:
            if shrink_sound_played > 0:
                shrink.play()
                self.shrink_sound_played += 1

            self.movespeed = 5
            self.ship_index += 0.2
            if self.ship_index >= len(self.ship_sprites): 
                self.ship_index = 0
            self.image = self.ship_shrink_sprites[int(self.ship_index)]
            self.rect = self.image.get_rect(center=self.rect.center)
            self.mask = pygame.mask.from_surface(self.image)

        # Left Animation
        elif keys[pygame.K_a]:
            self.image = self.ship_left
            self.rect = self.image.get_rect(center=self.rect.center)
        # Right Animation
        elif keys[pygame.K_d]:
            self.image = self.ship_right
            self.rect = self.image.get_rect(center=self.rect.center)

        # Ship Default Animation
        else:
            self.ship_index += 0.2
            if self.ship_index >= len(self.ship_sprites): 
                self.ship_index = 0
            self.image = self.ship_sprites[int(self.ship_index)]
            self.rect = self.image.get_rect(center=self.rect.center)
            self.mask = pygame.mask.from_surface(self.image)

    def update(self): # Update
        global playing
        self.ship_input()
        self.ship_animation()

        if not playing: # Reset Ship Position
            self.image = self.ship_sprites[int(self.ship_index)]
            self.rect = self.image.get_rect(center=(150, 550))

# Bricks
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

# Animations
class Animation(pygame.sprite.Sprite):
    def __init__(self, type, pos):
        super().__init__()

        self.frames = []

        if type == 'explosion':
            self.frames.append(pygame.image.load('Sprites/Animations/Explosion/explosion1.png').convert_alpha())
            self.frames.append(pygame.image.load('Sprites/Animations/Explosion/explosion2.png').convert_alpha())
            self.frames.append(pygame.image.load('Sprites/Animations/Explosion/explosion3.png').convert_alpha())
            self.frames.append(pygame.image.load('Sprites/Animations/Explosion/explosion4.png').convert_alpha())
            self.frames.append(pygame.image.load('Sprites/Animations/Explosion/explosion5.png').convert_alpha())
            self.frames.append(pygame.image.load('Sprites/Animations/Explosion/explosion6.png').convert_alpha())

        self.animation_index = 0
        self.image = self.frames[int(self.animation_index)]
        self.rect = self.image.get_rect(center=pos)

    def update(self):
        self.animation_index += 0.2
        if int(self.animation_index) >= len(self.frames):
            self.kill()
        else:
            self.image = self.frames[int(self.animation_index)]

# Bullet
class Bullet(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = pygame.image.load('Sprites/Ship/shot.png').convert_alpha()
        self.rect = self.image.get_rect(center=pos)
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        destroybrick = pygame.mixer.Sound('SFX\destroy.mp3')

        self.rect.y -= 20
        if self.rect.y < -50:
            self.kill()
        hit_brick = pygame.sprite.spritecollide(self, bricks, True, pygame.sprite.collide_mask)
        if hit_brick:
            self.kill()
            destroybrick.play()
            for brick in hit_brick:
                animation.add(Animation('explosion', brick.rect.center))

# Collision
def collision_sprite():
    death = pygame.mixer.Sound('SFX\death.mp3')

    if pygame.sprite.spritecollide(ship.sprite, bricks, False, pygame.sprite.collide_mask):
        death.play()
        bricks.empty()
        animation.empty()
        return False
    return True

# Score
def display_score():
    time = int(pygame.time.get_ticks() / 1000) - start_time
    score_surf = test_font.render(f'{time}', False, 'WHITE')
    score_rect = score_surf.get_rect(topleft=(120, 10))
    screen.blit(score_surf, score_rect)

# Main
pygame.init()
screen = pygame.display.set_mode((300, 600))
pygame.display.set_caption('Spaceonave')
clock = pygame.time.Clock()
playing = False
icon = pygame.image.load('Sprites/icon.png').convert_alpha()
pygame.display.set_icon(icon)
test_font = pygame.font.Font('Font/Pixeltype.ttf', 50)
start_time = 0
ammo = 3
final_score = 0

# Space Ship
ship = pygame.sprite.GroupSingle()
ship.add(Ship())

# Bullets
bullets = pygame.sprite.Group()

# Bricks
bricks = pygame.sprite.Group()

# Animations
animation = pygame.sprite.Group()

# Musics and Sound Effects
laser = pygame.mixer.Sound('SFX\laser.mp3')
play = pygame.mixer.Sound('SFX\play.mp3')

background_music = pygame.mixer.Sound('SFX/background.mp3')
background_music.play(loops = -1),

# Background
background = pygame.image.load('Sprites/Backgorunds/Background.png').convert()

# Menu
play1 = pygame.image.load('Sprites/Play1.png').convert()
play2 = pygame.image.load('Sprites/Play2.png').convert()
play_sprites = [play1, play2]
play_index = 0

display = pygame.image.load('Sprites/Display/display.png').convert_alpha()
displayrect = display.get_rect(midtop=(150, 0))

ammo_display_list = []
ammo_display_list.append(pygame.image.load('Sprites/Display/1bullet.png').convert_alpha())
ammo_display_list.append(pygame.image.load('Sprites/Display/2bullet.png').convert_alpha())
ammo_display_list.append(pygame.image.load('Sprites/Display/3bullet.png').convert_alpha())
ammodispimage = ammo_display_list[(ammo-1)]
ammodisprect = ammodispimage.get_rect(midtop=(150, 0))

scale_factor = 4
play_scaled = pygame.transform.scale(play_sprites[play_index], (play_sprites[play_index].get_width() * scale_factor, play_sprites[play_index].get_height() * scale_factor))
playrect = play_scaled.get_rect(center=(150, 400))

titlelogo = pygame.image.load('Sprites/title.png').convert()
titlerect = titlelogo.get_rect(center=(150, 150))

# Timers
brick_timer = pygame.USEREVENT + 1
pygame.time.set_timer(brick_timer, 500)
recharge = pygame.USEREVENT + 2
pygame.time.set_timer(recharge, 5000)

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
                play.play()
                ship.update()
                bullets.empty()
                animation.empty()
                start_time = int(pygame.time.get_ticks() / 1000)
                ammo = 3
                playing = True

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r and not playing:
                play.play()
                ship.update()
                bullets.empty()
                start_time = int(pygame.time.get_ticks() / 1000)
                ammo = 3
                playing = True

        if playing:
            if event.type == brick_timer:
                bricks.add(Brick(choice([1, 2, 3, 4, 5])))

            if event.type == recharge and ammo < 3:
                ammo += 1

            if event.type == pygame.KEYDOWN and ammo > 0:
                keys = pygame.key.get_pressed()
                if event.key == pygame.K_SPACE and not keys[pygame.K_LSHIFT]:
                    laser.play()
                    bullets.add(Bullet(ship.sprite.rect.center))
                    ammo -= 1

    if playing:
        # Background
        screen.blit(background, (0, 0))

        # Animações
        animation.draw(screen)
        animation.update()

        # Bricks
        bricks.draw(screen)
        bricks.update()

        # Bullets
        bullets.draw(screen)
        bullets.update()

        # Ship
        ship.draw(screen)
        ship.update()

        # Display
        screen.blit(display, displayrect)
        
        if ammo > 0:
            ammodispimage = ammo_display_list[(ammo-1)]
            screen.blit(ammodispimage,ammodisprect)
        display_score()

        # Collision
        if not collision_sprite():
            final_score = int(pygame.time.get_ticks() / 1000) - start_time
            playing = False

    else:
        finalscore_surf = test_font.render(f'Final Score: {final_score}', False, 'WHITE')
        finalscore_rect = finalscore_surf.get_rect(midbottom=(150, 350))

        screen.blit(background, (0, 0))
        play_scaled = pygame.transform.scale(play_sprites[play_index], (play_sprites[play_index].get_width() * scale_factor, play_sprites[play_index].get_height() * scale_factor))
        screen.blit(play_scaled, playrect)
        screen.blit(titlelogo, titlerect)
        if start_time > 0:
            screen.blit(finalscore_surf, finalscore_rect)
    
    pygame.display.update()
    clock.tick(60)