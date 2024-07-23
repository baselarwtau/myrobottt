import pygame
import sys
import time

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
CELL_SIZE = 50  # Adjust based on your preference for cell size
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = pygame.Color.g
GRAY = (200, 200, 200)

# Create the game window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('House Simulation')

# Font for text display
font = pygame.font.Font(None, 36)


def draw_house(screen, house_matrix, current_position, max_battery, max_steps):
    global back_steps
    screen.fill(WHITE)  # Clear the screen with white background

    # Draw cells based on house_matrix
    for y, row in enumerate(house_matrix):
        for x, cell in enumerate(row):
            rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            if cell == 'w':
                pygame.draw.rect(screen, BLACK, rect)  # Draw walls as black rectangles
            elif cell == 'D':
                pygame.draw.rect(screen, 'green', rect)  # Draw docking station as green rectangles
            else:
                pygame.draw.rect(screen, GRAY, rect)  # Draw other cells as gray rectangles

            # Display numbers (1-9) as text
            if cell.isdigit():
                text_surface = font.render(cell, True, BLACK)
                text_rect = text_surface.get_rect(center=rect.center)
                screen.blit(text_surface, text_rect)

            # Highlight current position
            if (x, y) == current_position:
                pygame.draw.circle(screen, (255, 0, 0), rect.center, CELL_SIZE // 4)  # Red circle at current position

    # Draw battery level text
    battery_font = pygame.font.Font(None, 24)  # Adjust font size as needed
    battery_text = battery_font.render(f'Battery: {max_battery}', True, BLACK)
    screen.blit(battery_text, (300, 10))  # Adjust position as needed

    # Draw max steps text
    steps_font = pygame.font.Font(None, 24)  # Adjust font size as needed
    steps_text = steps_font.render(f'remaining steps: {max_steps}', True, BLACK)
    screen.blit(steps_text, (300, 50))  # Adjust position as needed

    # Draw back steps
    back_steps_font = pygame.font.Font(None, 24)  # Adjust font size as needed
    back_steps_text = back_steps_font.render(f'back steps: {back_steps}', True, BLACK)
    screen.blit(back_steps_text, (300, 90))  # Adjust position as needed

    pygame.display.flip()  # Update the display


def reduce(num):
    if num == '1':
        return ' '
    elif num == '2':
        return '1'
    elif num == '3':
        return '2'
    elif num == '4':
        return '3'
    elif num == '5':
        return '4'
    elif num == '6':
        return '5'
    elif num == '7':
        return '6'
    elif num == '8':
        return '7'
    elif num == '9':
        return '8'
    else:
        # Handle unexpected input if needed
        return num  # or raise an error


def read_house_from_file(filename):
    house_matrix = []
    first_line = True
    with open(filename, 'r') as file:
        for line in file:
            # if(first_line):
            #     first_line = False
            #     continue
            row = list(line.strip().split(','))  # Convert each line into a list of characters
            house_matrix.append(row)
    for i in range(len(house_matrix)):
        for j in range(len(house_matrix[i])):
            if (house_matrix[i][j] == ''):
                house_matrix[i][j] = ' '
    return house_matrix


def find_starting_position(house_matrix):
    for y, row in enumerate(house_matrix):
        for x, cell in enumerate(row):
            if cell == 'D':
                return (x, y)  # Return the coordinates (x, y) of 'D'
    return None  # Handle case where 'D' is not found (though it should be there according to your description)


def move(house_matrix, current_position, direction, stay_key):
    global battery_level
    global max_steps
    global back_steps

    x, y = current_position
    # Possible movements: up, down, left, right
    movements = {
        pygame.K_UP: (0, -1),
        pygame.K_DOWN: (0, 1),
        pygame.K_LEFT: (-1, 0),
        pygame.K_RIGHT: (1, 0)
    }
    if direction in movements:
        dx, dy = movements[direction]
        new_x, new_y = x + dx, y + dy

        if 0 <= new_x < len(house_matrix[0]) and 0 <= new_y < len(house_matrix):
            if house_matrix[new_y][new_x] != 'w':  # Check if the cell is not a wall

                # Update current position
                current_position = (new_x, new_y)

                # Decrease battery level
                battery_level -= 1
                if battery_level < 0:
                    battery_level = 0

                # Decrease remain steps
                max_steps -= 1
                if max_steps < 0:
                    max_steps = 0

    # Handle stay action
    elif direction == stay_key:
        if house_matrix[y][x] != 'w' and house_matrix[y][x] != ' ':  # Check if the cell is not a wall
            # Change the cell to empty (' ') if it's a number or space
            if house_matrix[y][x] != 'D':
                house_matrix[y][x] = reduce(house_matrix[y][x])
                # Decrease battery level
                battery_level -= 1
                if battery_level < 0:
                    battery_level = 0

            else:
                back_steps.clear()
                if (battery_level == MAX_BATTERY):
                    max_steps += 1
                elif (battery_level < MAX_BATTERY):
                    battery_level += MAX_BATTERY / 20
                    if (battery_level > MAX_BATTERY):
                        battery_level = MAX_BATTERY

            # Decrease remain steps
            max_steps -= 1
            if max_steps < 0:
                max_steps = 0

    return current_position


def charge(house_matrix, current_position):
    global max_steps
    global battery_level
    global MAX_BATTERY

    back_steps.clear()
    while (max_steps > 0 and battery_level < MAX_BATTERY):
        if (battery_level < MAX_BATTERY):
            battery_level += MAX_BATTERY / 20
            if (battery_level > MAX_BATTERY):
                battery_level = MAX_BATTERY
        max_steps -= 1
        draw_house(screen, house_matrix, current_position, battery_level, max_steps)
        time.sleep(1.5)
    return


def go_to_D(house_matrix, current_position):
    global max_steps
    global battery_level

    x, y = current_position
    if (house_matrix[x][y] == 'D'):
        charge(house_matrix, current_position)
        return

    elif (house_matrix[x][y] != ' ' and battery_level == (len(back_steps) + 1)):
        reduce(house_matrix[x][y])
        battery_level -= 1
        max_steps -= 1
        draw_house(screen, house_matrix, current_position, battery_level, max_steps)
        time.sleep(1.5)

    while (max_steps > 0):
        for position in back_steps[::-1]:
            battery_level -= 1
            max_steps -= 1
            draw_house(screen, house_matrix, position, battery_level, max_steps)
            time.sleep(1.5)
            if position == starting_position:
                draw_house(screen, house_matrix, position, battery_level, max_steps)
                time.sleep(1.5)
                charge(house_matrix, position)
                return
    return


def main(filename):
    global battery_level
    global max_steps
    global MAX_BATTERY
    global back_steps
    global starting_position

    back_steps = []
    # Read the house matrix from file
    house_matrix = read_house_from_file(filename)
    MAX_BATTERY = float(house_matrix[0][0])  # Maximum battery level
    battery_level = MAX_BATTERY  # Initial battery level
    max_steps = int(house_matrix[0][1])
    house_matrix = house_matrix[1:]

    # Find starting position 'D'
    starting_position = find_starting_position(house_matrix)
    if not starting_position:
        print("Starting position 'D' not found in the house matrix.")
        return

    current_position = starting_position

    stay_key = pygame.K_SPACE  # Define the key for staying in the same cell

    while max_steps > 0:
        if (battery_level == len(back_steps) or battery_level == (len(back_steps) + 1)):
            time.sleep(2)
            go_to_D(house_matrix, current_position)
            current_position = starting_position
            continue
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.KEYDOWN:
                # Handle player movement and stay action
                pervios_postion = current_position
                if event.key in [pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT, stay_key]:
                    current_position = move(house_matrix, current_position, event.key, stay_key)
                    if (current_position != pervios_postion):
                        back_steps.append(pervios_postion)

        # Draw the house based on the updated matrix, current position, and battery level
        draw_house(screen, house_matrix, current_position, battery_level, max_steps)
        if (battery_level <= 0 and current_position != starting_position):
            break

    # Game over if battery runs out
    if battery_level == 0:
        print("Game Over: Out of battery!")

    if max_steps == 0:
        print("Game Over: Out of steps!")


inputs = sys.argv
inputs_length = len(inputs)  ### [not important, filename]
if (inputs_length != 2):
    print("An Error Has Occured")
else:
    main(inputs[1])


