import random
import sys
from os import environ

environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import pygame

pygame.init()

pygame.display.set_caption('Dijkstra Algorithm')

fps = 100
fpsClock = pygame.time.Clock()

screen_size = 600
screen = pygame.display.set_mode((screen_size, screen_size))

nodes_per_axis = 20
nodes_size = screen_size / nodes_per_axis

Font = pygame.font.SysFont('timesnewroman', 20)


class Node:
    def __init__(self, pos):
        self.pos = pos
        self.visited = False
        self.weight = random.randrange(10)
        self.previous_cell = [None, None]
        self.score = float('inf')

    def draw(self):
        if self.visited:
            pygame.draw.rect(screen, [self.weight * 255 // 10] * 3,
                             [self.pos[1] * nodes_size, self.pos[0] * nodes_size,
                              nodes_size, nodes_size])
        num = Font.render(str(self.weight), True, (0, 0, 255))
        screen.blit(num, [self.pos[1] * nodes_size + nodes_size / 200, self.pos[0] * nodes_size + nodes_size / 200])


class Dijkstra:
    def __init__(self):
        self.start_cell = [0, 0]
        self.end_cell = [19, 19]
        self.current_cell = self.start_cell
        self.stack = []
        self.grid = [[Node([i, j]) for j in range(nodes_per_axis)] for i in range(nodes_per_axis)]
        self.done = False
        self.start = False
        self.path = []
        self.grid[self.current_cell[0]][self.current_cell[1]].score = 0

    def get_neighbors(self):
        arr = []
        for direction in [[1, 0], [-1, 0], [0, 1], [0, -1]]:
            pos = [self.current_cell[0] + direction[0], self.current_cell[1] + direction[1]]
            if pos[0] < 0 or pos[1] < 0:
                continue
            elif pos[0] > nodes_per_axis - 1 or pos[1] > nodes_per_axis - 1:
                continue
            else:
                if not self.grid[pos[0]][pos[1]].visited:
                    if pos not in self.stack:
                        arr.append(pos)

        return arr

    def backtracker_path(self):
        self.path = [[nodes_per_axis - 1, nodes_per_axis - 1]]
        while self.path[-1][0] != self.start_cell[0] or self.path[-1][1] != self.start_cell[1]:
            self.path.append(self.grid[self.path[-1][0]][self.path[-1][1]].previous_cell)

    def step(self):
        if not self.done:
            if self.grid[self.end_cell[0]][self.end_cell[1]].visited:
                self.done = True
                self.backtracker_path()

            self.grid[self.current_cell[0]][self.current_cell[1]].visited = True
            neighbors = self.get_neighbors()

            if len(neighbors) > 0:
                for neighbor in neighbors:
                    # If Neighbor Cell Score Is Less Than The Current, Replace It
                    if self.grid[neighbor[0]][neighbor[1]].score > self.grid[self.current_cell[0]][
                        self.current_cell[1]].score + \
                            self.grid[neighbor[0]][neighbor[1]].weight:
                        self.grid[neighbor[0]][neighbor[1]].score = self.grid[self.current_cell[0]][
                                                                        self.current_cell[1]].score + \
                                                                    self.grid[neighbor[0]][neighbor[1]].weight
                        self.grid[neighbor[0]][neighbor[1]].previous_cell = self.current_cell

            # Flatten The Grid For Sorting
            flatten_grid = [j for sub in self.grid for j in sub]
            # Sorting For Not Visited And Lowest Score
            flatten_grid = sorted(flatten_grid, key=lambda x: (x.visited, x.score))

            # Choose The Next Cell To Be Visited
            if not flatten_grid[0].visited:
                self.current_cell = flatten_grid[0].pos

    def draw(self):
        if self.done:
            for pos in self.path:
                pygame.draw.circle(screen, (255, 0, 0),
                                   [pos[1] * nodes_size + nodes_size / 2, pos[0] * nodes_size + nodes_size / 2], 5)
        else:
            pygame.draw.rect(screen, (0, 255, 0), [self.current_cell[1] * nodes_size, self.current_cell[0] * nodes_size,
                                                   nodes_size, nodes_size])


dijkstra = Dijkstra()

while True:
    screen.fill((0, 0, 0))

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
            if event.key == pygame.K_RETURN:
                dijkstra.start = True

    if dijkstra.start:
        dijkstra.step()

    for row_node in dijkstra.grid:
        for node in row_node:
            node.draw()

    dijkstra.draw()

    pygame.display.flip()
    fpsClock.tick(fps)
