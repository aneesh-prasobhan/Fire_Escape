import pygame
import pygame.locals as pl
import threading
import sys

from inputs import *

# Initialize pygame
pygame.init()

screen = pygame.display.set_mode((horiz_screen_size, vert_screen_size))

floors = []
colors = []

for i in range(number_of_floors):
    floors.append(floor_height)
    if i % 2 == 0:
        colors.append(color_WHITE)
    else:
        colors.append(color_ASFALT)

#Compartment Size
compartment_width = building_width/number_of_compartments_per_floor

# Compartments list
compartments = []
for i in range(number_of_floors):
    floor_compartments = []
    for j in range(number_of_compartments_per_floor):
        x_coord = horiz_offset + j * compartment_width
        y_coord = vert_offset + i * floor_height
        floor_compartments.append((x_coord, y_coord))
    compartments.append(floor_compartments)

#Stickman Constants
radius = 10
body_length = 20
arm_length = 18
leg_length = 18
width = 6

stickman_start_floor = 0      # 0 = top floor, 1 = floor below top floor, etc.
stickman_start_compartment = 0        # Should be under "number_of_compartments_per_floor - 1" and >=0

# Main Door Constants
main_door_floor = 4
main_door_compartment = 4

# Make a list of all clicked compartments from the mouse click detection function
clicked_compartments = [] 

def draw_building(number_of_floors):
    y_coord = vert_offset    #Starting point for drawing the floor at the top of the screen
    for i in range(number_of_floors):
        pygame.draw.rect(screen, colors[i], (25, y_coord, building_width, floors[i]))
        y_coord +=floors[i]

# Function that draws the main door which takes in the floor and compartment as parameters
def draw_main_door(floor, compartment):
    x, y = get_compartment_coordinates(floor, compartment)
    pygame.draw.rect(screen, color_BRONZE, (x, y, compartment_width, floor_height))

def get_compartment_coordinates(floor, compartment):
    x, y = compartments[floor][compartment]
    return (x, y)


# Draw stickman function
def draw_stickman(floor, compartment):
    x, y = get_compartment_coordinates(floor, compartment)

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
            x, y = compartments[i][j]
            pygame.draw.rect(screen, color_RED, (x, y, compartment_width, floor_height), 1)

# Draw a red rectangle with fill, takes in the floor and compartment as parameters. Every drawn compartment is then added to the clicked_compartments list
def draw_compartment_rectangle_fill(floor, compartment):
    x, y = get_compartment_coordinates(floor, compartment)
    pygame.draw.rect(screen, color_RED, (x, y, compartment_width, floor_height))
    clicked_compartments.append((floor, compartment))


# A function that takes in the stickman_start_floor and stickman_start_compartment and then redraws the stickman to the next adjacent compartment or floor which is closer to the main door, the stickman is redrawn again and again till it reaches the main door and then pauses

def move_stickman(floor, compartment, main_door_floor, main_door_compartment):
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return 
        if floor < main_door_floor and compartment < main_door_compartment:
            floor += 1
            compartment += 1
            draw_stickman(floor, compartment)
            pygame.display.update()
            pygame.time.delay(10)
        elif floor < main_door_floor and compartment == main_door_compartment:
            floor += 1
            draw_stickman(floor, compartment)
            pygame.display.update()
            pygame.time.delay(10)
        elif floor == main_door_floor and compartment < main_door_compartment:
            compartment += 1
            draw_stickman(floor, compartment)
            pygame.display.update()
            pygame.time.delay(10)
        elif floor == main_door_floor and compartment == main_door_compartment:
            # # Background Color
            # screen.fill(color_BROWN)
            # # Draw the building
            # draw_building(number_of_floors)
            # # Draw the door in defined floor and compartment
            # draw_main_door(main_door_floor, main_door_compartment)  
            break

# Function that detects the mouse click and then draws a red rectangle on the compartment that is clicked

def mouse_click_detection():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        mouse_pressed = pygame.mouse.get_pressed()
        if mouse_pressed[0] == 1:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            for i in range(number_of_floors):
                for j in range(number_of_compartments_per_floor):
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
    draw_main_door(main_door_floor, main_door_compartment)
    draw_stickman(stickman_start_floor, stickman_start_compartment)
    clicked_compartments.clear()

# Function to handle reset button event
def reset_and_start_handling():
    while True:

        mouse_pressed = pygame.mouse.get_pressed()
        if mouse_pressed[0] == 1:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if reset_button_rect.collidepoint(mouse_x, mouse_y):
                reset()    
            elif start_button_rect.collidepoint(mouse_x, mouse_y):
                move_stickman(stickman_start_floor, stickman_start_compartment, main_door_floor, main_door_compartment)

# Thread for Reset Handling 
reset_thread = threading.Thread(target=reset_and_start_handling)
reset_thread.daemon = True
reset_thread.start()

# Main drawings should come outside the forever loop

# Background Color
screen.fill(color_BROWN)
# Draw the building
draw_building(number_of_floors)
# Draw the door in defined floor and compartment
draw_main_door(main_door_floor, main_door_compartment)    

# Draw a reset button on the bottom left of the screen and when clicked, the building is drawn again and the stickman is redrawn to the start position
reset_button_rect = pygame.draw.rect(screen, color_RED, (0, vert_screen_size - 50, 100, 50))
font = pygame.font.Font('freesansbold.ttf', 32)
text = font.render("Reset", True, color_WHITE, color_RED)
textRect = text.get_rect()
textRect.center = (50, vert_screen_size - 25)
screen.blit(text, textRect)

# Draw a start button on the bottom right of the screen (above reset button) and when clicked, the stickman starts moving towards the main door
start_button_rect = pygame.draw.rect(screen, color_GREEN, (0, vert_screen_size - 100, 100, 50))
font = pygame.font.Font('freesansbold.ttf', 32)
text = font.render("Start", True, color_WHITE, color_GREEN)
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
    draw_stickman(stickman_start_floor, stickman_start_compartment)

    # Draw compartment rectangles
    draw_compartment_rectangle()
    

    #Prints the total number of clicked compartments in the bottom right of the screen
    font = pygame.font.Font('freesansbold.ttf', 32)
    text = font.render(str(len(clicked_compartments)), True, color_WHITE, color_BROWN)
    textRect = text.get_rect()
    textRect.center = (vert_screen_size - 25, vert_screen_size - 25)
    screen.blit(text, textRect)   



    # # Move stickman, keep rerunning function when stickman reaches the main door
    # move_stickman(stickman_start_floor, stickman_start_compartment, main_door_floor, main_door_compartment)

    # Update the screen
    pygame.display.update()

# Quit pygame
pygame.display.quit()
pygame.quit()
