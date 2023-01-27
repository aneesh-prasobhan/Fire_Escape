import pygame

# Initialize pygame
pygame.init()

# Set the screen size
screen = pygame.display.set_mode((850, 550))

# Create a list of floor heights
floors = [100, 100, 100, 100, 100]

# Create a list of floor colors
colors = [(255,255,255), (128,128,128), (255,255,255), (128,128,128), (255,255,255)]

# Initialize the index variable
i = 0



# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Background Color
    screen.fill((205, 127, 50))

    # Draw the building
    y_coord = 25    #Starting point for drawing the floor at the top of the screen
    for i in range(5):
        pygame.draw.rect(screen, colors[i], (25, y_coord, 800, floors[i]))
        y_coord +=floors[i]

    # Draw the door 

    for i in range(5):
        
        if i == 4:
            door_width = 50
            door_height = 75
            door_x = (850 - door_width) // 2
            door_y = y_coord - floors[i] + (100 - door_height) // 2
            pygame.draw.rect(screen, (139, 69, 19), (door_x, door_y, door_width, door_height))


    # Update the screen
    pygame.display.update()

# Quit pygame
pygame.quit()
