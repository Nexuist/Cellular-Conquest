import pygame
from BaseClasses import Color, Coordinates, Scene
from Game import Game

class StartScene(Scene):

    def build_scene(self, args):
        font = pygame.font.Font(None, 36)
        # True for antialiasing
        self.text = font.render("Click to continue", True, Color.black)
        self.text_pos = self.text.get_rect(centerx = self.center_x, centery = self.center_y)

    def render_scene(self):
        self.background.blit(self.text, self.text_pos)

    def click(self, position):
        self.done = True
        GameScene()

class EndScene(Scene):

    def build_scene(self, args):
        font = pygame.font.Font(None, 36)
        self.lose_text = font.render("YOU LOSE", True, Color.black)
        self.lose_text_pos = self.lose_text.get_rect(centerx = self.center_x, centery = self.center_y)
        self.seconds_text = font.render("You lasted %s seconds" % args["seconds"], True, Color.red)
        self.seconds_text_pos = self.seconds_text.get_rect(centerx = self.center_x, centery = self.center_y + 40)
        self.click_text = font.render("Click to continue", True, Color.black)
        self.click_text_pos = self.click_text.get_rect(centerx = self.center_x, centery = self.center_y + 80)

    def render_scene(self):
        self.background.blit(self.lose_text, self.lose_text_pos)
        self.background.blit(self.seconds_text, self.seconds_text_pos)
        self.background.blit(self.click_text, self.click_text_pos)


    def click(self, position):
        self.done = True
        StartScene()


class GameScene(Scene):

    def build_scene(self, args):
        # init game
        self.game = Game(self.center)
        pygame.time.set_timer(pygame.USEREVENT + 1, 1000) # Remember to deactivate later by setting 1000->0

    def render_scene(self):
        self.screen.blit(self.background, (0, 0))
        self.game.update()
        self.game.sprites.draw(self.background)

    def click(self, position):
        self.game.handle_click(position)

    def handle_event(self, event):
        if event.type == pygame.USEREVENT + 1:
            self.game.every_second()
        elif event.type == pygame.USEREVENT + 2:
            self.done = True
            EndScene({"seconds": event.seconds})
