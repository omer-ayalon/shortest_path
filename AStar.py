import math
import sys
from os import environ

environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import pygame

pygame.init()

pygame.display.set_caption('Dijkstra Algorithm')

fps = 60
fpsClock = pygame.time.Clock()

screen_size = 600
screen = pygame.display.set_mode((screen_size, screen_size))

nodes_per_axis = 20
nodes_size = screen_size / nodes_per_axis

Font = pygame.font.SysFont('timesnewroman', 15)


class Node:
    def __init__(self, pos):
        self.block = False
        self.pos = pos
        self.visited = False
        self.previous_cell = [None, None]
        self.g_cost = float('inf')
        self.h_cost = float('inf')
        self.f_cost = float('inf')

    def draw(self):
        if self.visited:
            color = (255, 0, 0)
        elif self.block:
            color = (100, 100, 100)
        elif self.f_cost < float('inf'):
            color = (0, 255, 0)
        else:
            color = (0, 0, 0)

        pygame.draw.rect(screen, color,
                         [self.pos[1] * nodes_size, self.pos[0] * nodes_size, nodes_size, nodes_size])

        # if not self.block:
        #     num = Font.render(str(self.g_cost), True, (0, 0, 255))
        #     screen.blit(num, [self.pos[1] * nodes_size + nodes_size / 200, self.pos[0] * nodes_size + nodes_size / 200])
        #
        #     num = Font.render(str(self.h_cost), True, (0, 0, 255))
        #     screen.blit(num, [self.pos[1] * nodes_size + nodes_size / 2, self.pos[0] * nodes_size])
        #
        #     num = Font.render(str(self.f_cost), True, (0, 0, 255))
        #     screen.blit(num, [self.pos[1] * nodes_size + nodes_size / 3, self.pos[0] * nodes_size + nodes_size / 3])


class AStar:
    def __init__(self):
        self.start_cell = [0, 0]
        self.end_cell = [nodes_per_axis - 1, nodes_per_axis - 1]
        self.current_cell = self.start_cell
        self.grid = [[Node([i, j]) for j in range(nodes_per_axis)] for i in range(nodes_per_axis)]
        self.done = False
        self.start = False
        self.path = []
        self.grid[self.start_cell[0]][self.start_cell[1]].g_cost = 0

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

    def backtracker_path(self):
        self.path = [self.end_cell]
        while self.path[-1][0] != self.start_cell[0] or self.path[-1][1] != self.start_cell[1]:
            self.path.append(self.grid[self.path[-1][0]][self.path[-1][1]].previous_cell)

    def calc_score(self, pos1, pos2):
        pass

    def step(self):
        if not self.done:
            self.grid[self.current_cell[0]][self.current_cell[1]].visited = True

            if self.current_cell == self.end_cell:
                self.backtracker_path()
                self.done = True
                return

            neighbors = self.get_neighbors()

            if len(neighbors) > 0:
                for neighbor in neighbors:
                    # Calculate Distance Score From Neighbor Cell To End Cell
                    dist = [abs(neighbor[1] - self.end_cell[1]), abs(neighbor[0] - self.end_cell[0])]
                    if dist[0] != dist[1]:
                        score_to_end = 14 * (max(dist) - abs(dist[0] - dist[1])) + abs(dist[0] - dist[1]) * 10
                    else:
                        score_to_end = dist[0] * 14

                    score_to_start = self.grid[self.current_cell[0]][self.current_cell[1]].g_cost + int(math.sqrt(
                        abs((neighbor[0] - self.current_cell[0]) * 10) ** 2 + abs(
                            (neighbor[1] - self.current_cell[1]) * 10) ** 2))

                    # If Score Is Better, Replace Score
                    if self.grid[neighbor[0]][neighbor[1]].f_cost > score_to_start + score_to_end:
                        self.grid[neighbor[0]][neighbor[1]].previous_cell = self.current_cell

                        self.grid[neighbor[0]][neighbor[1]].g_cost = score_to_start

                        self.grid[neighbor[0]][neighbor[1]].h_cost = score_to_end
                        self.grid[neighbor[0]][neighbor[1]].f_cost = score_to_end + score_to_start

            # Flatten The Grid For Sorting
            flatten_grid = [j for sub in self.grid for j in sub]
            # Sorting For Not Visited And Lowest Score
            flatten_grid = sorted(flatten_grid, key=lambda x: (x.visited, x.f_cost))
            arr = [flatten_grid[0]]
            for node in flatten_grid[1:]:
                if flatten_grid[0].f_cost == node.f_cost and not node.visited:
                    arr.append(node)

            if len(arr) > 1:
                arr = sorted(arr, key=lambda x: x.h_cost)

            # Choose The Next Cell To Be Visited
            if not arr[0].visited:
                self.current_cell = arr[0].pos

    def draw_blocks(self):
        mouse_click = pygame.mouse.get_pressed()
        mouse_pos = pygame.mouse.get_pos()
        if mouse_click[0]:
            self.grid[int(mouse_pos[1] // nodes_size)][int(mouse_pos[0] // nodes_size)].block = True
        elif mouse_click[2]:
            self.grid[int(mouse_pos[1] // nodes_size)][int(mouse_pos[0] // nodes_size)].block = False

    def draw(self):
        # Draw Grid
        for i in range(nodes_per_axis + 1):
            pygame.draw.line(screen, (255, 255, 255), [0, i * nodes_size], [screen_size, i * nodes_size])
            pygame.draw.line(screen, (255, 255, 255), [i * nodes_size, 0], [i * nodes_size, screen_size])

        # Draw Path If Done, Else Draw Current Cell
        if self.done:
            for pos in self.path:
                pygame.draw.circle(screen, (0, 0, 255),
                                   [pos[1] * nodes_size + nodes_size / 2, pos[0] * nodes_size + nodes_size / 2], 5)
        else:
            pygame.draw.rect(screen, (0, 0, 255), [self.current_cell[1] * nodes_size, self.current_cell[0] * nodes_size,
                                                   nodes_size, nodes_size])


astar = AStar()

while True:
    screen.fill((0, 0, 0))

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
            if event.key == pygame.K_RETURN:
                astar.start = True

    if astar.start:
        astar.step()
    else:
        astar.draw_blocks()

    for row_node in astar.grid:
        for node in row_node:
            node.draw()

    astar.draw()

    pygame.display.flip()
    fpsClock.tick(fps)
