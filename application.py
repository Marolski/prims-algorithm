import pygame
import vertex

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
                        self.vertices.add(vertex.Vertex(pygame.mouse.get_pos()))
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
        
        
#tu jest jakby main, tworzę nowe okno programu
application = Application()        