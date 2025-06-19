import pygame as py
import random
import stack

# Constants
WIDTH = 320
HEIGHT = 320
GRID_SIZE = 10
ROWS = HEIGHT // GRID_SIZE
COLUMNS = WIDTH // GRID_SIZE
INITIAL = (0, 0)

# Initialize Pygame
py.init()
clock = py.time.Clock()
screen = py.display.set_mode((WIDTH, HEIGHT))
screen.fill((0, 0, 0))  

# Draw initial white grid (walls)
for i in range(COLUMNS + 1):
    py.draw.line(screen, py.Color(255, 255, 255), (GRID_SIZE * i, 0), (GRID_SIZE * i, HEIGHT))
for j in range(ROWS + 1):
    py.draw.line(screen, py.Color(255, 255, 255), (0, GRID_SIZE * j), (WIDTH, GRID_SIZE * j))

py.display.flip()

#checks if the point is not outside the walls
def in_range_of_gird(point):
    x, y = point
    return 0 <= x < WIDTH and 0 <= y < HEIGHT

#checks the neighbours for a given point and whether they are visited or not 
def check_neighbours(nodes, point, grid_size):
    neighbours = []
    x, y = point

    directions = [
        (x, y - grid_size),  # up
        (x, y + grid_size),  # down
        (x - grid_size, y),  # left
        (x + grid_size, y)   # right
    ]

    for n in directions:
        if in_range_of_gird(n) and not nodes.visited(n):
            neighbours.append(n)

    if neighbours:
        current = random.choice(neighbours)
        x2, y2 = current

        # Carve out wall between point and current
        if current == (x, y - grid_size):  # UP
            py.draw.line(screen, py.Color(0, 0, 0), (x, y), (x + grid_size, y))
        elif current == (x, y + grid_size):  # DOWN
            py.draw.line(screen, py.Color(0, 0, 0), (x, y + grid_size), (x + grid_size, y + grid_size))
        elif current == (x - grid_size, y):  # LEFT
            py.draw.line(screen, py.Color(0, 0, 0), (x, y), (x, y + grid_size))
        elif current == (x + grid_size, y):  # RIGHT
            py.draw.line(screen, py.Color(0, 0, 0), (x + grid_size, y), (x + grid_size, y + grid_size))

        return current

    return None


# Maze generation using DFS with a stack
nodes = stack.Stack()
current = INITIAL
nodes.push(current)

# Optional: draw start cell
py.draw.rect(screen, py.Color(0, 255, 0), py.Rect(current, (GRID_SIZE, GRID_SIZE)))
py.display.flip()

running = True

while running:
    if not nodes.is_empty():
        next_cell = check_neighbours(nodes, current, GRID_SIZE)
        if next_cell:
            nodes.push(next_cell)
            py.draw.line(screen,py.Color(0, 0, 255),(current[0] + GRID_SIZE // 2, current[1] + GRID_SIZE // 2),(next_cell[0] + GRID_SIZE // 2, next_cell[1] + GRID_SIZE // 2),1)
            current = next_cell
            
        else:
            nodes.pop()
            if not nodes.is_empty():
                current = nodes.peek()
        py.display.flip()
    else:
        break

    for event in py.event.get():
        if event.type == py.QUIT:
            running = False

    clock.tick(60)

# Optional: mark end cell
py.draw.rect(screen, py.Color(255, 0, 0), py.Rect((WIDTH - GRID_SIZE, HEIGHT - GRID_SIZE), (GRID_SIZE, GRID_SIZE)))
py.display.flip()

# Wait until user closes window
done = False
while not done:
    for event in py.event.get():
        if event.type == py.QUIT:
            done = True

py.quit()