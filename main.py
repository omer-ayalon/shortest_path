import numpy as np
import sys
import pygame


def find_neighbor(pos):
    neighbors = []
    if grid_map[pos[0]+1][pos[1]] == 0:  # Search Down
        neighbors.append([pos[0]+1, pos[1]])
    if grid_map[pos[0]-1][pos[1]] == 0:  # Search Up
        neighbors.append([pos[0]-1, pos[1]])
    if grid_map[pos[0]][pos[1]-1] == 0:  # Search Left
        neighbors.append([pos[0], pos[1]-1])
    if grid_map[pos[0]][pos[1]+1] == 0:  # Search Right
        neighbors.append([pos[0], pos[1]+1])

    return neighbors


def find_path():
    tmp = np.array(curr_pos)
    path = [tmp]

    while np.any(np.not_equal(path[-1], start_pos)):
        path.append(priors[int(tmp[0])][int(tmp[1])])
        tmp = priors[int(tmp[0])][int(tmp[1])]

    path = path[0:-1]
    return path


def draw():
    screen.fill('black')

    for i in range(grid_map.shape[0]):
        for j in range(grid_map.shape[1]):
            if grid_map[i][j] == 1:
                pygame.draw.rect(screen, 'purple', [j * a, i * a, a, a])

    for pos in visited_pos:
        pygame.draw.rect(screen, 'white', [pos[1] * a, pos[0] * a, a, a])

    for pos in queue:
        pygame.draw.rect(screen, 'grey', [pos[1] * a, pos[0] * a, a, a])

    pygame.draw.rect(screen, 'green', [start_pos[1] * a, start_pos[0] * a, a, a])
    pygame.draw.rect(screen, 'red', [end_pos[1] * a, end_pos[0] * a, a, a])

    if not searching:
        path = find_path()
        for pos in path:
            pygame.draw.rect(screen, 'blue', [pos[1] * a, pos[0] * a, a, a])

    pygame.display.flip()


pygame.init()

fps = 60
fpsClock = pygame.time.Clock()

width, height = 640, 480
screen = pygame.display.set_mode((width, height))

start_pos = [1, 1]
end_pos = [5, 18]
visited_pos = []
queue = [start_pos]
grid_map = np.array([[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                     [1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                     [1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                     [1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                     [1, 0, 0, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1],
                     [1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1],
                     [1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1],
                     [1, 0, 0, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1],
                     [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1],
                     [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1],
                     [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                     [1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                     [1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                     [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                     [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                     [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]])
priors = np.zeros([grid_map.shape[0], grid_map.shape[1], 2])


a = 25
searching = True
# Game loop.
while True:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                sys.exit()

    # Update.
    if searching:
        curr_pos = queue.pop(0)

        visited_pos.append(curr_pos)
        neighbors = find_neighbor(curr_pos)
        for neighbor in neighbors:
            if neighbor not in queue and neighbor not in visited_pos:
                if neighbor == end_pos:
                    searching = False
                    break
                priors[neighbor[0]][neighbor[1]] = curr_pos
                queue.append(neighbor)

    draw()
    fpsClock.tick(fps)
