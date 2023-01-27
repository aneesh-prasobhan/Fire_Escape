import pygame

# Initialize pygame
pygame.init()

# Global variables
screen = pygame.display.set_mode((850, 550))
floors = [100, 100, 100, 100, 100]
colors = [(255,255,255), (128,128,128), (255,255,255), (128,128,128), (255,255,255)]

#Stickman Constants
radius = 12.5
body_length = 40
arm_length = 25
leg_length = 25
width = 5

stickman_coord_x = 425
stickman_coord_y = 425

def draw_building():
    y_coord = 25    #Starting point for drawing the floor at the top of the screen
    for i in range(5):
        pygame.draw.rect(screen, colors[i], (25, y_coord, 800, floors[i]))
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

def draw_stickman(x, y):
    pygame.draw.circle(screen, (0, 0, 0), (x, y), radius)
    pygame.draw.line(screen, (0, 0, 0), (x, y), (x, y + body_length), width)
    pygame.draw.line(screen, (0, 0, 0), (x, y + body_length/2), (x-arm_length, y + body_length/2), width)
    pygame.draw.line(screen, (0, 0, 0), (x, y + body_length/2), (x+arm_length, y + body_length/2), width)
    pygame.draw.line(screen, (0, 0, 0), (x, y + body_length), (x-leg_length, y + body_length + leg_length), width)
    pygame.draw.line(screen, (0, 0, 0), (x, y + body_length), (x+leg_length, y + body_length + leg_length), width)


# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Background Color
    screen.fill((205, 127, 50))

    # Draw the building
    y_coord = draw_building()

    # Draw the door 
    draw_door(y_coord)
    
    #Draw Stickman
    draw_stickman(stickman_coord_x, stickman_coord_y)
    # Update the screen
    pygame.display.update()

# Quit pygame
pygame.quit()
