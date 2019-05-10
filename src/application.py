import pygame
import math

class Application:

    def __init__(self):   
        self.screen = pygame.display.set_mode((960,600)) 
        pygame.display.set_caption('Oszczedne połaczenie zabudowan we wsi')
        pygame.display.set_icon(pygame.image.load('icon.png'))
        pygame.font.init()
        self.vertices = pygame.sprite.Group() 
        self.edges = []
        self.display()

    def display(self):
        continue_work = True 
        self.starting_vertex = None
        edge_being_drawn = False
        current_edge = None
        distanceList = []
        distance = None
        font = pygame.font.SysFont("comicsansms", 15)


        
        
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
                #obsługa kliknięcia PPM
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
                    for v in self.vertices:
                        if v.rect.collidepoint(pygame.mouse.get_pos()):
                            current_edge = Edge((v.x,v.y),pygame.mouse.get_pos(), v)
                            self.edges.append(current_edge)
                            edge_being_drawn = True      
                            break
                #obsługa odkliknięcia PPM
                if event.type == pygame.MOUSEBUTTONUP and event.button == 3:                    
                    if edge_being_drawn:
                        found_vertex = None                    
                        edge_is_complete = False
                        edge_already_exists = False
                        edge_has_beginning_same_as_end = False
                        for v in self.vertices:
                            if v.rect.collidepoint(pygame.mouse.get_pos()): 
                                found_vertex = v
                                edge_is_complete = True
                        for e in self.edges:
                            if e is not current_edge:
                                if (e.vertex_beginning is current_edge.vertex_beginning) and (e.vertex_end is found_vertex):
                                    edge_already_exists = True
                        if found_vertex is current_edge.vertex_beginning:
                            edge_has_beginning_same_as_end = True
                        if (edge_is_complete) and (not edge_already_exists) and (not edge_has_beginning_same_as_end):
                            current_edge.set_vertex_end(found_vertex)
                            distance = math.floor(math.sqrt(((e.vertex_beginning.x-found_vertex.x)**2)+((e.vertex_beginning.y-found_vertex.y)**2))/40)
                            distanceList.append(distance)
                        else:
                            self.edges.remove(current_edge)
                            current_edge = None
                        
                        
                        edge_being_drawn = False              
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
                            edges_to_remove = []
                            for e in self.edges:
                                if (e.vertex_beginning is v) or (e.vertex_end is v):
                                    edges_to_remove.append(e)
                            for e in edges_to_remove:                                    
                                self.edges.remove(e)
                                e = None
                            v.kill()
                

                            
                            
            if edge_being_drawn:
                current_edge.update_position(current_edge.position_beginning, pygame.mouse.get_pos())
                
                            
            for e in self.edges:
                e.draw(self.screen)
                for d in distanceList:
                    d = str(d)
                    text = font.render(d, True, (0, 0, 0))
                    self.screen.blit(text,e.distance_rectangle(e.vertex_beginning,e.vertex_end))
                

            self.vertices.draw(self.screen)
            
            pygame.display.flip()

        pygame.quit()   
    


class Vertex(pygame.sprite.Sprite):
    def __init__(self, position):
        pygame.sprite.Sprite.__init__(self)
        (self.x, self.y) = position
        self.set_type(False)
        self.adjacent = []
        
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
    
    def add_adjacent(self, vertex, weight):
        self.adjacent.append((vertex,weight))


class Edge:
    def __init__(self, position_beginning, position_end, vertex_beginning):
        self.vertex_beginning = vertex_beginning
        self.position_beginning = position_beginning
        self.position_end = position_end
        self.visible = True
    def draw(self, surface):
        if self.visible == True:
            pygame.draw.line(surface, (0,0,0), self.position_beginning, self.position_end, 3)
    def update_position(self, position_beginning, position_end):
        self.position_beginning = position_beginning
        self.position_end = position_end
    def set_vertex_end(self, vertex_end):
        self.vertex_end = vertex_end
        self.position_end = (vertex_end.x, vertex_end.y)
    def distance_rectangle(self,vertex_beginning, vertex_end):
        surface = (((self.vertex_beginning.x + self.vertex_end.x)/2),((self.vertex_beginning.y+self.vertex_end.y)/2))
        return surface
        


        
    
        
        
    
        
        
        
#tu jest jakby main, tworzę nowe okno programu
application = Application()        