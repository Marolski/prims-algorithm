import pygame

class Application:

    def __init__(self):   
        self.screen = pygame.display.set_mode((960,600)) 
        self.vertices = pygame.sprite.Group() 
        self.display()

    def display(self):
        continue_work = True 
        self.starting_vertex = None
        while continue_work:
        
            self.screen.fill((90, 209, 54))
            for event in pygame.event.get():
            
                #obsługa kliknięcia na krzyżyk
                if event.type == pygame.QUIT:
                    continue_work = False
                #obsługa kliknięcia LPM
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    add_new = True
                    for v in self.vertices:
                        if v.rect.collidepoint(pygame.mouse.get_pos()):
                            add_new = False
                    if add_new:
                        self.vertices.add(Vertex(pygame.mouse.get_pos()))
                #obsługa wciśnięcia "s"
                if event.type == pygame.KEYDOWN and event.key == pygame.K_s:
                    for v in self.vertices:
                        if v.rect.collidepoint(pygame.mouse.get_pos()):
                            if self.starting_vertex is None:
                                v.set_type(True)
                                self.starting_vertex = v
                            else:
                                self.starting_vertex.set_type(False)
                                self.starting_vertex = v
                                v.set_type(True)   
                #obsługa wciśnięcia "d"
                if event.type == pygame.KEYDOWN and event.key == pygame.K_d:
                    for v in self.vertices:
                        if v.rect.collidepoint(pygame.mouse.get_pos()):
                            v.kill()

                
                    
            self.vertices.update()
            self.vertices.draw(self.screen)
            pygame.display.flip()

        pygame.quit()   

class Vertex(pygame.sprite.Sprite):
    def __init__(self, position):
        pygame.sprite.Sprite.__init__(self)
        (self.x, self.y) = position
        self.set_type(False)
        
    def set_type(self, is_starting_vertex):
        self.is_starting_vertex = is_starting_vertex
        self.set_icon(is_starting_vertex)
 
    def set_icon(self, is_starting_vertex):
        if is_starting_vertex:
            self.image = pygame.image.load("electric_pole.png").convert_alpha()
        else:
            self.image = pygame.image.load("house.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = self.x - self.rect.width/2
        self.rect.y = self.y - self.rect.height/2        
        
        
#tu jest jakby main, tworzę nowe okno programu
application = Application()        