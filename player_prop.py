import pygame
from abc import ABC
from pytmx.util_pygame import load_pygame
from settings import SCREEN_WIDTH, SCREEN_HEIGHT

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups, obstacle_sprites):
        super().__init__(groups)
        
        # Load cat animations
        self.import_cat_assets()
        self.frame_index = 0
        self.animation_speed = 0.15
        self.status = 'idle'
        self.facing_right = True

        #sounds
        pygame.mixer.music.set_volume(0.5)
        self.jump_sound = pygame.mixer.Sound('assets/sounds/jump.wav')
        self.alive = True
        self.death_sound = pygame.mixer.Sound('assets/sounds/Meow.wav')
        
        self.image = self.animations[self.status][self.frame_index]
        self.rect = self.image.get_rect(topleft=pos)
        
        # Movement
        self.direction = pygame.math.Vector2(0, 0)
        self.speed = 5
        self.gravity = 1
        self.jump_speed = -19
        self.on_ground = False
        
        # Collision
        self.obstacle_sprites = obstacle_sprites
        
        # Map boundaries
        self.map_width = 0
        self.map_height = 0

    def set_map_bounds(self, map_width, map_height):
        self.map_width = map_width
        self.map_height = map_height

    def import_cat_assets(self):
        self.animations = {
            'idle': [], 'walk_right': [], 'walk_left': [], 'stand_right': [], 'stand_left': []}
        
        # Idle
        idle = pygame.image.load('assets/graphics/cat_idle.png').convert_alpha()
        self.animations['idle'].append(idle)
        
        # Right standing
        stand_right = pygame.image.load('assets/graphics/cat_right_standing.png').convert_alpha()
        self.animations['stand_right'].append(stand_right)
        
        # Left standing
        stand_left = pygame.image.load('assets/graphics/cat_left_standing.png').convert_alpha()
        self.animations['stand_left'].append(stand_left)
        
        # Right walking
        for i in range(1, 5):
            frame = pygame.image.load(f'assets/graphics/cat_right_walking_{i}.png').convert_alpha()
            self.animations['walk_right'].append(frame)
        
        # Left walking
        for i in range(1, 5):
            frame = pygame.image.load(f'assets/graphics/cat_left_walking_{i}.png').convert_alpha()
            self.animations['walk_left'].append(frame)

    def get_status(self):
        # Moving left
        if self.direction.x < 0:
            self.status = 'walk_left'
            self.facing_right = False
        # Moving right
        elif self.direction.x > 0:
            self.status = 'walk_right'
            self.facing_right = True
        # Standing
        else:
            if self.facing_right:
                self.status = 'stand_right'
            else:
                self.status = 'stand_left'
    
    def animate(self):
        animation = self.animations[self.status]
        
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0
        
        self.image = animation[int(self.frame_index)]
    
    def input(self):
        keys = pygame.key.get_pressed()
        
        # Horizontal movement
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            if self.rect.right < self.map_width:
                self.direction.x = 1
            else:
                self.direction.x = 0
        elif keys[pygame.K_LEFT] or keys[pygame.K_a]:
            if self.rect.left > 0:
                self.direction.x = -1
            else:
                self.direction.x = 0
        else:
            self.direction.x = 0
        
        # Jump
        if (keys[pygame.K_SPACE] or keys[pygame.K_UP] or keys[pygame.K_w]) and self.on_ground:
            self.direction.y = self.jump_speed
            self.jump_sound.play()
            self.jump_sound.set_volume(0.5)
    
    def apply_gravity(self):
        self.direction.y += self.gravity
        self.rect.y += self.direction.y
        
        # Bottom boundary 
        if self.rect.bottom >= self.map_height:
            self.rect.bottom = self.map_height
            self.direction.y = 0
            self.on_ground = True
    
    def horizontal_movement_collision(self):
        self.rect.x += self.direction.x * self.speed
        
        for sprite in self.obstacle_sprites:
            if sprite.rect.colliderect(self.rect):
                if self.direction.x < 0: 
                    self.rect.left = sprite.rect.right
                elif self.direction.x > 0: 
                    self.rect.right = sprite.rect.left
    
    def vertical_movement_collision(self):
        self.apply_gravity()
        self.on_ground = False
        
        for sprite in self.obstacle_sprites:
            if sprite.rect.colliderect(self.rect):
                if self.direction.y > 0: 
                    self.rect.bottom = sprite.rect.top
                    self.direction.y = 0
                    self.on_ground = True
                elif self.direction.y < 0: 
                    self.rect.top = sprite.rect.bottom
                    self.direction.y = 0
    
    def update(self):
        self.input()
        self.get_status()
        self.animate()
        self.horizontal_movement_collision()
        self.vertical_movement_collision()