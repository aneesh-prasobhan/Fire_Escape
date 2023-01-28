import pygame

# Initialize pygame
pygame.init()

# Global variables

#Screen Size
horiz_screen_size = 850
vert_screen_size = 550

screen = pygame.display.set_mode((horiz_screen_size, vert_screen_size))

#Colors
color_BROWN = (205, 127, 50)
color_WHITE = (255, 255, 255)
color_ASFALT = (128, 128, 128)
color_BRONZE = (139, 69, 19)
color_RED = (255, 0, 0)

#Floors
number_of_floors = 5
floor_height = 100
building_width = 800

horiz_offset = 25
vert_offset = 25

floors = []
colors = []

for i in range(number_of_floors):
    floors.append(floor_height)
    if i % 2 == 0:
        colors.append(color_WHITE)
    else:
        colors.append(color_ASFALT)


# Compartment size
number_of_compartments_per_floor = 10

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

def draw_building(number_of_floors):
    y_coord = 25    #Starting point for drawing the floor at the top of the screen
    for i in range(number_of_floors):
        pygame.draw.rect(screen, colors[i], (25, y_coord, building_width, floors[i]))
        y_coord +=floors[i]
    return y_coord

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
            pygame.time.delay(1000)
        elif floor < main_door_floor and compartment == main_door_compartment:
            floor += 1
            draw_stickman(floor, compartment)
            pygame.display.update()
            pygame.time.delay(1000)
        elif floor == main_door_floor and compartment < main_door_compartment:
            compartment += 1
            draw_stickman(floor, compartment)
            pygame.display.update()
            pygame.time.delay(1000)
        elif floor == main_door_floor and compartment == main_door_compartment:
            break


# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Background Color
    screen.fill(color_BROWN)

    # Draw the building
    y_coord = draw_building(number_of_floors)

    
    # Draw the door in defined floor and compartment
    draw_main_door(main_door_floor, main_door_compartment)    


    #Draw Stickman
    draw_stickman(stickman_start_floor, stickman_start_compartment)

    # Draw compartment rectangles
    draw_compartment_rectangle()

    # Move stickman, keep rerunning function when stickman reaches the main door
    move_stickman(stickman_start_floor, stickman_start_compartment, main_door_floor, main_door_compartment)
    

    # Update the screen
    pygame.display.update()


# Quit pygame
pygame.display.quit()
pygame.quit()
