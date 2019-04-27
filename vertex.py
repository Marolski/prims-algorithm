import pygame

class Vertex(pygame.sprite.Sprite):
    def __init__(self, position, is_starting_vertex=False):
        super().__init__()
        (x, y) = position
        (self.x, self.y) = position
        self.is_starting_vertex = is_starting_vertex
        self.set_icon(is_starting_vertex)

    def set_position(self, x, y):
        self.rect.x = x
        self.rect.y = y
        
    def set_type(self, is_starting_vertex):
        self.set_icon(is_starting_vertex)
        self.is_starting_vertex = is_starting_vertex
        
    def set_icon(self, is_starting_vertex):
        if is_starting_vertex:
            self.image = pygame.image.load("electric_pole.png").convert_alpha()
        else:
            self.image = pygame.image.load("house.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = self.x - self.rect.width/2
        self.rect.y = self.y - self.rect.height/2
            
    