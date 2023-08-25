import sys
from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import pygame
from collections import deque

pygame.init()

fps = 60
fpsClock = pygame.time.Clock()

width, height = 640, 480
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Path Finding - BFS')

block_size = 20
grid = [[0] * (width // block_size) for _ in range(height // block_size)]
grid_for_path = [[0, 0] * (width // block_size) for _ in range(height // block_size)]

start_block = [-1, -1]
end_block = [-1, -1]

state = 'draw'

visited_pos = []
queue = deque()

path = []


def draw():
    for i in range(height // block_size):
        for j in range(width // block_size):
            # Draw Barrier Blocks
            if grid[i][j]:
                pygame.draw.rect(screen, (100, 100, 100), [j * block_size, i * block_size, block_size, block_size])

            # Draw The Queue In Green And Visited Positions In Red
            if [i, j] in visited_pos:
                pygame.draw.rect(screen, (255, 0, 0), [j * block_size, i * block_size, block_size, block_size])
            if [i, j] in queue:
                pygame.draw.rect(screen, (0, 255, 0), [j * block_size, i * block_size, block_size, block_size])

            # Draw Start And End Positions
            if start_block == [i, j]:
                pygame.draw.rect(screen, (255, 255, 255), [j * block_size, i * block_size, block_size, block_size])
            if end_block == [i, j]:
                pygame.draw.rect(screen, (0, 0, 255), [j * block_size, i * block_size, block_size, block_size])

            # Draw Grid Lines
            if j == width // block_size - 1:
                pygame.draw.line(screen, (255, 255, 255), [0, i * block_size], [width, i * block_size])
            if i == height // block_size - 1:
                pygame.draw.line(screen, (255, 255, 255), [j * block_size, 0], [j * block_size, height])

    # Draw Path
    if state == 'end':
        for pos in path:
            pygame.draw.rect(screen, (0, 255, 255), [pos[1] * block_size, pos[0] * block_size, block_size, block_size])


def mouse_keyboard_handler():
    global start_block, end_block, queue, state
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
            if state == 'draw':
                if event.key == pygame.K_RETURN:  # It's The Enter Button
                    if start_block[0] >= 0 and end_block[0] >= 0:
                        queue.append(start_block)
                        state = 'algorithm'
                if event.key == pygame.K_s:
                    start_block = pygame.mouse.get_pos()
                    start_block = [start_block[1] // block_size, start_block[0] // block_size]

                if event.key == pygame.K_e:
                    end_block = pygame.mouse.get_pos()
                    end_block = [end_block[1] // block_size, end_block[0] // block_size]

    if state == 'draw':
        mouse_buttons = pygame.mouse.get_pressed()
        if mouse_buttons[0]:
            pos = pygame.mouse.get_pos()
            grid[pos[1] // block_size][pos[0] // block_size] = 1
        if mouse_buttons[2]:
            pos = pygame.mouse.get_pos()
            grid[pos[1] // block_size][pos[0] // block_size] = 0


def get_neighbors(pos):
    neighbors = []
    # Up
    if pos[0] >= 0:
        if not grid[pos[0] - 1][pos[1]]:
            neighbors.append([pos[0] - 1, pos[1]])
    # Down
    if pos[0] < height // block_size - 1:
        if not grid[pos[0] + 1][pos[1]]:
            neighbors.append([pos[0] + 1, pos[1]])
    # Right
    if pos[1] < width // block_size - 1:
        if not grid[pos[0]][pos[1] + 1]:
            neighbors.append([pos[0], pos[1] + 1])
    # Left
    if pos[1] >= 0:
        if not grid[pos[0]][pos[1] - 1]:
            neighbors.append([pos[0], pos[1] - 1])

    return neighbors


def find_path():
    arr = [end_block]
    while arr[-1][0] != start_block[0] or arr[-1][1] != start_block[1]:
        arr.append(grid_for_path[arr[-1][0]][arr[-1][1]])

    arr = arr[1:-1]
    return arr


def algorithm_step():
    global state, path
    curr_pos = queue.popleft()
    if curr_pos == end_block:
        path = find_path()
        state = 'end'
    visited_pos.append(curr_pos)
    neighbors = get_neighbors(curr_pos)
    for neighbor in neighbors:
        if neighbor not in visited_pos and neighbor not in queue:
            queue.append(neighbor)
            grid_for_path[neighbor[0]][neighbor[1]] = curr_pos


def main():
    while True:
        screen.fill((0, 0, 0))

        mouse_keyboard_handler()
        if state == 'algorithm':
            algorithm_step()

        draw()

        pygame.display.flip()
        # if state != 'algorithm':
        fpsClock.tick(fps)


if __name__ == '__main__':
    main()
