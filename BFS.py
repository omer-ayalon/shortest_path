import sys
from collections import deque
from os import environ

environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import pygame

pygame.init()
pygame.display.set_caption('BFS Algorithm')

fps = 60
fpsClock = pygame.time.Clock()

screen_size = 600
screen = pygame.display.set_mode((screen_size, screen_size))

nodes_per_axis = 20
nodes_size = screen_size / nodes_per_axis


class Node:
    def __init__(self, pos):
        self.block = False
        self.pos = pos
        self.visited = False
        self.previous_cell = [None, None]

    def draw(self):
        if self.visited:
            color = (255, 0, 0)
        elif self.pos in bfs.queue:
            color = (0, 255, 0)
        elif self.block:
            color = (100, 100, 100)
        else:
            color = (0, 0, 0)

        pygame.draw.rect(screen, color,
                         [self.pos[1] * nodes_size, self.pos[0] * nodes_size, nodes_size, nodes_size])


class BFS:
    def __init__(self):
        self.start_cell = [0, 0]
        self.end_cell = [nodes_per_axis - 1, nodes_per_axis - 1]
        self.current_cell = self.start_cell
        self.done = False
        self.start = False
        self.path = []
        self.grid = [[Node([i, j]) for j in range(nodes_per_axis)] for i in range(nodes_per_axis)]
        self.queue = deque([self.start_cell])

    def get_neighbors(self):
        arr = []
        for direction in [[1, 0], [-1, 0], [0, 1], [0, -1], [1, 1], [-1, -1], [1, -1], [-1, 1]]:
            pos = [self.current_cell[0] + direction[0], self.current_cell[1] + direction[1]]
            if pos[0] < 0 or pos[1] < 0:
                continue
            elif pos[0] > nodes_per_axis - 1 or pos[1] > nodes_per_axis - 1:
                continue
            else:
                if not self.grid[pos[0]][pos[1]].block and not self.grid[pos[0]][pos[1]].visited:
                    arr.append(pos)

        return arr

    def step(self):
        if not self.done:
            self.current_cell = self.queue.popleft()
            if self.current_cell == self.end_cell:
                self.backtracker_path()
                self.done = True

            self.grid[self.current_cell[0]][self.current_cell[1]].visited = True
            neighbors = self.get_neighbors()
            for neighbor in neighbors:
                if not self.grid[neighbor[0]][neighbor[1]].visited and neighbor not in self.queue:
                    self.queue.append(neighbor)
                    self.grid[neighbor[0]][neighbor[1]].previous_cell = self.current_cell

    def backtracker_path(self):
        self.path = [self.end_cell]
        while self.path[-1][0] != self.start_cell[0] or self.path[-1][1] != self.start_cell[1]:
            self.path.append(self.grid[self.path[-1][0]][self.path[-1][1]].previous_cell)

    def draw(self):
        # Draw Grid
        for i in range(nodes_per_axis + 1):
            pygame.draw.line(screen, (255, 255, 255), [0, i * nodes_size], [screen_size, i * nodes_size])
            pygame.draw.line(screen, (255, 255, 255), [i * nodes_size, 0], [i * nodes_size, screen_size])

        # Draw Path If Done, Else Draw Current Cell
        if self.done:
            for pos in self.path:
                pygame.draw.circle(screen, (0, 0, 255),
                                   [pos[1] * nodes_size + nodes_size / 2,
                                    pos[0] * nodes_size + nodes_size / 2], 5)
        else:
            pygame.draw.rect(screen, (0, 0, 255), [self.current_cell[1] * nodes_size, self.current_cell[0] * nodes_size,
                                                   nodes_size, nodes_size])

    def draw_blocks(self):
        mouse_click = pygame.mouse.get_pressed()
        mouse_pos = pygame.mouse.get_pos()
        if 0 < mouse_pos[0] < screen_size and 0 < mouse_pos[1] < screen_size:
            if mouse_click[0]:
                self.grid[int(mouse_pos[1] // nodes_size)][int(mouse_pos[0] // nodes_size)].block = True
            elif mouse_click[2]:
                self.grid[int(mouse_pos[1] // nodes_size)][int(mouse_pos[0] // nodes_size)].block = False


bfs = BFS()

while True:
    screen.fill((0, 0, 0))

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
            if event.key == pygame.K_RETURN:
                bfs.start = True

    if bfs.start:
        bfs.step()
    else:
        bfs.draw_blocks()

    for row in bfs.grid:
        for node in row:
            node.draw()

    bfs.draw()

    pygame.display.flip()
    fpsClock.tick(fps)
