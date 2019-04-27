import pygame
import vertex

class Application:

    def __init__(self):   
        self.width = 960
        self.height = 600
        self.screen = pygame.display.set_mode((self.width,self.height))
        self.screen.fill((90, 209, 54))
        self.vertices = pygame.sprite.Group()
        self.display()

    def display(self):
        continue_work = True
        starting_vertex = None
        while continue_work:
            for event in pygame.event.get():
                
                if event.type == pygame.QUIT:
                    continue_work = False
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    add_new = True
                    for v in self.vertices:
                        if v.rect.collidepoint(pygame.mouse.get_pos()):
                            add_new = False
                    if add_new:
                        self.vertices.add(vertex.Vertex(pygame.mouse.get_pos()))
                    
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
                    for v in self.vertices:
                        if v.rect.collidepoint(pygame.mouse.get_pos()):
                            if starting_vertex is None:
                                v.set_type(True)
                                starting_vertex = v
                            else:
                                starting_vertex.set_type(False)
                                starting_vertex = v
                                v.set_type(True)      
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 2:
                    for v in self.vertices:
                        if v.rect.collidepoint(pygame.mouse.get_pos()):
                            v.kill()

                
                    
            self.vertices.update()
            self.vertices.draw(self.screen)
            pygame.display.flip()
            self.screen.fill((90, 209, 54))
        pygame.quit()        
        
        
#tu jest jakby main, tworzę nowe okno programu
application = Application()        