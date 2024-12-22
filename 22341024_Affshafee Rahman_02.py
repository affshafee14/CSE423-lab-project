import random
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import math

# Define the window size
WINDOW_WIDTH, WINDOW_HEIGHT = 500, 500

# Global variables for plane position
x_position = 250  
y_position = 30     
scale = 0.5       # Scaling factor for the plane

#Bullets properties
bullets = []  # List to store active bullets as (x, y) tuples
bullet_radius = 2  # Size of the bullet
bullet_speed = 1  # Speed of the bullet

# Falling obstacle properties
obstacles = []  # List to store active obstacles (x, y)
obstacle_radius = 20  # obstacle radius
fall_speed = 0.2  # Speed of obstacles 
spawn_interval = 300  # Interval between each obstacles (in frames)
frame_count = 0  

# Global variable for score
score = 0  

# Global variables for missed obstacles
missed_obstacles = 0  # Counter for obstacles that fall without getting hit


# Bonus Circle Properties
bonus_circle = None  # (x, y, initial_radius, time_offset)
bonus_base_radius = 15  # Base size for the bonus circle
bonus_amplitude = 10  # Amplitude of size oscillation
bonus_speed = fall_speed * 1.2  # Bonus circle falls slightly faster
bonus_points = 20  # Points for hitting the bonus circle 


# Midpoint Line Drawing Algorithm (Zone 0)
def midpoint_line(x0, y0, x1, y1):
    points = []
    dx = x1 - x0
    dy = y1 - y0

    p = 2 * dy - dx
    x, y = x0, y0

    while x <= x1:
        points.append((x, y))
        x += 1
        if p < 0:
            p += 2 * dy
        else:
            y += 1
            p += 2 * dy - 2 * dx

    return points

# Zone Conversion
def zone_conversion(x0, y0, x1, y1):
    dx, dy = x1 - x0, y1 - y0

    if abs(dx) >= abs(dy):  # dx dominates
        if dx > 0 and dy >= 0: return (x0, y0, x1, y1, 0)
        if dx < 0 <= dy: return (-x0, y0, -x1, y1, 3)
        if dx < 0 and dy < 0: return (-x0, -y0, -x1, -y1, 4)
        if dx > 0 > dy: return (x0, -y0, x1, -y1, 7)
    else:  # dy dominates
        if dy > 0 and dx >= 0: return (y0, x0, y1, x1, 1)
        if dy > 0 > dx: return (y0, -x0, y1, -x1, 2)
        if dy < 0 and dx < 0: return (-y0, -x0, -y1, -x1, 5)
        if dy < 0 <= dx: return (-y0, x0, -y1, x1, 6)

# Reverse Zone Conversion
def reverse_zone_conversion(x, y, zone):
    if zone == 0: return x, y
    if zone == 1: return y, x
    if zone == 2: return -y, x
    if zone == 3: return -x, y
    if zone == 4: return -x, -y
    if zone == 5: return -y, -x
    if zone == 6: return y, -x
    if zone == 7: return x, -y

# Draw a Line
def draw_line(x0, y0, x1, y1):
    converted = zone_conversion(x0, y0, x1, y1)
    x0, y0, x1, y1, zone = converted
    points = midpoint_line(x0, y0, x1, y1)
    final_points = [reverse_zone_conversion(x, y, zone) for x, y in points]

    glBegin(GL_POINTS)
    for x, y in final_points:
        glVertex2f(x, y)
    glEnd()


# Midpoint Circle Drawing Algorithm
def plot_symmetric_points(xc, yc, x, y):
    glVertex2f(xc + x, yc + y)
    glVertex2f(xc - x, yc + y)
    glVertex2f(xc + x, yc - y)
    glVertex2f(xc - x, yc - y)
    glVertex2f(xc + y, yc + x)
    glVertex2f(xc - y, yc + x)
    glVertex2f(xc + y, yc - x)
    glVertex2f(xc - y, yc - x)

def midpoint_circle(xc, yc, r):
    x = 0
    y = r
    p = 1 - r

    glBegin(GL_POINTS)
    plot_symmetric_points(xc, yc, x, y)

    while x < y:
        x += 1
        if p < 0:
            p += 2 * x + 1
        else:
            y -= 1
            p += 2 * x - 2 * y + 1

        plot_symmetric_points(xc, yc, x, y)
    glEnd()

draw_circle = lambda x, y, r: midpoint_circle(x, y, r)

# Draw the Plane
def draw_plane(x, y, scale):
    """Draws a taller and thinner plane centered around (x, y) with uniform scaling."""
    # Triangle (Top Tip)
    draw_line(x, y + 180 * scale, x - 30 * scale, y + 120 * scale)
    draw_line(x, y + 180 * scale, x + 30 * scale, y + 120 * scale)
    draw_line(x - 30 * scale, y + 120 * scale, x + 30 * scale, y + 120 * scale)

    # Rectangle (Body)
    draw_line(x - 30 * scale, y + 120 * scale, x - 30 * scale, y - 20 * scale)
    draw_line(x + 30 * scale, y + 120 * scale, x + 30 * scale, y - 20 * scale)
    draw_line(x - 30 * scale, y - 20 * scale, x + 30 * scale, y - 20 * scale)

    # Wings
    draw_line(x - 30 * scale, y + 50 * scale, x - 80 * scale, y - 20 * scale)
    draw_line(x + 30 * scale, y + 50 * scale, x + 80 * scale, y - 20 * scale)

    # Horizontal lines
    draw_line(x - 30 * scale, y - 20 * scale, x - 80 * scale, y - 20 * scale)
    draw_line(x + 30 * scale, y - 20 * scale, x + 80 * scale, y - 20 * scale)
    # Flames (Rectangular and shorter, vertical flames)
    flame_height = 30 * scale  # Shorter flames
    flame_width = 7 * scale   # Width of the rectangular flames

    # Left flame (rectangular)
    # Draw a rectangle: left and right sides + top and bottom
    draw_line(x - 15 * scale - flame_width / 2, y - 20 * scale, x - 15 * scale - flame_width / 2, y - 20 * scale - flame_height)  # Left vertical side
    draw_line(x - 15 * scale + flame_width / 2, y - 20 * scale, x - 15 * scale + flame_width / 2, y - 20 * scale - flame_height)  # Right vertical side
    draw_line(x - 15 * scale - flame_width / 2, y - 20 * scale - flame_height, x - 15 * scale + flame_width / 2, y - 20 * scale - flame_height)  # Bottom side
    draw_line(x - 15 * scale - flame_width / 2, y - 20 * scale, x - 15 * scale + flame_width / 2, y - 20 * scale)  # Top side

    # Center flame (rectangular)
    # Draw a rectangle: left and right sides + top and bottom
    draw_line(x - flame_width / 2, y - 20 * scale, x - flame_width / 2, y - 20 * scale - flame_height)  # Left vertical side
    draw_line(x + flame_width / 2, y - 20 * scale, x + flame_width / 2, y - 20 * scale - flame_height)  # Right vertical side
    draw_line(x - flame_width / 2, y - 20 * scale - flame_height, x + flame_width / 2, y - 20 * scale - flame_height)  # Bottom side
    draw_line(x - flame_width / 2, y - 20 * scale, x + flame_width / 2, y - 20 * scale)  # Top side

    # Right flame (rectangular)
    # Draw a rectangle: left and right sides + top and bottom
    draw_line(x + 15 * scale - flame_width / 2, y - 20 * scale, x + 15 * scale - flame_width / 2, y - 20 * scale - flame_height)  # Left vertical side
    draw_line(x + 15 * scale + flame_width / 2, y - 20 * scale, x + 15 * scale + flame_width / 2, y - 20 * scale - flame_height)  # Right vertical side
    draw_line(x + 15 * scale - flame_width / 2, y - 20 * scale - flame_height, x + 15 * scale + flame_width / 2, y - 20 * scale - flame_height)  # Bottom side
    draw_line(x + 15 * scale - flame_width / 2, y - 20 * scale, x + 15 * scale + flame_width / 2, y - 20 * scale)  # Top side


# Animate Bullet
def animate_bullets():
    global bullets

    glColor3f(1.0, 1.0, 1.0)  # White bullets
    updated_bullets = []

    for x, y in bullets:
        if y < WINDOW_HEIGHT:  # If the bullet is still on screen
            draw_circle(x, y, bullet_radius)
            updated_bullets.append((x, y + bullet_speed))  # Move bullet upward

    bullets = updated_bullets


# obstacles falling down...
def animate_obstacles():
    global obstacles, bullets, score, missed_obstacles

    glColor3f(1.0, 1.0, 0.93)  # Light yellow obstacles
    updated_obstacles = []
    updated_bullets = bullets.copy()  # Copy the bullets list to safely modify during iteration

    for obstacle_x, obstacle_y in obstacles:
        if obstacle_y > -obstacle_radius:  # If the obstacle is still on screen
            collision_detected = False

            # Check for collision with bullets
            for bullet_x, bullet_y in bullets:
                # distance between the bullet and the obstacle
                distance = math.sqrt((bullet_x - obstacle_x)**2 + (bullet_y - obstacle_y)**2)
                if distance <= bullet_radius + obstacle_radius:
                    collision_detected = True
                    score += 1  # Increment the score
                    print(f"Score: {score}")  # Display the score in the console
                    updated_bullets.remove((bullet_x, bullet_y))
                    break  # Stop checking other bullets for this obstacle

            # Potential collision with the rocket
            rocket_radius = 50 * scale  # Approximate hitbox radius for the rocket
            rocket_center_x = x_position
            rocket_center_y = y_position + 90 * scale  # Center of the rocket
            distance_to_rocket = math.sqrt((obstacle_x - rocket_center_x)**2 + (obstacle_y - rocket_center_y)**2)

            if distance_to_rocket <= rocket_radius + obstacle_radius:
                print("Collision with rocket! Game Over.")
                glutLeaveMainLoop()
                return  # Stop further processing

            if not collision_detected:
                # Draw obstacle and move it down
                draw_circle(obstacle_x, obstacle_y, obstacle_radius)
                updated_obstacles.append((obstacle_x, obstacle_y - fall_speed))
        else:
            # If the obstacle has fallen past the bottom of the screen
            missed_obstacles += 1
            print(f"Missed Obstacles: {missed_obstacles}")  # Display missed obstacles in the console
            if missed_obstacles > 3:  # Quit if more than 3 obstacles are missed
                print("Game Over! Too many missed obstacles.")
                glutLeaveMainLoop()
                return  # Stop further processing

    # Update global lists
    obstacles = updated_obstacles
    bullets = updated_bullets

def animate_bonus_circle():
    global bonus_circle, bullets, score

    if bonus_circle is not None:
        x, y, initial_radius, time_offset = bonus_circle

        # Calculate the oscillating radius using a sinusoidal function
        t = frame_count + time_offset
        radius = initial_radius + bonus_amplitude * math.sin(t * 0.01)

        # Check for collision with bullets
        collision_detected = False
        for bullet_x, bullet_y in bullets:
            distance = math.sqrt((bullet_x - x)**2 + (bullet_y - y)**2)
            if distance <= bullet_radius + radius:
                collision_detected = True
                score += bonus_points
                print(f"Bonus Hit! Score: {score}")
                bullets.remove((bullet_x, bullet_y))
                bonus_circle = None  # Remove the bonus circle
                break

        # Check if the bonus circle is still visible
        if y > -bonus_base_radius and not collision_detected:
            # Draw and move the bonus circle
            glColor3f(0.0, 1.0, 0.0)  # Green for the bonus circle
            draw_circle(x, y, radius  )
            bonus_circle = (x, y - bonus_speed, initial_radius, time_offset)
        elif not collision_detected:
            # Remove bonus circle if it leaves the screen
            bonus_circle = None



def display():
    global frame_count

    glClear(GL_COLOR_BUFFER_BIT)  # Clear the screen
    glPointSize(2.0)

    # Draw the rocket
    glColor3f(1.0, 1.0, 0.0)  # Yellow rocket
    draw_plane(x_position, y_position, scale)

    # Animate bullets
    animate_bullets()

    # Animate obstacles and handle collisions
    animate_obstacles()

    # Animate the bonus circle
    animate_bonus_circle()

    # Spawn new obstacles at intervals
    frame_count += 1
    if frame_count % spawn_interval == 0:
        spawn_new_obstacle()
    '''above function is used to speed up 
    or slow down the rate of obstacle generation'''

    # Occasionally spawn a bonus circle
    if frame_count % (spawn_interval * 5) == 0 and bonus_circle is None:
        spawn_bonus_circle()

    glFlush()  
    glutPostRedisplay()  


# introduces an obstacle randomly
def spawn_new_obstacle():
    global obstacles
    new_x = random.randint(0, WINDOW_WIDTH)  # Random horizontal position
    obstacles.append((new_x, WINDOW_HEIGHT + obstacle_radius))  

def spawn_bonus_circle():
    global bonus_circle
    new_x = random.randint(0, WINDOW_WIDTH)  # Random horizontal position
    initial_radius = bonus_base_radius  
    time_offset = random.randint(0, 100)  # Randomize the oscillation phase
    bonus_circle = (new_x, WINDOW_HEIGHT + bonus_base_radius, initial_radius, time_offset)



# Spacebar Key Function (shoot bullet)
def button_click(key, x, y):
    global bullets

    if key == b" ":  # Spacebar key
        # Adds a new bullet at the current plane position
        bullets.append((x_position, y_position + 180 * scale))

    glutPostRedisplay() 


# Arrow Key Function
def arrow_click(key, x, y):
    global x_position

    if key == GLUT_KEY_RIGHT:  
        x_position += 20
    elif key == GLUT_KEY_LEFT:  
        x_position -= 20 

    glutPostRedisplay()  



# Initialize OpenGL
def init():
    glClearColor(0.0, 0.0, 0.0, 1.0)  # Black background
    gluOrtho2D(0, WINDOW_WIDTH, 0, WINDOW_HEIGHT)  

# Main Function
glutInit()
glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB)
glutInitWindowSize(WINDOW_WIDTH, WINDOW_HEIGHT)

screen_width = glutGet(GLUT_SCREEN_WIDTH)
screen_height = glutGet(GLUT_SCREEN_HEIGHT)
glutInitWindowPosition((screen_width - WINDOW_WIDTH) // 2, (screen_height - WINDOW_HEIGHT) // 2)

glutCreateWindow(b"CSE423 lab assignment #2" ) 
init()
glutDisplayFunc(display)
glutSpecialFunc(arrow_click)
glutKeyboardFunc(button_click)
glutMainLoop()