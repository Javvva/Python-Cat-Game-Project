import pygame

class TitleScreen:
    def __init__(self, screen, gameStateManager, player): 
        self.screen = screen
        self.gameStateManager = gameStateManager

        self.text_font = pygame.font.Font('assets/fonts/PixelType.ttf', 50)

        self.text_font_small = pygame.font.Font('assets/fonts/PixelType.ttf', 40)
        self.player_hold = False

        # player sprite
        self.player = player
        self.player_surf = player.image
        self.player_rect = player.rect
        self.drop_sound = pygame.mixer.Sound('assets/sounds/Meow.wav')
        pygame.mixer.music.set_volume(0.5)

        #text
        self.game_name = self.text_font.render('Welcome to Test Demo', False, ('White'))
        self.game_name_rect = self.game_name.get_rect(midtop=(400, 50))

        self.click_start_surf = self.text_font.render('Click here to start', False, 'White')
        self.click_start_rect = self.click_start_surf.get_rect(midtop=(400, 110))


        #keybinds
        self.keybinds_title = self.text_font.render('Keybinds: ', False, 'White')
        self.keybinds_title_rect = self.keybinds_title.get_rect(topleft=(10, 530))

        self.keybinds_text = self.text_font_small.render('Arrow keys or WASD and space', False, 'White')
        self.keybinds_text_rect = self.keybinds_text.get_rect(topleft=(10, 570))


        self.credits_text = self.text_font_small.render('By: Collin Samson', False, 'White')
        self.credits_text_rect = self.keybinds_text.get_rect(topleft=(590, 570))

    def handle_events(self, events):
        for event in events:
            # Holding player
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.player_rect.collidepoint(event.pos):
                    self.player_hold = True
                    self.drop_sound.play()
                if self.click_start_rect.collidepoint(event.pos):
                    self.gameStateManager.currentState = 'Level_1'

            # Change text color via mouse
            elif event.type == pygame.MOUSEMOTION:
                if self.player_hold:
                    self.player_rect.move_ip(event.rel)
                if self.click_start_rect.collidepoint(event.pos):
                    self.click_start_surf = self.text_font.render('Click here to start', False, 'Red')
                else:
                    self.click_start_surf = self.text_font.render('Click here to start', False, 'White')

            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                self.player_hold = False
                

        # Apply gravity when not holding
        if not self.player_hold:
            self.player.intro_gravity += 0.8
            self.player_rect.y += int(self.player.intro_gravity)
        else:
            self.player.intro_gravity = 0

        # Stop at bottom of screen
        if self.player_rect.bottom >= self.screen.get_height():
            self.player_rect.bottom = self.screen.get_height()
            self.player.intro_gravity = 0
        
        if self.player_rect.bottom >= 492:  
            self.player_rect.bottom = 492
            self.player.intro_gravity = 0

        self.player_rect.clamp_ip(self.screen.get_rect())

    def draw(self):
        #scaling the player to make it bigger
        scaled_player = pygame.transform.scale(self.player.image, (32, 32)) 
        self.screen.blit(scaled_player, self.player_rect)
        
        
        
        self.screen.blit(self.game_name, self.game_name_rect)
        self.screen.blit(self.click_start_surf, self.click_start_rect)
        self.screen.blit(self.keybinds_title, self.keybinds_title_rect)
        self.screen.blit(self.keybinds_text, self.keybinds_text_rect)
        self.screen.blit(self.credits_text, self.credits_text_rect)
        