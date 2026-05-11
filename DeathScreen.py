import pygame

class DeathScreen:
    def __init__(self, screen, gameStateManager):
        self.screen = screen
        self.gameStateManager = gameStateManager

        self.text_font = pygame.font.Font('assets/fonts/PixelType.ttf', 50)

        self.title = self.text_font.render('You Died!', False, 'Red')
        self.title_rect = self.title.get_rect(midtop=(400, 80))

        self.click_restart_surf = self.text_font.render('Restart', False, 'White')
        self.click_restart_rect = self.click_restart_surf.get_rect(midtop=(400, 200))

        self.click_menu_surf = self.text_font.render('Main Menu', False, 'White')
        self.click_menu_rect = self.click_menu_surf.get_rect(midtop=(400, 280))

        # Death screen music
        pygame.mixer.music.load('assets/sounds/death_music.wav')
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(0.5)

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.MOUSEMOTION:
                if self.click_restart_rect.collidepoint(event.pos):
                    self.click_restart_surf = self.text_font.render('Restart', False, 'Red')
                else:
                    self.click_restart_surf = self.text_font.render('Restart', False, 'White')

                if self.click_menu_rect.collidepoint(event.pos):
                    self.click_menu_surf = self.text_font.render('Main Menu', False, 'Red')
                else:
                    self.click_menu_surf = self.text_font.render('Main Menu', False, 'White')

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.click_restart_rect.collidepoint(event.pos):
                    self.gameStateManager.set_state('Level_1')
                if self.click_menu_rect.collidepoint(event.pos):
                    self.gameStateManager.set_state('Intro')

    def draw(self):
        self.screen.fill('Black')
        self.screen.blit(self.title, self.title_rect)
        self.screen.blit(self.click_restart_surf, self.click_restart_rect)
        self.screen.blit(self.click_menu_surf, self.click_menu_rect)

    def run(self):
        self.draw()