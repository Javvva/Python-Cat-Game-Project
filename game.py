import pygame, sys
from pytmx.util_pygame import load_pygame
from player_prop import Player
from camera import Camera, Border
from settings import SCREEN, SCREEN_WIDTH, SCREEN_HEIGHT
from TitleScreen import TitleScreen
from DeathScreen import DeathScreen


pygame.init()
clock = pygame.time.Clock()


#map class--------------------------------------------------------------------------------------------------------
class Tile(pygame.sprite.Sprite):
    def __init__(self, pos,surf,groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_rect(topleft = pos)
#-----------------------------------------------------------------------------------------------------------------


#Intro------------------------------------------------------------------------------------------------------------
class Intro:
    def __init__(self, display, gameStateManager):
        self.display = display
        self.SCREEN = SCREEN
        self.gameStateManager = gameStateManager
        intro_music = True
        
        #zoom
        self.ZOOM_LEVEL = 1
        self.RENDER_WIDTH = SCREEN_WIDTH
        self.RENDER_HEIGHT = SCREEN_HEIGHT
        self.render_surface = pygame.Surface((self.RENDER_WIDTH, self.RENDER_HEIGHT))

        #map stuff
        tmx_data = load_pygame('Intro_Map/Intro.tmx')
 
        self.MAP_WIDTH = tmx_data.width * tmx_data.tilewidth
        self.MAP_HEIGHT = tmx_data.height * tmx_data.tileheight
 
        self.tile_sprites = pygame.sprite.Group()
        self.obstacle_sprites = pygame.sprite.Group()
        self.player_group = pygame.sprite.Group()
        
        for layer in tmx_data.visible_layers:
            if hasattr(layer, 'data'):
                for x, y, surf in layer.tiles():
                    pos = (x * 32, y * 32)
                    if layer.name == 'ground':
                        Tile(pos, surf, [self.tile_sprites, self.obstacle_sprites])
                    else:  
                        Tile(pos, surf, [self.tile_sprites])
 
        # Camera
        self.camera_x = (self.MAP_WIDTH - self.RENDER_WIDTH) // 2
        self.camera_y = (self.MAP_HEIGHT - self.RENDER_HEIGHT) // 2
 
        # Create player 
        self.player = Player(pos=(350, 400), groups=self.player_group, obstacle_sprites=self.obstacle_sprites)
        self.player.intro_gravity = 0
        
        self.player.image = pygame.transform.scale(self.player.image, (32, 32))  
        self.player.rect = self.player.image.get_rect(topleft=self.player.rect.topleft)
 
        self.title_screen = TitleScreen(self.SCREEN, self.gameStateManager, self.player)

 
    def handle_events(self, events):
        self.title_screen.handle_events(events)
 
    def run(self):
        self.render_surface.fill("black")
 
        # Draw camera
        for sprite in self.tile_sprites:
            offset_pos = (sprite.rect.x - self.camera_x, sprite.rect.y - self.camera_y)
            self.render_surface.blit(sprite.image, offset_pos)
 
        # Scale to screen
        self.SCREEN.blit(self.render_surface, (0, 0))
        self.title_screen.draw()
#-----------------------------------------------------------------------------------------------------------------

#Level 1----------------------------------------------------------------------------------------------------------
class Level_1:
    def __init__(self, display, gameStateManager):
        self.display = display
        self.SCREEN = SCREEN
        self.gameStateManager = gameStateManager
        self.is_dead = False
        

        self.ZOOM_LEVEL = 1.5 
        self.RENDER_WIDTH = SCREEN_WIDTH // self.ZOOM_LEVEL   
        self.RENDER_HEIGHT = SCREEN_HEIGHT // self.ZOOM_LEVEL  
        self.render_surface = pygame.Surface((self.RENDER_WIDTH, self.RENDER_HEIGHT))
        
        tmx_data = load_pygame('Map_1/map_1.tmx')

        self.MAP_WIDTH = tmx_data.width * tmx_data.tilewidth
        self.MAP_HEIGHT = tmx_data.height * tmx_data.tileheight

        self.tile_sprites = pygame.sprite.Group()
        self.obstacle_sprites = pygame.sprite.Group()
        self.trap_sprites = pygame.sprite.Group()
        self.player_group = pygame.sprite.Group()
 
        for layer in tmx_data.visible_layers:
            if hasattr(layer, 'data'):
                for x, y, surf in layer.tiles():
                    pos = (x * 32, y * 32)
                    if layer.name == 'ground':
                        Tile(pos, surf, [self.tile_sprites, self.obstacle_sprites])
                    elif layer.name == 'traps':
                        Tile(pos, surf, [self.tile_sprites, self.trap_sprites])

                    else:
                        Tile(pos, surf, [self.tile_sprites])
    

        self.player = Player(pos=(100, 350), groups=self.player_group, obstacle_sprites=self.obstacle_sprites)
        self.player.set_map_bounds(self.MAP_WIDTH, self.MAP_HEIGHT)
        
        
        self.camera = Camera(self.player, self.RENDER_WIDTH, self.RENDER_HEIGHT, self.MAP_WIDTH, self.MAP_HEIGHT)
        self.camera.setmethod(Border(self.camera, self.player))

        self.death_sound = pygame.mixer.Sound('assets/sounds/Meow.wav')


    def play_music(self):
        pygame.mixer.music.load('assets/sounds/level1_music.wav')
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(0.5)

    def run(self):
        if self.gameStateManager.get_state() != 'Level_1':
            return
        self.render_surface.fill('black')
        self.player_group.update()
        self.camera.scroll()
            
         # Draw map
        for sprite in self.tile_sprites:
            offset_pos = (sprite.rect.x - self.camera.offset.x, sprite.rect.y - self.camera.offset.y)
            self.render_surface.blit(sprite.image, offset_pos)
            
        # Draw player
        for sprite in self.player_group:
            offset_pos = (sprite.rect.x - self.camera.offset.x, sprite.rect.y - self.camera.offset.y)
            self.render_surface.blit(sprite.image, offset_pos)

        #traps/death
        for trap in self.trap_sprites:
            if trap.rect.colliderect(self.player.rect):
                self.player.death_sound.play()
                self.gameStateManager.set_state('Death')

        if not self.is_dead:
            for trap in self.trap_sprites:
                if trap.rect.colliderect(self.player.rect):
                    self.is_dead = True
                    self.death_sound.play()
                    self.gameStateManager.set_state('Death')

            if self.player.rect.y > 500:
                self.is_dead = True
                self.death_sound.play()
                self.gameStateManager.set_state('Intro')
        
        #zoom
        scaled_surface = pygame.transform.scale(self.render_surface, (SCREEN_WIDTH, SCREEN_HEIGHT))
        self.SCREEN.blit(scaled_surface, (0, 0))
#-----------------------------------------------------------------------------------------------------------------



#Game State Manager-----------------------------------------------------------------------------------------------
class GameStateManager:
    def __init__(self, currentState):
        self.currentState = currentState
 
    def get_state(self):
        return self.currentState
 
    def set_state(self, state):
        self.currentState = state


#game loop --------------------------------------------------------------------------------------------------------
class Game:
    def __init__(self):
        pygame.init()
        self.SCREEN = SCREEN
        self.clock = pygame.time.Clock()
 
        self.gameStateManager = GameStateManager('Intro')
        self.intro = Intro(self.SCREEN, self.gameStateManager)
        self.level_1 = Level_1(self.SCREEN, self.gameStateManager)
        self.death_screen = DeathScreen(self.SCREEN, self.gameStateManager)

        self.states = {'Intro': self.intro, 'Level_1': self.level_1, 'Death': self.death_screen}
 
    def run(self):
        current_state = self.gameStateManager.get_state()

        while True:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            pygame.mixer.music.set_volume(0.5)

            new_state = self.gameStateManager.get_state()

            if new_state != current_state:
                current_state = new_state

                if current_state == 'Level_1':
                    self.level_1 = Level_1(self.SCREEN, self.gameStateManager)
                    self.states['Level_1'] = self.level_1
                    self.level_1.play_music()

                elif current_state == 'Death':
                    self.level_1 = Level_1(self.SCREEN, self.gameStateManager) 
                    self.states['Level_1'] = self.level_1
                    self.death_screen = DeathScreen(self.SCREEN, self.gameStateManager)
                    self.states['Death'] = self.death_screen

                elif current_state == 'Intro':
                    self.intro = Intro(self.SCREEN, self.gameStateManager)
                    self.states['Intro'] = self.intro
                    pygame.mixer.music.load('assets/sounds/intro_music.wav')
                    pygame.mixer.music.play(-1)
            
                else:
                    pygame.mixer.pause()   

            if self.gameStateManager.get_state() == 'Intro':
                self.intro.handle_events(events)
            elif self.gameStateManager.get_state() == 'Death':
                self.death_screen.handle_events(events)

            self.states[self.gameStateManager.get_state()].run()

            pygame.display.update()
            clock.tick(60)
 
if __name__ == '__main__':
    game = Game()
    game.run()
#-----------------------------------------------------------------------------------------------------------------