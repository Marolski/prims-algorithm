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
        self.build_graph()

    def build_graph(self):
        continue_work = True 
        self.starting_vertex = None
        edge_being_drawn = False
        current_edge = None


        
        
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
                            current_edge.vertex_beginning.add_adjacent(found_vertex, current_edge.weight)
                            found_vertex.add_adjacent(current_edge.vertex_beginning, current_edge.weight)
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
                    for e in self.edges:
                        if e.detect_edge_rectangle.collidepoint(pygame.mouse.get_pos()):
                            if e.vertex_end is not None:
                                for v in e.vertex_beginning.adjacent:
                                    if v is e.vertex_end:
                                        e.vertex_beginning.adjacent.remove(v)
                                for v in e.vertex_end.adjacent:
                                    if v is e.vertex_beginning:
                                        e.vertex_beginning.adjacent.remove(v)
                            self.edges.remove(e)
                if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN and not edge_being_drawn:
                    p = Prim(self.vertices, self.edges)
                    p.process_graph()
                    self.draw_minimum_spanning_tree()
                


            if edge_being_drawn:
                current_edge.update_position(current_edge.position_beginning, pygame.mouse.get_pos())
                
                            
            for e in self.edges:
                e.draw(self.screen)
                
            self.vertices.draw(self.screen)
            
            pygame.display.flip()
            
        pygame.quit()
           
    
    def draw_minimum_spanning_tree(self):
        display_minimum_spanning_tree = True
        while display_minimum_spanning_tree:
            self.screen.fill((90, 209, 54))
            for event in pygame.event.get():
                #obsługa kliknięcia na krzyżyk
                if event.type == pygame.QUIT:
                    display_minimum_spanning_tree = False
                    self.continue_work = False
        
            for e in self.edges:
               e.draw(self.screen)     
            self.vertices.draw(self.screen)
            
            pygame.display.flip()
        return
    


class Vertex(pygame.sprite.Sprite):
    def __init__(self, position):
        pygame.sprite.Sprite.__init__(self)
        (self.x, self.y) = position
        self.set_type(False)
        self.adjacent = []
        
        #zmienne tylko i wylacznie do algorytmu
        self.cost = None
        self.connecting_edge = None
        
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
        self.weight = None
        self.detect_edge_rectangle = None
    def update_position(self, position_beginning, position_end):
        self.position_beginning = position_beginning
        self.position_end = position_end
        self.update_weight(position_beginning, position_end)
    def set_vertex_end(self, vertex_end):
        self.vertex_end = vertex_end
        self.position_end = (self.vertex_end.x, self.vertex_end.y)
    def update_weight(self, position_beginning, position_end):
        (x1, y1) = position_beginning
        (x2, y2) = position_end
        self.weight = round(math.sqrt((x1 - x2)**2+(y1-y2)**2)/35, 2)
    def draw(self, surface):
        if self.visible == True:
            set_font = pygame.font.SysFont("comicsansms", 15)
            text = set_font.render(str(self.weight) + "[m]", True, (255, 0, 0))
            weight_display_position = (((self.position_beginning[0] + self.position_end[0])/2),((self.position_beginning[1]+self.position_end[1])/2))
            surface.blit(text,weight_display_position)
            self.detect_edge_rectangle = pygame.Rect(weight_display_position[0]-30, weight_display_position[1]-30, 60, 60)
            pygame.draw.line(surface, (0,0,0), self.position_beginning, self.position_end, 3)


class PriorityQueue: 
    def __init__(self): 
        self.queue = [] 
  
  #wyświetla elementy kolejki oddzielone spacja
    def __str__(self): 
        return ' '.join([str(i) for i in self.queue]) 
  
    # sprawdzanie czy kolejka jest pusta
    def is_empty(self): 
        return len(self.queue) == 0 
  
    # wstawianie elementu do kolejki
    def insert(self, data): 
        self.queue.append(data) 
  
    # zwraca najmniejszy element
    def delete(self):  
            min = 0
            for i in range(len(self.queue)): 
                if self.queue[i].cost < self.queue[min].cost: 
                    min = i 
            item = self.queue[min] 
            del self.queue[min] 
            return item
            
            
class Prim:
    def __init__(self, vertices, edges):
        self.vertices = vertices
        self.edges = edges
    #funkcja która przeprowadza algorytm Prima i czyni wszystkie krawędzie
    #nienależące do MDR niewidzialnymi
    def process_graph(self):
        que = PriorityQueue()
        for v in self.vertices:            
            if v.is_starting_vertex:
                v.cost = 0 
            else:
                v.cost = float("inf")
            que.insert(v)  
        while not que.is_empty():
            u = que.delete()
            for v in u.adjacent:
                edge = self.find_edge(u, v)
                if (edge is not None) and (v in que) and (v.cost > edge.weight):
                    v.cost = edge.weight
                    v.connecting_edge = edge
        for e in self.edges:
            e.visible = False
        for v in self.vertices:
            if v.connecting_edge is not None:
                v.connecting_edge.visible = True
        
    def find_edge(self, vertex_beginning, vertex_end):
        for e in self.edges:
            if ((e.vertex_beginning is vertex_beginning) and (e.vertex_end is vertex_end)) or ((e.vertex_beginning is vertex_end) and (e.vertex_end is vertex_beginning)):
                return e
               
        
         
        
#tu jest jakby main, tworzę nowe okno programu
pygame.init()
application = Application()        