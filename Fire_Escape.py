import pygame

# Initialize pygame
pygame.init()

# Global variables

#Screen Size
horiz_screen_size = 850
vert_screen_size = 550

screen = pygame.display.set_mode((horiz_screen_size, vert_screen_size))

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
        colors.append((255,255,255))
    else:
        colors.append((128,128,128))


# Compartment size
number_of_compartments_per_floor = 20
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
body_length = 40
arm_length = 18
leg_length = 18
width = 6

stickman_floor = 0
stickman_compartment = 0        # Should be under "number_of_compartments_per_floor - 1"


def draw_building(number_of_floors):
    y_coord = 25    #Starting point for drawing the floor at the top of the screen
    for i in range(number_of_floors):
        pygame.draw.rect(screen, colors[i], (25, y_coord, building_width, floors[i]))
        y_coord +=floors[i]
    return y_coord

def draw_door(y_coord):
    
    for i in range(5):
        if i == 4:
            door_width = 50
            door_height = 75
            door_x = (850 - door_width) // 2
            door_y = y_coord - floors[i] + (100 - door_height) // 2
            pygame.draw.rect(screen, (139, 69, 19), (door_x, door_y, door_width, door_height))


def get_compartment_coordinates(floor, compartment):
    x, y = compartments[floor][compartment]
    return (x, y)


# Draw stickman function
def draw_stickman(floor, compartment):
    x, y = get_compartment_coordinates(floor, compartment)
    # Draw the stickman using the x and y coordinates
    pygame.draw.circle(screen, (0, 0, 0), (x + compartment_width/2, y + compartment_width/2), radius)
    pygame.draw.line(screen, (0, 0, 0), (x + compartment_width/2, y + compartment_width/2), (x + compartment_width/2, y + compartment_width/2 + body_length), width)
    pygame.draw.line(screen, (0, 0, 0), (x + compartment_width/2, y + compartment_width/2 + body_length/2), (x + compartment_width/2-arm_length, y + compartment_width/2 + body_length/2), width)
    pygame.draw.line(screen, (0, 0, 0), (x + compartment_width/2, y + compartment_width/2 + body_length/2), (x + compartment_width/2+arm_length, y + compartment_width/2 + body_length/2), width)
    pygame.draw.line(screen, (0, 0, 0), (x + compartment_width/2, y + compartment_width/2 + body_length), (x + compartment_width/2-leg_length, y + compartment_width/2 + body_length + leg_length), width)
    pygame.draw.line(screen, (0, 0, 0), (x + compartment_width/2, y + compartment_width/2 + body_length), (x + compartment_width/2+leg_length, y + compartment_width/2 + body_length + leg_length), width)
    
    


# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Background Color
    screen.fill((205, 127, 50))

    # Draw the building
    y_coord = draw_building(number_of_floors)

    # Draw the door 
    draw_door(y_coord)
    
    #Draw Stickman
    draw_stickman(stickman_floor, stickman_compartment)
    # Update the screen
    pygame.display.update()

# Quit pygame
pygame.quit()
