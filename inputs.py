# Global variables

#Screen Size
horiz_screen_size = 850
vert_screen_size = 650      # was 550 before

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

#Floors
number_of_floors = 5
floor_height = 100
building_width = 800

horiz_offset = 25
vert_offset = 25

# Compartment size
number_of_compartments_per_floor = 10

#Colors
color_BROWN = (205, 127, 50)
color_WHITE = (255, 255, 255)
color_ASFALT = (128, 128, 128)
color_BRONZE = (139, 69, 19)
color_RED = (255, 0, 0)
color_ORANGE = (255, 165, 0)
color_YELLOW = (255, 255, 0)
color_GREEN = (0, 255, 0)
color_LIGHT_GREY = (211, 211, 211)
color_BLACK = (0, 0, 0)

stairway_color = color_ASFALT
fire_color = color_RED
door_color = color_BRONZE
floor_color_1 = color_WHITE
floor_color_2 = color_LIGHT_GREY
background_color = color_BROWN
reset_button_color = color_RED
reset_button_text_color = color_WHITE
start_button_color = color_GREEN
start_button_text_color = color_WHITE
compartment_rectangle_color = color_RED
clicked_compartment_counter_color = color_WHITE
clicked_compartment_counter_box_color = color_BROWN

