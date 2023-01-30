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

stickman_placing_MODE = True

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

def draw_sign(screen, x, y, width, height, direction):
    # Draw the black border of the sign board
    pygame.draw.rect(screen, (0, 0, 0), (x, y, width, height), 1)
    # Draw the white fill inside the sign board
    pygame.draw.rect(screen, (255, 255, 255), (x + 1, y + 1, width - 2, height - 2))

    # Calculate the coordinates of the center of the sign board
    center_x = x + width // 2
    center_y = y + height // 2

    # Draw the red arrow based on the direction argument
    if direction == "up":
        pygame.draw.polygon(screen, (255, 0, 0), [(center_x, y + 1), (center_x + width // 4, center_y), (center_x - width // 4, center_y)])
    elif direction == "down":
        pygame.draw.polygon(screen, (255, 0, 0), [(center_x, y + height - 1), (center_x + width // 4, center_y), (center_x - width // 4, center_y)])
    elif direction == "left":
        pygame.draw.polygon(screen, (255, 0, 0), [(x + 1, center_y), (center_x, center_y + height // 4), (center_x, center_y - height // 4)])
    elif direction == "right":
        pygame.draw.polygon(screen, (255, 0, 0), [(x + width - 1, center_y), (center_x, center_y + height // 4), (center_x, center_y - height // 4)])
    print("drawing sign")
    # pygame.display.update()
    
def draw_default_signs_on_floors(screen, compartments, number_of_compartments_per_floor, floor_height, compartment_width, main_door_floor, main_door_compartment):
    sign_list = []
    for i in range(len(compartments)):
        floor_compartments = compartments[i]
        for j in range(len(floor_compartments)):
            x, y = floor_compartments[j]
            compartment_number = x // compartment_width
            # Skip the main door compartment
            if i == main_door_compartment and j == main_door_floor:
                continue
            if j == main_door_floor:
            # Draw signs towards main door
                # Draw signs on even compartments of even-numbered floors
                if (i % 2 == 0 and j % 2 == 0):
                    print("default (x,y)=", x,y)
                    draw_sign(screen, x + compartment_width // 4, y + floor_height // 4, compartment_width // 2, floor_height // 2, "left" if main_door_compartment < i else "right")
                    sign_list.append((int(compartment_number), j))
                # Draw signs on odd compartments of odd-numbered floors
                elif (i % 2 != 0 and j % 2 != 0):
                    print("default (x,y)=", x,y)
                    draw_sign(screen, x + compartment_width // 4, y + floor_height // 4, compartment_width // 2, floor_height // 2, "left" if main_door_compartment < i else "right")                
                    sign_list.append((int(compartment_number), j))
            else:
            # Draw signs on odd compartments of odd-numbered floors
                if i % 2 != 0 and j % 2 != 0:
                # Draw signs in direction of closest first or last compartment
                    if compartment_number < number_of_compartments_per_floor // 2:
                        print("default (x,y)=", x,y)
                        draw_sign(screen, x + compartment_width // 4, y + floor_height // 4, compartment_width // 2, floor_height // 2, "left")
                        sign_list.append((int(compartment_number), j))
                    else:
                        print("default (x,y)=", x,y)
                        draw_sign(screen, x + compartment_width // 4, y + floor_height // 4, compartment_width // 2, floor_height // 2, "right")
                        sign_list.append((int(compartment_number), j))
                        
                # Draw signs on even compartments of even-numbered floors
                elif (i % 2 == 0 and j % 2 == 0):
                    # Draw signs in direction of closest first or last compartment
                    if compartment_number < number_of_compartments_per_floor // 2:
                        print("default (x,y)=", x,y)
                        draw_sign(screen, x + compartment_width // 4, y + floor_height // 4, compartment_width // 2, floor_height // 2, "left")
                        sign_list.append((int(compartment_number), j))
                    else:
                        print("default (x,y)=", x,y)
                        draw_sign(screen, x + compartment_width // 4, y + floor_height // 4, compartment_width // 2, floor_height // 2, "right")
                        sign_list.append((int(compartment_number), j))
    return sign_list
             

# Now I have a list of compartments  where the signs are present. What I want to do now is I want to have a new  function which runs the bfs algorithm on each compartment inside the sign_list and find the shortest part to the main door. After finding the path, I want to re display the signs so that it shows the arrow in the direction of the next compartment in the shortest path result from the bfs algorithm. In the new function, use the bfs function which takes in clicked_compartments, start and end (start here is the current compartment in the sign_list, end is the compartment of the main door). 
def run_bfs_on_signs(screen, sign_list, clicked_compartments, main_door_compartment, main_door_floor):
    for start in sign_list:
        end = (main_door_compartment, main_door_floor)
        sign_path = bfs(clicked_compartments, start, end)
        if sign_path is None:
            continue
        # Clip path so that it only has the first two positions
        sign_path = sign_path[1:2]
        # Current Sign 
        print("current sign =", start)
        print("next path =", sign_path)
        if sign_path:
            current_sign = start
            next_path = sign_path[0]
            print("calling redraw function")
            redraw_signs(screen, current_sign, next_path)
            # break


def redraw_signs(screen, current_sign, next_path):

    x_position, y_position = current_sign 
    x,y = get_compartment_coordinates(x_position, y_position)
    
    next_x_position, next_y_position = next_path
    next_x, next_y = get_compartment_coordinates(next_x_position, next_y_position)
    
    print("got coordinates")
    # If next x is greater and next y is same as current y, then draw sign to the right
    if next_x > x and next_y == y:
        print("(x,y)=", x,y)
        draw_sign(screen, x + compartment_width // 4, y + floor_height // 4, compartment_width // 2, floor_height // 2, "right")
    elif next_x < x and next_y == y:
        print("(x,y)=", x,y)
        draw_sign(screen, x + compartment_width // 4, y + floor_height // 4, compartment_width // 2, floor_height // 2, "left")
    elif next_y > y and next_x == x:
        print("(x,y)=", x,y)
        draw_sign(screen, x + compartment_width // 4, y + floor_height // 4, compartment_width // 2, floor_height // 2, "down")
    elif next_y < y and next_x == x:
        print("(x,y)=", x,y)
        draw_sign(screen, x + compartment_width // 4, y + floor_height // 4, compartment_width // 2, floor_height // 2, "up")


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

def bfs(clicked_compartments, start, end):
    # Create a queue and a dictionary to keep track of the compartments
    queue = [start]
    parent = {start: None}

    # Create a 2D grid representing the compartments
    grid = [[0 for x in range(number_of_compartments_per_floor)] for y in range(number_of_floors)]
    for x, y in clicked_compartments:
        grid[y][x] = 1

    # Perform the BFS algorithm
    while queue:
        current = queue.pop(0)
        if current == end:
            return reconstruct_path(parent, end)
        x, y = current
        # Check if current node is the first or last compartment in the current floor
        if x != 0 and x != number_of_compartments_per_floor-1:
            for dx, dy in [(1, 0), (-1, 0)]:
                if x + dx < 0 or x + dx >= number_of_compartments_per_floor or y + dy < 0 or y + dy >= number_of_floors:
                    continue
                if grid[y + dy][x + dx] == 1:
                    continue
                if (x + dx, y + dy) in parent:
                    continue
                parent[(x + dx, y + dy)] = current
                queue.append((x + dx, y + dy))
        else:
            for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                if x + dx < 0 or x + dx >= number_of_compartments_per_floor or y + dy < 0 or y + dy >= number_of_floors:
                    continue
                if grid[y + dy][x + dx] == 1:
                    continue
                if (x + dx, y + dy) in parent:
                    continue
                parent[(x + dx, y + dy)] = current
                queue.append((x + dx, y + dy))
    return None



def reconstruct_path(parent, current):
    path = [current]
    while current in parent and parent[current] is not None:
        current = parent[current]
        path.append(current)
    path.reverse()
    return path


def move_stickman_with_algorithm(path):
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.display.quit()
                pygame.quit()
                return 
            
        if path is not None:
            for i in range(len(path)):
                x, y = path[i]
                draw_stickman(x, y)
                pygame.display.update()
                pygame.time.wait(100) # Wait for 100ms before moving to the next compartment
            break
        else:
            font = pygame.font.Font(None, 36)
            print("no path found")
            text = font.render("No Path Found", 1, (255, 255, 255))
            screen.blit(text, (screen.get_width()//2 - text.get_width()//2, screen.get_height() - text.get_height()))
            pygame.display.update()                
            break

# Function that detects the mouse click and then draws a red rectangle on the compartment that is clicked
def mouse_click_detection(stickman_placing_MODE = 1):
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.display.quit()
                pygame.quit()
                sys.exit()

        mouse_pressed = pygame.mouse.get_pressed()
        if mouse_pressed[0] == 1:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            
            if stickman_placing_MODE == False:
                for i in range(number_of_compartments_per_floor):
                    for j in range(number_of_floors):
                        x, y = compartments[i][j]
                        # Do not draw if the compartment is already clicked
                        if (i, j) in clicked_compartments:
                            continue
                        if x < mouse_x < x + compartment_width and y < mouse_y < y + floor_height:
                            mouse_pressed[0] == 1
                            draw_compartment_rectangle_fill(i, j)
                            draw_number_of_clicked_compartments()
                            pygame.display.update()
                            print("red draw triggered")

            else:
                # Place stickman in the compartment that is clicked
                for i in range(number_of_compartments_per_floor):
                    for j in range(number_of_floors):
                        x, y = compartments[i][j]
                        if x < mouse_x < x + compartment_width and y < mouse_y < y + floor_height:
                            mouse_pressed[0] == 1
                            draw_stickman(i, j)
                            pygame.display.update()
                            print("stickman draw triggered")  
                            stickman_placing_MODE = False
                            # Change stickman start compartment and floor
                            stickman_start_compartment = i
                            stickman_start_floor = j

              
            
            
            if reset_button_rect.collidepoint(mouse_x, mouse_y):
                reset()    
                print("reset triggered")
                pygame.time.delay(100)
                
            elif start_button_rect.collidepoint(mouse_x, mouse_y):
                print("start triggered")
                # move_stickman(stickman_start_compartment, stickman_start_floor, main_door_compartment, main_door_floor)
                # path_for_stickman = shortest_path_algorithm(number_of_compartments_per_floor, number_of_floors, clicked_compartments)
                
                run_bfs_on_signs(screen, sign_list, clicked_compartments, main_door_compartment, main_door_floor)
                
                start = (stickman_start_compartment, stickman_start_floor)
                end = (main_door_compartment, main_door_floor)

                
                path_for_stickman = bfs(clicked_compartments, start, end)
                move_stickman_with_algorithm(path_for_stickman)
                pygame.time.delay(100)  # Debouncing

# Thread to detect mouse click
mouse_thread = threading.Thread(target=mouse_click_detection)
mouse_thread.daemon = True
mouse_thread.start()



# Function to handle reset button event
def reset():
    screen.fill(background_color)
    draw_buttons(screen, font, reset_button_color, reset_button_text_color, start_button_color, start_button_text_color, vert_screen_size)
    draw_building(number_of_floors)
    # Draw compartment rectangles
    draw_compartment_rectangle()
    draw_main_door(main_door_compartment, main_door_floor)
    draw_default_signs_on_floors(screen, compartments, number_of_compartments_per_floor, floor_height, compartment_width, main_door_floor, main_door_compartment)
    draw_stickman(stickman_start_compartment, stickman_start_floor)
    draw_number_of_clicked_compartments()

    clicked_compartments.clear()

# # Drawing Number of Clicked Compartments
def draw_number_of_clicked_compartments():
    #Prints the total number of clicked compartments in the bottom right of the screen
    font = pygame.font.Font('freesansbold.ttf', 32)
    text = font.render(str(len(clicked_compartments)), True, clicked_compartment_counter_color, clicked_compartment_counter_box_color)
    textRect = text.get_rect()
    textRect.center = (vert_screen_size - 25, vert_screen_size - 25)
    screen.blit(text, textRect)   


# Main drawings should come outside the forever loop

# Background Color
screen.fill(background_color)
# Draw the building
draw_building(number_of_floors)
# Draw the door in defined floor and compartment
draw_main_door(main_door_compartment, main_door_floor)   

# Draw a sign board with black border and white fill half the size of the compartment which has a Red arrow (with red fill) pointing to the nearest compartment which is either the first compartment or the last compartment in the floor.
# A sign board should be drawn in every odd number of compartments in the first floor and every even number of compartments in the seconds floor and so on.

sign_list = draw_default_signs_on_floors(screen, compartments, number_of_compartments_per_floor, floor_height, compartment_width, main_door_floor, main_door_compartment)
print(sign_list)


# Drawing in Global
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

def draw_buttons(screen, font, reset_button_color, reset_button_text_color, start_button_color, start_button_text_color, vert_screen_size):
    reset_button_rect = pygame.draw.rect(screen, color_RED, (0, vert_screen_size - 50, 100, 50))
    text = font.render("Reset", True, reset_button_text_color, reset_button_color)
    textRect = text.get_rect()
    textRect.center = (50, vert_screen_size - 25)
    screen.blit(text, textRect)
  
    start_button_rect = pygame.draw.rect(screen, start_button_color, (0, vert_screen_size - 100, 100, 50))
    text = font.render("Start", True, start_button_text_color, start_button_color)
    textRect = text.get_rect()
    textRect.center = (50, vert_screen_size - 75)
    screen.blit(text, textRect)


# Draw compartment rectangles for initializing
draw_compartment_rectangle()

#Draw Stickman
# draw_stickman(stickman_start_compartment, stickman_start_floor)

# Draw Clicked Compartments 
draw_number_of_clicked_compartments()


# Main game loop #

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False



    # Update the screen
    pygame.display.update()         # Needed for fast screen updates
    pygame.time.delay(10)       
# Quit pygame
pygame.display.quit()
pygame.quit()
