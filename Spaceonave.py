import pygame
from sys import exit
from random import randint, choice

class Ship(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        ship_1 = pygame.image.load('Sprites/Ship/ship1.png').convert_alpha()
        ship_2 = pygame.image.load('Sprites/Ship/ship2.png').convert_alpha()
        self.ship_left = pygame.image.load('Sprites\Ship\shipleft.png').convert_alpha()
        self.ship_right = pygame.image.load('Sprites/Ship/shipright.png').convert_alpha()
        self.ship_sprites = [ship_1, ship_2]
        self.ship_index = 0
        self.movespeed = 3

        self.image = self.ship_sprites[self.ship_index]
        self.rect = self.image.get_rect(center=(150, 550))
        self.mask = pygame.mask.from_surface(self.image)

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
            

    def ship_animation(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.image = self.ship_left
        elif keys[pygame.K_d]:
            self.image = self.ship_right
        else:
            self.ship_index += 0.2
            if self.ship_index >= len(self.ship_sprites): 
                self.ship_index = 0
            self.image = self.ship_sprites[int(self.ship_index)]
            self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        self.ship_input()
        self.ship_animation()

class Meteor(pygame.sprite.Sprite):
    def __init__(self, sprite):
        super().__init__()
        if sprite == 1:
            self.image = pygame.image.load('Sprites/Meteors/meteor1.png').convert_alpha()
        elif sprite == 2:
            self.image = pygame.image.load('Sprites/Meteors/meteor2.png').convert_alpha()
        elif sprite == 3:
            self.image = pygame.image.load('Sprites/Meteors/meteor3.png').convert_alpha()
        self.rect = self.image.get_rect(center=(randint(0, 300), -100))
        self.mask = pygame.mask.from_surface(self.image)
    
    def destroy(self):
        if self.rect.y > 700:
            self.kill()

    def update(self):
        self.rect.y += 3
        self.destroy()

def collision_sprite():
    if pygame.sprite.spritecollide(ship.sprite, meteor, False, pygame.sprite.collide_mask):
        meteor.empty()
        return False
    return True

# Main
pygame.init()
screen = pygame.display.set_mode((300, 600))
pygame.display.set_caption('Spaceonave')
clock = pygame.time.Clock()
playing = False

# Space Ship
ship = pygame.sprite.GroupSingle()
ship.add(Ship())

# Meteors
meteor = pygame.sprite.Group()

# Background
background = pygame.image.load('Sprites\Backgorounds\Background.png').convert()

#Menu
play1 = pygame.image.load('Sprites\Play1.png').convert()
play2 = pygame.image.load('Sprites\Play2.png').convert()
play_sprites = [play1,play2]
play_index = 0
        
scale_factor = 4
play_scaled = pygame.transform.scale(play_sprites[play_index], (play_sprites[play_index].get_width() * 4, play_sprites[play_index].get_height() * 4))
playrect = play_scaled.get_rect(center = (150, 500))


# Timers
meteor_timer = pygame.USEREVENT + 1
pygame.time.set_timer(meteor_timer, 700)

while True:
    for event in pygame.event.get(): 
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == meteor_timer:
            meteor.add(Meteor(choice([1, 2, 3])))
        if event.type == pygame.MOUSEMOTION:
            if playrect.collidepoint(event.pos): 
                play_index = 1
                if event.type == pygame.MOUSEBUTTONUP:
                    playing = True
                    print ('Playing')
                    
            else: 
                play_index = 0

    if playing:
        # Background
        screen.blit(background,(0,0))

        # Meteors
        meteor.draw(screen)
        meteor.update()
            
        # Ship
        ship.draw(screen)
        ship.update()

        # Collision
        playing = collision_sprite()

    else:
        
        screen.blit(background,(0,0))
        play_scaled = pygame.transform.scale(play_sprites[play_index], (play_sprites[play_index].get_width() * 4, play_sprites[play_index].get_height() * 4))
        screen.blit(play_scaled, playrect)
    
    pygame.display.update()
    clock.tick(60)