import pygame
import pygame.locals as pl
import threading
import sys
import heapq

from inputs import *

# Initialize pygame
pygame.init()

screen = pygame.display.set_mode((horiz_screen_size, vert_screen_size))
#Print a Title for the window
pygame.display.set_caption("Fire Escape")

floors = []
colors = []

for i in range(number_of_floors):
    floors.append(floor_height)
    if i % 2 == 0:
        colors.append(floor_color_1)
    else:
        colors.append(floor_color_2)

#Compartment Size
compartment_width = building_width/number_of_compartments_per_floor

# Compartments list
compartments = []
for i in range(number_of_compartments_per_floor):
    floor_compartments = []
    for j in range(number_of_floors):
        x_coord = horiz_offset + i * compartment_width
        y_coord = vert_offset + j * floor_height
        floor_compartments.append((x_coord, y_coord))
    compartments.append(floor_compartments)

# Make a list of all clicked compartments from the mouse click detection function
clicked_compartments = [] 

def draw_building(number_of_floors):
    y_coord = vert_offset    #Starting point for drawing the floor at the top of the screen
    for i in range(number_of_floors):
        pygame.draw.rect(screen, colors[i], (25, y_coord, building_width, floors[i]))
        # The first and last compartment of each floor is drawn with a different color_ASPHALT
        pygame.draw.rect(screen, stairway_color, (25, y_coord, compartment_width, floors[i]))
        pygame.draw.rect(screen, stairway_color, (25 + compartment_width * (number_of_compartments_per_floor - 1), y_coord, compartment_width, floors[i]))        
        y_coord +=floors[i]

# Function that draws the main door which takes in the floor and compartment as parameters
def draw_main_door(compartment, floor):
    x, y = get_compartment_coordinates(compartment, floor)
    pygame.draw.rect(screen, door_color, (x, y, compartment_width, floor_height))
    print(compartment, floor)

def get_compartment_coordinates(compartment, floor):
    x, y = compartments[compartment][floor]
    return (x, y)


# Draw stickman function
def draw_stickman(compartment, floor):
    x, y = get_compartment_coordinates(compartment, floor)

    # Draw stickman using the x and y coordinates which starts in the middle of the compartment
    pygame.draw.circle(screen, (0, 0, 0), (x + compartment_width // 2, y + floor_height // 2), radius, width)
    pygame.draw.line(screen, (0, 0, 0), (x + compartment_width // 2, y + floor_height // 2 + radius), (x + compartment_width // 2, y + floor_height // 2 + radius + body_length), width)
    pygame.draw.line(screen, (0, 0, 0), (x + compartment_width // 2, y + floor_height // 2 + radius + body_length // 2), (x + compartment_width // 2 - arm_length, y + floor_height // 2 + radius + body_length // 2), width)
    pygame.draw.line(screen, (0, 0, 0), (x + compartment_width // 2, y + floor_height // 2 + radius + body_length // 2), (x + compartment_width // 2 + arm_length, y + floor_height // 2 + radius + body_length // 2), width)
    pygame.draw.line(screen, (0, 0, 0), (x + compartment_width // 2, y + floor_height // 2 + radius + body_length), (x + compartment_width // 2 - leg_length, y + floor_height // 2 + radius + body_length + leg_length), width)
    pygame.draw.line(screen, (0, 0, 0), (x + compartment_width // 2, y + floor_height // 2 + radius + body_length), (x + compartment_width // 2 + leg_length, y + floor_height // 2 + radius + body_length + leg_length), width)

# Draw a red rectangle with no fill but only outline on each compartment 
def draw_compartment_rectangle():
    for i in range(number_of_floors):
        for j in range(number_of_compartments_per_floor):
            x, y = compartments[j][i]
            pygame.draw.rect(screen, compartment_rectangle_color, (x, y, compartment_width, floor_height), 1)

# Draw a red rectangle with fill, takes in the floor and compartment as parameters. Every drawn compartment is then added to the clicked_compartments list
def draw_compartment_rectangle_fill(compartment, floor):
    x, y = get_compartment_coordinates(compartment, floor)
    pygame.draw.rect(screen, fire_color, (x, y, compartment_width, floor_height))
    clicked_compartments.append((compartment, floor))


# A function that takes in the stickman_start_floor and stickman_start_compartment and then redraws the stickman to the next adjacent compartment or floor which is closer to the main door, the stickman is redrawn again and again till it reaches the main door and then pauses

def move_stickman(compartment, floor, main_door_compartment, main_door_floor):
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.display.quit()
                pygame.quit()
                return 
        if floor < main_door_floor and compartment < main_door_compartment:
            floor += 1
            compartment += 1
            draw_stickman(compartment, floor)
            pygame.display.update()
            pygame.time.delay(10)
        elif floor < main_door_floor and compartment == main_door_compartment:
            floor += 1
            draw_stickman(compartment, floor)
            pygame.display.update()
            pygame.time.delay(10)
        elif floor == main_door_floor and compartment < main_door_compartment:
            compartment += 1
            draw_stickman(compartment, floor)
            pygame.display.update()
            pygame.time.delay(10)
        elif floor == main_door_floor and compartment == main_door_compartment:
            # # Background Color
            # screen.fill(color_BROWN)
            # # Draw the building
            # draw_building(number_of_floors)
            # # Draw the door in defined floor and compartment
            # draw_main_door(main_door_compartment, main_door_floor)  
            break

# A function that takes in number of compartments per floor 
# as the max x axis, number of floors as the max y axis and 
# takes in the compartments that are already clicked as the obstacles
# then returns the shortest path to the main door. The path is returned as an array of coordinates
# traveling through adjacent compartments and floors. The stickman can only travel through the first 
# and last compartment of each floor. On the same floor, the stickamn can tracel through any adjacent compartment.
# This array of coordinates is then used to draw the stickman by the 
# move_stickman_with_algorithm function.

def shortest_path_algorithm(number_of_compartments_per_floor, number_of_floors, clicked_compartments):
    # Create a 2D grid representing the compartments
    grid = [[0 for x in range(number_of_compartments_per_floor)] for y in range(number_of_floors)]
    for x, y in clicked_compartments:
        grid[y][x] = 1
    # Define the start and end point
    start = (stickman_start_compartment, stickman_start_floor)
    end = (main_door_compartment, main_door_floor)

    # Create a priority queue
    heap = [(0, start)]
    visited = set()
    while heap:
        (cost, current) = heapq.heappop(heap)
        if current in visited:
            continue
        visited.add(current)
        if current == end:
            print("visited path=", visited)
            break
        # Check all the adjacent compartments
        for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            x, y = current
            if dy != 0 and (x != 0 and x != number_of_compartments_per_floor-1):
                continue
            if x + dx < 0 or x + dx >= number_of_compartments_per_floor or y + dy < 0 or y + dy >= number_of_floors:
                continue
            if grid[y + dy][x + dx] == 1:
                continue
            heapq.heappush(heap, (cost + 1, (x + dx, y + dy)))

    # Reconstruct the path
    path = []
    while current != start:
        if current in path:
            print("No valid path found.")
            break
        path.append(current)
        for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            x, y = current
            if dx == 0 and (x != 0 and x != number_of_compartments_per_floor - 1):
                continue
            if (x + dx, y + dy) in visited:
                current = (x + dx, y + dy)
                break
        else:
            print("No valid next step found.")
            break



    # Reverse the path
    print(path)
    path.reverse()
    return path


def move_stickman_with_algorithm(path):
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.display.quit()
                pygame.quit()
                return 
        for i in range(len(path)):
            x, y = path[i]
            draw_stickman(x, y)
            pygame.display.update()
            pygame.time.wait(100) # Wait for 100ms before moving to the next compartment
        break

# Function that detects the mouse click and then draws a red rectangle on the compartment that is clicked
def mouse_click_detection():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.display.quit()
                pygame.quit()
                sys.exit()

        mouse_pressed = pygame.mouse.get_pressed()
        if mouse_pressed[0] == 1:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            for i in range(number_of_compartments_per_floor):
                for j in range(number_of_floors):
                    x, y = compartments[i][j]
                    # Do not draw if the compartment is already clicked
                    if (i, j) in clicked_compartments:
                        continue
                    if x < mouse_x < x + compartment_width and y < mouse_y < y + floor_height:
                        mouse_pressed[0] == 1
                        draw_compartment_rectangle_fill(i, j)
                        pygame.display.update()
                        print("red draw triggered")

# Thread to detect mouse click
mouse_thread = threading.Thread(target=mouse_click_detection)
mouse_thread.daemon = True
mouse_thread.start()



# Function to handle reset button event
def reset():
    draw_building(number_of_floors)
    draw_main_door(main_door_compartment, main_door_floor)
    draw_stickman(stickman_start_compartment, stickman_start_floor)
    clicked_compartments.clear()

# Function to handle reset button event
def reset_and_start_handling():
    while True:

        mouse_pressed = pygame.mouse.get_pressed()
        if mouse_pressed[0] == 1:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if reset_button_rect.collidepoint(mouse_x, mouse_y):
                reset()    
                print("reset triggered")
                pygame.time.delay(100)
                
            elif start_button_rect.collidepoint(mouse_x, mouse_y):
                print("start triggered")
                # move_stickman(stickman_start_compartment, stickman_start_floor, main_door_compartment, main_door_floor)
                path = shortest_path_algorithm(number_of_compartments_per_floor, number_of_floors, clicked_compartments)
                move_stickman_with_algorithm(path)
                pygame.time.delay(100)

# Thread for Reset Handling 
reset_thread = threading.Thread(target=reset_and_start_handling)
reset_thread.daemon = True
reset_thread.start()

# Main drawings should come outside the forever loop

# Background Color
screen.fill(background_color)
# Draw the building
draw_building(number_of_floors)
# Draw the door in defined floor and compartment
draw_main_door(main_door_compartment, main_door_floor)    

# Draw a reset button on the bottom left of the screen and when clicked, the building is drawn again and the stickman is redrawn to the start position
reset_button_rect = pygame.draw.rect(screen, color_RED, (0, vert_screen_size - 50, 100, 50))
font = pygame.font.Font('freesansbold.ttf', 32)
text = font.render("Reset", True, reset_button_text_color, reset_button_color)
textRect = text.get_rect()
textRect.center = (50, vert_screen_size - 25)
screen.blit(text, textRect)

# Draw a start button on the bottom right of the screen (above reset button) and when clicked, the stickman starts moving towards the main door
start_button_rect = pygame.draw.rect(screen, start_button_color, (0, vert_screen_size - 100, 100, 50))
font = pygame.font.Font('freesansbold.ttf', 32)
text = font.render("Start", True, start_button_text_color, start_button_color)
textRect = text.get_rect()
textRect.center = (50, vert_screen_size - 75)
screen.blit(text, textRect)


# Main game loop #

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    #Draw Stickman
    draw_stickman(stickman_start_compartment, stickman_start_floor)

    # Draw compartment rectangles
    draw_compartment_rectangle()
    

    #Prints the total number of clicked compartments in the bottom right of the screen
    font = pygame.font.Font('freesansbold.ttf', 32)
    text = font.render(str(len(clicked_compartments)), True, clicked_compartment_counter_color, clicked_compartment_counter_box_color)
    textRect = text.get_rect()
    textRect.center = (vert_screen_size - 25, vert_screen_size - 25)
    screen.blit(text, textRect)   



    # # Move stickman, keep rerunning function when stickman reaches the main door
    # move_stickman(stickman_start_compartment, stickman_start_floor, main_door_floor, main_door_compartment)

    # Update the screen
    pygame.display.update()

# Quit pygame
pygame.display.quit()
pygame.quit()
