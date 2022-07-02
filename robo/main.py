from array import array
from asyncio.windows_events import NULL
import pygame
import sys
import time
from collections import defaultdict
from queue import PriorityQueue
import random

PURPLE = (148,0,211)
GOLD = (255,215,0)
BLACK = (0, 0, 0)
GREEN = (124,252,0)
ROBO = (230,0,126)
BLUE = (30, 144, 255)
ORANGE = (210, 105, 30)
ORANGE_HOT = (255, 131, 30)
BROWN = (160,82,45)
YELLOW = (255, 255, 0)
GRAY = (128, 128, 128)
RED = (255, 0, 0)
WHITE = (255, 255, 255)


with open("fabricas.txt") as f:
    fabricas = f.readlines()

fabricas = [list(map(int, x.strip().split())) for x in fabricas]
fb_array = []
for item in fabricas:
    fb_array += item

# print(fb_array)
FB_COR = [
    [fb_array[0], fb_array[1]],
    [fb_array[2], fb_array[3]],
    [fb_array[4], fb_array[5]],
    [fb_array[6], fb_array[7]],
    [fb_array[8], fb_array[9]],
]

POS_FABRICAS = [
    FB_COR[0][0] * 42 + FB_COR[0][1],
    FB_COR[1][0] * 42 + FB_COR[1][1],
    FB_COR[2][0] * 42 + FB_COR[2][1],
    FB_COR[3][0] * 42 + FB_COR[3][1],
    FB_COR[4][0] * 42 + FB_COR[4][1]
]

ROBO_CORD = [17,26]

POS_AUX = []

CORES_FERRAMENTAS = [YELLOW, BLACK, GRAY, RED, WHITE]

TOOL1CORD = []
TOOL2CORD = []
TOOL3CORD = []
TOOL4CORD = []
TOOL5CORD = []
TOOL1 = []
TOOL2 = []
TOOL3 = []
TOOL4 = []
TOOL5 = []

colors = [GREEN, BROWN, BLUE, ORANGE]

MARGIN = 1
WIDTH = 600 / 42 - MARGIN
HEIGHT = 600 / 42 - MARGIN
WINDOW_SIZE = [600, 600]

pygame.init()

screen = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("ROBO")
clock = pygame.time.Clock()

screen.fill(BLACK)

with open("mapa.txt") as m:
    mapa = m.readlines()

mapa = [list(map(int, x.strip().split())) for x in mapa]
mapa_array = []
for item in mapa:
    mapa_array += item

# posx, posy = map(int, input("Digite a posição inicial: ").split())
posx, posy = 1, 1
start = 42*posx + posy
# destx, desty = map(int, input("Digite a posição de destino: ").split())
destx, desty = 41,41
end = 42*destx + desty

global cont_dijkstra 
global cont_aStar 


print(f'start: {start} end: {end}')

class Adjacencia():
    def __init__(self, values):
        self.adj = defaultdict(list) # adj[0] -> [1, 42] 
        self.values = values # mapa.txt em vetor
        self.valueCorreto = {0:1, 1:5,2:10,3:15}
        self.length = 42**2
        self.cont = 0
        self.dist = [sys.maxsize] * (self.length)
        self.current_position_robo = ROBO_CORD[0] * 42 + ROBO_CORD[1]
        self.qtd_tool1 = 0
        self.qtd_tool2 = 0
        self.qtd_tool3 = 0
        self.qtd_tool4 = 0
        self.qtd_tool5 = 0
        self.pos_fab_1 = []
        self.pos_fab_2 = []
        self.pos_fab_3 = []
        self.pos_fab_4 = []
        self.pos_fab_5 = []
        self.visionRobot = []
        self.fabricas_atendidas = 0
        self.contagemIteracoes = 0
        self.iteraction = True

        self.fill()

    def routineDrawMap(self):
        self.drawMapa()
        pygame.time.wait(300)
        pygame.display.flip()

    def rotinaAStarPathStar(self, start, end, color=PURPLE):
        self.drawMapa()
        pygame.time.wait(300)
        print("iniciando A*")
        self.astar(start, end, color)
        pygame.display.flip()
        pygame.time.wait(300)
        print("iniciando pathA*")
        return self.pathStar(start,end)

    def roboAndaAteFerramenta(self, path):
        pygame.display.flip()
        for position in path:
            self.current_position_robo = ((position//42) * 42) + (position%42)
            self.routineDrawMap()

    def settingPr(self):
        pr = self.current_position_robo

        vision = [
            pr, #pos atual
            pr-1, pr+1, pr+42, pr-42, pr+43, pr-43, pr-41, pr+41, pr-2, pr+2, pr+42*2, pr-42*2, pr-3, pr+3,
            pr+42*3, pr-42*3, pr+42*2+1, pr-42*2+1, pr+42*2-1, pr-42*2-1, pr+44, pr-44,pr-40, pr+40, pr-4, pr+4,
            pr+42*4, pr-42*4, pr+45, pr-45, pr+39, pr-39, pr+42*2+2, pr+42*2+3, pr-42*2+2, pr-42*2+3, pr+42*2-2,
            pr+42*3-1,pr+42*3-2, pr-42*3-1,  pr-42*4+1,pr-42*4+2, pr-42*3+1,pr-42*3+2,pr+42*3+1, pr-42*2-2,
            pr+46, pr+38, pr+42*2+4, pr+42*2-3, pr+42*2-4,pr+42*3+2, pr+42*3+3, pr+42*3+4, pr+42*3-3, pr+42*3-4,
            pr+42*4+1,pr+42*4+2, pr+42*4+3, pr+42*4+4, pr+42*4-1,pr+42*4-2, pr+42*4-3, pr+42*4-4,pr-46, pr-38,
            pr-42*2+4, pr-42*2-3, pr-42*2-4,pr-42*3+3, pr-42*3+4, pr-42*3-2, pr-42*3-3, pr-42*3-4,pr-42*4+3,
            pr-42*4+4, pr-42*4-1,pr-42*4-2, pr-42*4-3, pr-42*4-4,
        ]
        self.visionRobot = vision
        return pr//42, pr%42, vision

    def findedManfc(self, start, end, color, id_fabrica):
        path = self.rotinaAStarPathStar(start, end, color=color) #Aqui tenho o caminho 
        path.reverse() # caminho certo
        self.roboAndaAteFerramenta(path)
        posx, posy, array_vision = self.settingPr()
        self.fabricas_atendidas += 1
        print("Manutenção fabrica:", id_fabrica )
        return posx, posy, array_vision

    def findedTool(self, start, end):
        path = self.rotinaAStarPathStar(start, end) #Aqui tenho o caminho 
        path.reverse() # caminho certo
        self.roboAndaAteFerramenta(path)
        posx, posy, array_vision = self.settingPr()
        pygame.display.flip()
        return posx, posy, array_vision

    def walkRobot(self):
        if self.current_position_robo <= 0:
            passo = random.randint(3, 4)
        elif self.current_position_robo >= 1764:
            passo = random.randint(1, 2)
        else:
            passo = random.randint(1, 4)
            
        if passo == 1: #pra cima
            self.current_position_robo -= 42
        elif passo == 2: #pra esquerda
            self.current_position_robo -= 1
        elif passo == 3: #pra baixo
            self.current_position_robo += 42
        elif passo == 4: #pra direita
            self.current_position_robo += 1
        
        self.routineDrawMap()


    def rotinaExperimentacao(self, start, end, idIteracao):
        # pygame.time.wait(3000)
        print('BFS')
        bfs = self.road(start, end)
        pygame.image.save(screen,"greedy_way.jpg")
        self.routineDrawMap()
        # input('ENTER para continuar com DIJKSTRA')
        print('DIJKSTRA')
        dij = self.path(start,end)
        pygame.image.save(screen,"dijkstra_way.jpg")
        self.routineDrawMap()
        print('A*')
        self.astar(start, end)
        aux, ast = self.pathStar(start,end)
        pygame.image.save(screen,"astar_way.jpg")
        # input('ENTER para sair')
        # pygame.quit()
        # pygame.time.wait(3000)
        string1 = "##### RESULTADOS ITERAÇÃO:" + str(idIteracao) + "#####"
        string2 = "Qnt. nós visitados -- BFS: " + str(bfs[0]) + " - Dijkstra: "+ str(dij[0]) + " - A*: " + str(ast[0])
        string3 = "Custo -- BFS: " + str(bfs[1])+ " - Dijkstra: "+ str(dij[1]) + " - A*: "+ str(ast[1])

        
        arquivo = open('experimentacao.txt','a')
        arquivo.write(string1 + "\n")
        arquivo.write(string2 + "\n")
        arquivo.write(string3 + "\n")
        arquivo.close()

        exit()

    def visionTools(self):
        posx, posy, array_vision = self.settingPr()
        have_tool_in_vision = True
        count_tool_in_vision = 0

        while have_tool_in_vision:
            for pos in array_vision:
                if count_tool_in_vision == len(array_vision):
                    have_tool_in_vision = False
                else:
                    if pos in POS_FABRICAS:
                        index_aux = POS_FABRICAS.index(pos)
                        aux_x = pos//42
                        aux_y = pos%42

                        if index_aux == 0 and len(self.pos_fab_1) == 0:
                            self.pos_fab_1.append(aux_x)
                            self.pos_fab_1.append(aux_y)
                        elif index_aux == 1 and len(self.pos_fab_2) == 0:
                            self.pos_fab_2.append(aux_x)
                            self.pos_fab_2.append(aux_y)
                        elif index_aux == 2 and len(self.pos_fab_3) == 0:
                            self.pos_fab_3.append(aux_x)
                            self.pos_fab_3.append(aux_y)
                            print(self.pos_fab_3[0])
                        elif index_aux == 3 and len(self.pos_fab_4) == 0:
                            self.pos_fab_4.append(aux_x)
                            self.pos_fab_4.append(aux_y)
                        elif index_aux == 4 and len(self.pos_fab_5) == 0:
                            self.pos_fab_5.append(aux_x)
                            self.pos_fab_5.append(aux_y)

                    if self.qtd_tool1 == 20:
                        if len(self.pos_fab_1) > 0:
                            posx, posy, array_vision = self.findedManfc((42*posx + posy),(42*self.pos_fab_1[0] + self.pos_fab_1[1]), PURPLE,1)
                            self.qtd_tool1 = 0
                    elif self.qtd_tool2 == 10:
                        if len(self.pos_fab_2) > 0:
                            posx, posy, array_vision = self.findedManfc((42*posx + posy),(42*self.pos_fab_2[0] + self.pos_fab_2[1]), PURPLE,2)
                            self.qtd_tool2 = 0
                    elif self.qtd_tool3 == 8:
                        if len(self.pos_fab_3) > 0:
                            posx, posy, array_vision = self.findedManfc((42*posx + posy),(42*self.pos_fab_3[0] + self.pos_fab_3[1]), PURPLE,3)
                            self.qtd_tool3 = 0
                    elif self.qtd_tool4 == 6:
                        if len(self.pos_fab_4) > 0:
                            posx, posy, array_vision = self.findedManfc((42*posx + posy),(42*self.pos_fab_4[0] + self.pos_fab_4[1]), PURPLE,4)
                            self.qtd_tool4 = 0
                    elif self.qtd_tool5 == 4:
                        if len(self.pos_fab_5) > 0:
                            posx, posy, array_vision = self.findedManfc((42*posx + posy),(42*self.pos_fab_5[0] + self.pos_fab_5[1]), PURPLE,5)
                            self.qtd_tool5 = 0

                    if pos in TOOL1:
                            posx, posy, array_vision = self.findedTool((42*posx + posy), (42*(pos//42) + pos%42))
                            self.qtd_tool1 += 1
                            del TOOL1[TOOL1.index(pos)]
                            pygame.display.flip()
                            count_tool_in_vision = 0
                            break
                    elif pos in TOOL2:
                            posx, posy, array_vision = self.findedTool((42*posx + posy), (42*(pos//42) + pos%42))
                            self.qtd_tool2 += 1
                            del TOOL2[TOOL2.index(pos)]
                            pygame.display.flip()
                            count_tool_in_vision = 0
                            break
                    elif pos in TOOL3:
                            posx, posy, array_vision = self.findedTool((42*posx + posy), (42*(pos//42) + pos%42))
                            self.qtd_tool3 += 1
                            del TOOL3[TOOL3.index(pos)]
                            pygame.display.flip()
                            count_tool_in_vision = 0
                            break

                    elif pos in TOOL4:
                            posx, posy, array_vision = self.findedTool((42*posx + posy), (42*(pos//42) + pos%42))
                            self.qtd_tool4 += 1
                            del TOOL4[TOOL4.index(pos)]
                            pygame.display.flip()
                            count_tool_in_vision = 0
                            break
                
                    elif pos in TOOL5:
                            posx, posy, array_vision = self.findedTool((42*posx + posy), (42*(pos//42) + pos%42))
                            self.qtd_tool5 += 1
                            del TOOL5[TOOL5.index(pos)]
                            pygame.display.flip()
                            count_tool_in_vision = 0
                            break
                    else:
                        count_tool_in_vision += 1

    def generateTool(self):
        X = random.randint(1,41)
        Y = random.randint(1,41)
        number_TMP = X * 42 + Y

        while number_TMP in POS_AUX or number_TMP in POS_FABRICAS or self.values[number_TMP] != 0:
            X = random.randint(1,41)
            Y = random.randint(1,41)
            number_TMP = X * 42 + Y
        
        return X, Y, number_TMP

    def generateTools(self):
        for i in range(20):
            cord_x, cord_y, number_TMP = self.generateTool()
            POS_AUX.append(number_TMP)
            TOOL1.append(number_TMP)
            TOOL1CORD.append([cord_x,cord_y])

        for i in range(10):
            cord_x, cord_y, number_TMP = self.generateTool()
            POS_AUX.append(number_TMP)
            TOOL2.append(number_TMP)
            TOOL2CORD.append([cord_x,cord_y])

        for i in range(8):
            cord_x, cord_y, number_TMP = self.generateTool()
            POS_AUX.append(number_TMP)
            TOOL3.append(number_TMP)
            TOOL3CORD.append([cord_x,cord_y])

        for i in range(6):
            cord_x, cord_y, number_TMP = self.generateTool()
            POS_AUX.append(number_TMP)
            TOOL4.append(number_TMP)
            TOOL4CORD.append([cord_x,cord_y])
    
        for i in range(4):
            cord_x, cord_y, number_TMP = self.generateTool()
            POS_AUX.append(number_TMP)
            TOOL5.append(number_TMP)
            TOOL5CORD.append([cord_x,cord_y])

    def fill(self):
        for i in range(42):
            for j in range(42):
                vizinhos = [(i-1, j),(i, j+1),(i+1,j),(i, j-1)] #vizinhos possiveis: norte leste sul oeste
                vizinhos = [x for x in vizinhos if (x[0] >= 0 and x[0] < 42) and (x[1] >= 0 and x[1] < 42)] #vizinhos ctz: norte leste sul oeste
                for (x,y) in vizinhos:
                    self.adj[42*i + j].append(42*x + y)
    
    def drawMapa(self):
        if self.cont == 0:
            self.generateTools()
            self.cont += 1
        
        # print(TOOL4)
        # print(POS_FABRICAS)
        for s in range(self.length):
            color = colors[self.values[s]]
            pygame.draw.rect(
                screen,
                color,
                [(MARGIN + WIDTH) * (s%42) + MARGIN,
                (MARGIN + HEIGHT) * (s//42) + MARGIN,
                WIDTH,
                HEIGHT]
            )

            if s == self.current_position_robo:
                color = ROBO
                pygame.draw.rect(
                screen,
                BLACK,
                [(MARGIN + WIDTH) * (s%42) + MARGIN + 1,
                (MARGIN + HEIGHT) * (s//42) + MARGIN + 1,
                WIDTH - 2,
                HEIGHT - 2]
                )

                pygame.draw.rect(
                screen,
                color,
                [(MARGIN + WIDTH) * (s%42) + MARGIN + 2,
                (MARGIN + HEIGHT) * (s//42) + MARGIN + 2,
                WIDTH - 4,
                HEIGHT - 4]
                )
            # elif s in self.visionRobot:
            #     color = CORES_FERRAMENTAS[0]
            #     pygame.draw.rect(
            #     screen,
            #     BLACK,
            #     [(MARGIN + WIDTH) * (s%42) + MARGIN + 1,
            #     (MARGIN + HEIGHT) * (s//42) + MARGIN + 1,
            #     WIDTH - 2,
            #     HEIGHT - 2]
            #     )

            #     pygame.draw.rect(
            #     screen,
            #     color,
            #     [(MARGIN + WIDTH) * (s%42) + MARGIN + 2,
            #     (MARGIN + HEIGHT) * (s//42) + MARGIN + 2,
            #     WIDTH - 4,
            #     HEIGHT - 4]
            #     )
            elif s in POS_FABRICAS:
                if s == POS_FABRICAS[0]:
                    color = CORES_FERRAMENTAS[0]
                elif s == POS_FABRICAS[1]:
                    color = CORES_FERRAMENTAS[1]
                elif s == POS_FABRICAS[2]:
                    color = CORES_FERRAMENTAS[2]
                elif s == POS_FABRICAS[3]:
                    color = CORES_FERRAMENTAS[3]
                elif s == POS_FABRICAS[4]:
                    color = CORES_FERRAMENTAS[4]
            
                pygame.draw.rect(
                screen,
                BLACK,
                [(MARGIN + WIDTH) * (s%42) + MARGIN + 1,
                (MARGIN + HEIGHT) * (s//42) + MARGIN + 1,
                WIDTH - 2,
                HEIGHT - 2]
                )

                pygame.draw.rect(
                screen,
                color,
                [(MARGIN + WIDTH) * (s%42) + MARGIN + 2,
                (MARGIN + HEIGHT) * (s//42) + MARGIN + 2,
                WIDTH - 4,
                HEIGHT - 4]
                )

            else:
                if s in TOOL1:
                    color = CORES_FERRAMENTAS[0]
                elif s in TOOL2:
                    color = CORES_FERRAMENTAS[1]
                elif s in TOOL3:
                    color = CORES_FERRAMENTAS[2]
                elif s in TOOL4:
                    color = CORES_FERRAMENTAS[3]
                elif s in TOOL5:
                    color = CORES_FERRAMENTAS[4]
                else:
                    color = colors[self.values[s]]

                pygame.draw.circle(
                    screen,
                    color,
                    ((MARGIN + WIDTH) * (s%42) + 7,
                    (MARGIN + HEIGHT) * (s//42) + 7),
                    5
                    )
        clock.tick(120)

    def caminho(self,s, color):
        pygame.draw.rect(
            screen,
            color,
            [(MARGIN + WIDTH) * (s%42) + MARGIN,
            (MARGIN + HEIGHT) * (s//42) + MARGIN,
            WIDTH,
            HEIGHT]
        )
        clock.tick(120000)
        time.sleep(0.000000001)
        pygame.display.flip()

    def bfs(self, visited, start, end):
        self.routineDrawMap()
        prev = {}
        visited.append(start)
        queue = []
        queue.append(start)
        while(queue):
            s = queue.pop(0)
            #print(f'({s//42},{s%42})', end=' ')
            if s == end:
                return prev
            for neighbour in self.adj[s]:
                if neighbour not in visited:
                    prev[neighbour] = s
                    visited.append(neighbour)
                    queue.append(neighbour)
            color = PURPLE
            self.caminho(s, color)   
                #self.drawMapa()

    def road(self, start, end):
        prev = self.bfs([], start, end)
        whereami = end
        road = [whereami]
        pygame.image.save(screen,"greedy_expansion.jpg")
        # input("Aperte ENTER para continuar")
        self.routineDrawMap()
        while(whereami != start):
            whereami = prev[whereami]
            road.append(whereami)
        road = [(x, self.valueCorreto[self.values[x]]) for x in road[::-1]]
        color = GOLD
        for item in road:
            self.caminho(item[0], color)
        road2 = [x[1] for x in road]
        return (len(prev), sum(road2))
        #print(f'\n\nroad {road}')

    def distance(self, visited):
        minimo = sys.maxsize
        for i in range(self.length):
            if self.dist[i] < minimo and visited[i] == False:
                minimo = self.dist[i]
                index = i
        return index

    def dijkstra(self, start, end):
        self.routineDrawMap()
        self.dist[start] = 0
        visited = [False] * (self.length)
        prev = {}
        current = start
        while current != end:
            #print(f"CURRENT: {current}")
            #print(self.dist[:4])
            current = self.distance(visited)
            #print(f'estou em {current}')
            
            for node in self.adj[current]:
                if self.dist[node] > self.dist[current] + self.valueCorreto[self.values[node]] and not visited[node]:
                    prev[node] = current 
                    self.dist[node] = self.dist[current] + self.valueCorreto[self.values[node]]
            visited[current] = True
            color = PURPLE
            self.caminho(current, color)
            #print(f'{current} visitado')
        return prev

    def path(self, start, end):
        prev = self.dijkstra(start, end)
        pygame.image.save(screen,"dijkstra_expansion.jpg")
        # input("Aperte ENTER para continuar")
        self.routineDrawMap()
        #print('TODOS OS NÓS PERCORRIDOS DIJKSTRA')
        #print(prev)
        #print("passou do dijkstra")
        current = end
        path = [current]
        while current != start:
            current = prev[current]
            path.append(current)
        color = GOLD
        for item in path[::-1]:
            self.caminho(item, color)
        road = [self.valueCorreto[self.values[x]] for x in path[::-1]]
        return (len(prev), sum(road))
        #return path[::-1]


    def dist_manhattan(self, a, b):
        a = (a//42, a%42)
        b = (b//42, b%42)
        #print(a,b)
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def astar(self, start, end, color = PURPLE):
        openset = set()
        g = {}
        g[start] = 0
        h = {}
        h[start] = self.dist_manhattan(end, start)
        openset.add(start) # posicao
        prev = {}
        prev[start] = None
        closedset = set()
        
        while openset:
            current = min(openset, key=lambda x: g[x] + h[x])

            self.caminho(current, color)

            if current == end:
                return prev

            openset.remove(current)
            closedset.add(current)

            for node in self.adj[current]:
                if node in closedset:
                    continue
                if node in openset:
                    new_g = g[current] + self.valueCorreto[self.values[node]]
                    if g[node] > new_g:
                        g[node] = new_g
                        prev[node] = current
                else:
                    g[node] = g[current] + self.valueCorreto[self.values[node]]
                    h[node] = self.dist_manhattan(end, node)
                    prev[node] = current
                    openset.add(node)

    def pathStar(self, start, end):
        #prev = self.aStar(start, end)
        prev = self.astar(start, end)
        pygame.image.save(screen,"astar_expansion.jpg")
        #print('TODOS OS NÓS PERCORRIDOS A*')
        #print(prev)
        # input("Aperte ENTER para continuar")
        self.routineDrawMap()
        current = end
        path = [current]
        while current != start:
            current = prev[current]
            path.append(current)
        color = GOLD
        for item in path[::-1]:
            self.caminho(item, color)
        road = [self.valueCorreto[self.values[x]] for x in path[::-1]]
        return path

# experimentacao()
adj = Adjacencia(mapa_array)
adj.routineDrawMap()
pygame.display.flip()
while adj.fabricas_atendidas < 5:
    adj.walkRobot()
    adj.visionTools()
# # print('BFS')
# # bfs = adj.road(start, end)
# # input('ENTER para continuar com DIJKSTRA')
# # print('DIJKSTRA')
# # dij = adj.path(start,end)
# # input('ENTER para continuar com A*')
# # print('A*')
# # adj.astar(start, end)
# # ast = adj.pathStar(start,end)
# # # input('ENTER para sair')
# pygame.quit()

# # print("##### RESULTADOS #####")
# # print(f"Qnt. nós visitados -- BFS: {bfs[0]} - Dijkstra: {dij[0]} - A*: {ast[0]}")
# # print(f"Custo -- BFS: {bfs[1]} - Dijkstra: {dij[1]} - A*: {ast[1]}")
# # # print(cont_dijkstra)
# # print(cont_aStar)