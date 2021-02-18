import pygame


class game:
    def __init__(self, width, height, title):
        self.width = width
        self.height = height
        self.title = title
        self.__init_game()

    def __init_game(self):
        pygame.init()
        pygame.display.set_caption(self.title)
        self.screen = pygame.display.set_mode((self.width, self.height))
