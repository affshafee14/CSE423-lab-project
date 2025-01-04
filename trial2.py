from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from math import sin, cos, pi

# Constants
SCREEN_WIDTH = 900
SCREEN_HEIGHT = 600

CATCHER_WIDTH = 150 #the width and height of the catcher
CATCHER_HEIGHT = 30
WHITE = (1.0, 1.0, 1.0)
catcher_color = WHITE
catcher_x = SCREEN_WIDTH - 50 #x-coordinate of the catcher's position
catcher_y = SCREEN_HEIGHT // 2 #y-coordinate of the catcher's position


game_over = False
paused = False
exit_game = False
RETRY_BUTTON_LOCATION = (20, SCREEN_HEIGHT - 50)
# PAUSE_BUTTON_LOCATION = (SCREEN_WIDTH / 2, SCREEN_HEIGHT - 50)
# EXIT_BUTTON_LOCATION = (SCREEN_WIDTH - 50, SCREEN_HEIGHT - 50)

PAUSE_BUTTON_LOCATION = (30, SCREEN_HEIGHT - 100)  # Slightly lower
EXIT_BUTTON_LOCATION = (SCREEN_WIDTH - 60, SCREEN_HEIGHT - 30)  # Slightly inward



retry_color =  (1.0, 1.0, 1.0)
pause_color =  (1.0, 1.0, 1.0)
exit_color =  (1.0, 1.0, 1.0)

# New variable for football field color
football_field_color = [0.529, 0.808, 0.922]  # Default color: light blue
current_color_flag = 0  # 0: Default, 1: Green, 2: Blue, 3: Red 4: back to default

# Football variables
ball_radius = 15
ball_x = SCREEN_WIDTH // 2
ball_y = SCREEN_HEIGHT // 2
ball_speed = 1
ball_direction = [0, 0]  # Initial direction 

# Player variables
player_radius = 30
player1_x = SCREEN_WIDTH // 3
player1_y = SCREEN_HEIGHT // 2

player2_x = 2 * SCREEN_WIDTH // 3
player2_y = SCREEN_HEIGHT // 2

player1_speed = 5
player2_speed = 5

player1_score = 0
player2_score = 0

player1_movement = {'W': False, 'A': False, 'S': False, 'D': False}
player2_movement = {'I': False, 'J': False, 'K': False, 'L': False}

#_______________________________________________________________Football______________________________________________________

class Football:
    def __init__(self, x, y, radius, speed):
        self.x = x
        self.y = y
        self.radius = radius
        self.speed = speed
        self.direction = [0, 0]  # Initial direction 

    def move(self): #updating the position of the ball
        # Update ball position
        self.x += self.speed * self.direction[0]
        self.y += self.speed * self.direction[1]

        # Check collision with walls
        if self.x - self.radius < 50 or self.x + self.radius > SCREEN_WIDTH - 50:
            self.direction[0] *= -1  # Reverse the x-direction

        if self.y - self.radius < 50 or self.y + self.radius > SCREEN_HEIGHT - 50:
            self.direction[1] *= -1  # Reverse the y-direction
            
#___________________________________________button______________________________________________________________________________________________________________________________________________________________



def draw_retry_button(x, y, color=retry_color):
    size = 10  # Reduced size
    draw_midpoint_line(x, y, x + size, y - size, color)
    draw_midpoint_line(x, y, x + size, y + size, color)
    draw_midpoint_line(x, y, x + 2 * size, y, color)



def draw_pause_button(x, y, color=pause_color):
    size = 5  # Reduced size
    draw_midpoint_line(x + size, y + 2 * size, x + size, y - 2 * size, color)
    draw_midpoint_line(x - size, y + 2 * size, x - size, y - 2 * size, color)


    

def draw_play_button(x, y, color=pause_color):
    size = 5  # Reduced size
    draw_midpoint_line(x - size, y + 2 * size, x - size, y - 2 * size, color)
    draw_midpoint_line(x - size, y + 2 * size, x + size, y, color)
    draw_midpoint_line(x - size, y - 2 * size, x + size, y, color)

def draw_exit(x, y, color=exit_color):
    size = 10  # Reduced size
    draw_midpoint_line(x - size, y + size, x + size, y - size, color)
    draw_midpoint_line(x - size, y - size, x + size, y + size, color)    

def handle_mouse(button, state, x, y): #represent the mouse button, button state, and coordinates of the mouse click.
    global paused, exit_game, game_over, player1_score, player2_score

    # Transform y to match OpenGL coordinate system
    y = SCREEN_HEIGHT - y #adjusts the y-coordinate to match the OpenGL system.

    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN: #checks if the left mouse button is pressed down

        #checks if the mouse click is within the bounds of the pause button
        if (PAUSE_BUTTON_LOCATION[0] - 20 <= x <= PAUSE_BUTTON_LOCATION[0] + 20 #checks if the mouse click is within the bounds of the pause button
            and PAUSE_BUTTON_LOCATION[1] - 20 <= y <= PAUSE_BUTTON_LOCATION[1] + 20):
            paused = not paused
            if paused:
                print("Game Paused")
            else:
                print("Game Resumed")

        #checks if the mouse click is within the bounds of the exit button
        elif (EXIT_BUTTON_LOCATION[0] - 10 <= x <= EXIT_BUTTON_LOCATION[0] + 10 
            and EXIT_BUTTON_LOCATION[1] - 10 <= y <= EXIT_BUTTON_LOCATION[1] + 10):
            print("Exiting Game")
            glutLeaveMainLoop()  # This will close the window

        #This block checks if the mouse click is within the bounds of the retry button.
        elif (RETRY_BUTTON_LOCATION[0] <= x <= RETRY_BUTTON_LOCATION[0] + 50
            and RETRY_BUTTON_LOCATION[1] <= y <= RETRY_BUTTON_LOCATION[1] + 20):
            print("Resetting Game")
            reset_game()
            reset_ball()

#___________________________________________SCORE__________________________________________________________________________________________
def draw_scoreboard():
    """Draw the scoreboard at the top center of the screen."""
    score_text = f"{player1_score} - {player2_score}"
    glColor3f(1.0, 1.0, 1.0)  # White color for the text
    glRasterPos2f(SCREEN_WIDTH // 2 - 25, SCREEN_HEIGHT - 40)  # Adjust position
    for char in score_text:
        glutBitmapCharacter(GLUT_BITMAP_TIMES_ROMAN_24, ord(char)) # type: ignore


#___________________________________________CATCHER________________________________________________________________________________________


def draw_catcher():
    glColor3f(1.0, 0.0, 0.0)  # Red color for the catcher
    glPushMatrix()
    glTranslatef(SCREEN_WIDTH - 50, SCREEN_HEIGHT // 2, 0.0)  # Align to the right boundary
    glRotatef(90.0, 0.0, 0.0, 1.0)  # Rotate vertically
    glTranslatef(-(SCREEN_WIDTH - 50), -(SCREEN_HEIGHT // 2), 0.0)

    # Define coordinates relative to the boundary
    x1, x2 = SCREEN_WIDTH - 50 - CATCHER_WIDTH / 2, SCREEN_WIDTH - 50 + CATCHER_WIDTH / 2
    y1, y2 = SCREEN_HEIGHT // 2 + CATCHER_HEIGHT / 2, SCREEN_HEIGHT // 2 - CATCHER_HEIGHT / 2
    draw_rectangle(x1, y1, x2, y2)  # Use a rectangle for simplicity

    glPopMatrix()


def draw_second_catcher():
    glColor3f(0.0, 0.0, 0.0)  # Black color for the catcher
    glPushMatrix()
    glTranslatef(50, SCREEN_HEIGHT // 2, 0.0)  # Align to the left boundary
    glRotatef(-90.0, 0.0, 0.0, 1.0)  # Rotate vertically
    glTranslatef(-50, -(SCREEN_HEIGHT // 2), 0.0)

    # Define coordinates relative to the boundary
    x1, x2 = 50 - CATCHER_WIDTH / 2, 50 + CATCHER_WIDTH / 2
    y1, y2 = SCREEN_HEIGHT // 2 + CATCHER_HEIGHT / 2, SCREEN_HEIGHT // 2 - CATCHER_HEIGHT / 2
    draw_rectangle(x1, y1, x2, y2)  # Use a rectangle for simplicity

    glPopMatrix()




#_______________________________________________________Midpoint Line Algo___________________________________________________

def draw_midpoint_line(x1, y1, x2, y2, color): #defines the two endpoints of the line and color
    zone = find_zone(x1, y1, x2, y2)
    x1, y1 = to_zone0(zone, x1, y1) #call the zone0converter function used to convert the coordinates based on the determined zone.
    x2, y2 = to_zone0(zone, x2, y2)

    dx = x2 - x1 #change in x
    dy = y2 - y1 #change in y

    d = 2 * dy - dx #initial decision
    incrE = 2 * dy #for updating d if east is chosen
    incrNE = 2 * (dy - dx) #for updating d if northeast is chosen

    x = x1 
    y = y1
    x0, y0 = to_zoneM(zone, x, y)

    draw_points(x0, y0, color)
    while x < x2:
        if d <= 0:  
            d = d + incrE #if dinit less than zero then d is updated by adding dinit and de
            x = x + 1 #move the iteration to the next pixel in the east direction
        else:
            d = d + incrNE #if dinit greater than or equal to zero then d is updated by adding dinit and dne
            x = x + 1 #move the iteration to the next pixel in the northeast direction
            y = y + 1 ##move the iteration to the next pixel in the northeast direction
        x0, y0 = to_zoneM(zone, x, y)

        draw_points(x0, y0, color)

    
def to_zone0(zone, x, y): #for converting to zone zero coordinates
    if zone == 0:
        return x, y
    elif zone == 1:
        return y, x
    elif zone == 2:
        return y, -x
    elif zone == 3:
        return -x, y
    elif zone == 4:
        return -x, -y
    elif zone == 5:
        return -y, -x
    elif zone == 6:
        return -y, x
    elif zone == 7:
        return x, -y
    else:
        raise ValueError("Zone must be in [0, 7]")

def to_zoneM(zone, x, y): ##for converting coordinates from Zone 0 to their original zone
    if zone == 0:
        return x, y
    elif zone == 1:
        return y, x
    elif zone == 2:
        return -y, x
    elif zone == 3:
        return -x, y
    elif zone == 4:
        return -x, -y
    elif zone == 5:
        return -y, -x
    elif zone == 6:
        return y, -x
    elif zone == 7:
        return x, -y
    else:
        raise ValueError("Zone must be in [0, 7]")

def find_zone(x1, y1, x2, y2): #determines the zone of a line based on the signs of the differences in x and y coordinates between its two endpoints
    dx = x2 - x1
    dy = y2 - y1
    if abs(dx) > abs(dy): # For Zone 0, 3, 4 and 7
        if dx >= 0 and dy >= 0:
            return 0
        elif dx >= 0 and dy <= 0:
            return 7
        elif dx <= 0 and dy >= 0:
            return 3
        elif dx <= 0 and dy <= 0:
            return 4
    else:                 #For zone 1, 2, 5, and 6
        if dx >= 0 and dy >= 0:
            return 1
        elif dx <= 0 and dy >= 0:
            return 2
        elif dx <= 0 and dy <= 0:
            return 5
        elif dx >= 0 and dy <= 0:
            return 6
        
def draw_points(x, y, color=WHITE, size=2):
    glColor3fv(color)
    glPointSize(size)
    glBegin(GL_POINTS)
    glVertex2f(x, y)
    glEnd()
     
#_____________________________________________Midpoint Circle Algo_________________________________________________________    

def circ_point(x, y, cx, cy):               
    glVertex2f(cx + x, cy + y) #south
    glVertex2f(cx + y, cy + x) #southeast
    glVertex2f(cx + y, cy - x) #east
    glVertex2f(cx + x, cy - y) #northeast
    glVertex2f(cx - x, cy - y) #north
    glVertex2f(cx - y, cy - x) #northwest
    glVertex2f(cx - y, cy + x) #west
    glVertex2f(cx - x, cy + y) #southwest

def mid_circle(cx, cy, radius): #implementing midpoint circle algorithm
    d = 1 - radius #initial decision parameter
    x = 0
    y = radius

    glBegin(GL_POINTS) #for drawing points for the circle
    circ_point(x, y, cx, cy)

    while x < y:
        if d < 0: #if initial decision parameter is negative then east pixel is chosen
            d = d + 2 * x + 3 #updating decision parameter accordingly
        else: #if decision parameter is positive southeast pixel is chosen
            d = d + 2 * x - 2 * y + 5 #updating decision parameter accordingly
            y = y - 1 #value of y is decremented by 1

        x = x + 1 #in both cases value of x will increment by 1
        circ_point(x, y, cx, cy)

    glEnd()

def draw_circle(x, y, radius):
    mid_circle(x, y, radius)

def draw_filled_circle(x, y, radius):
    num_segments = 100
    delta_theta = 2.0 * pi / num_segments

    glBegin(GL_POLYGON)
    for _ in range(num_segments):
        theta = _ * delta_theta
        glVertex2f(x + radius * cos(theta), y + radius * sin(theta))
    glEnd()

#________________________________________________Simple Line Drawing________________________________________________________

def draw_line(x1, y1, x2, y2):
    glBegin(GL_LINES)
    glVertex2f(x1, y1)
    glVertex2f(x2, y2)
    glEnd()

def draw_football_field():
    glColor3fv(football_field_color)
    glBegin(GL_QUADS)
    glVertex2f(50, 50)
    glVertex2f(SCREEN_WIDTH - 50, 50)
    glVertex2f(SCREEN_WIDTH - 50, SCREEN_HEIGHT - 50)
    glVertex2f(50, SCREEN_HEIGHT - 50)
    glEnd()

    # Set color for lines
    glColor3f(1.0, 1.0, 1.0)  # White for the lines

    # Draw field outline
    draw_line(50, 50, SCREEN_WIDTH - 50, 50)
    draw_line(50, SCREEN_HEIGHT - 50, SCREEN_WIDTH - 50, SCREEN_HEIGHT - 50)
    draw_line(50, 50, 50, SCREEN_HEIGHT - 50)
    draw_line(SCREEN_WIDTH - 50, 50, SCREEN_WIDTH - 50, SCREEN_HEIGHT - 50)

    # Draw midfield line
    draw_line(SCREEN_WIDTH // 2, 50, SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50)

    # Draw center circle using midpoint circle algorithm
    mid_circle(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, 50)

    # Draw penalty areas (adjust coordinates to make them the same size)
    draw_rectangle(50, SCREEN_HEIGHT // 2 - 100, 150, SCREEN_HEIGHT // 2 + 100)
    draw_rectangle(SCREEN_WIDTH - 150, SCREEN_HEIGHT // 2 - 100, SCREEN_WIDTH - 50, SCREEN_HEIGHT // 2 + 100)
    
    
    

def draw_rectangle(x1, y1, x2, y2): #for the Dbox
    glBegin(GL_LINE_LOOP)
    glVertex2f(x1, y1)
    glVertex2f(x2, y1)
    glVertex2f(x2, y2)
    glVertex2f(x1, y2)
    glEnd()

def draw_player(x, y):
    glColor3f(1.0, 1.0, 1.0)                           # White color for player 1
    mid_circle(x, y, player_radius)
    mid_circle(x, y, player_radius - 3)
    mid_circle(x, y, player_radius - 6)
    mid_circle(x, y, player_radius - 9)
    # draw_filled_circle(x, y, player_radius)

def draw_player2(x, y):
    glColor3f(0.0, 0.0, 0.0)                           # Black color for player 2
    mid_circle(x, y, player_radius)
    # draw_filled_circle(x, y, player_radius)


def reshape(width, height):
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0, width, 0, height, -1, 1)
    glMatrixMode(GL_MODELVIEW)


#________________________________________________Player Movement_________________________________________________________________

from math import sqrt

def update_player_positions():
# def update_player_positions_with_boundary():
    """
    Update player positions and resolve boundary issues.
    """
    global player1_x, player1_y, player2_x, player2_y

    if not paused:
        # Update player 1
        dx, dy = 0, 0
        if player1_movement['W']:
            dy += player1_speed
        if player1_movement['A']:
            dx -= player1_speed
        if player1_movement['S']:
            dy -= player1_speed
        if player1_movement['D']:
            dx += player1_speed

        player1_x += dx
        player1_y += dy
        player1_x, player1_y = resolve_boundary_collision(player1_x, player1_y, player_radius)

        # Update player 2
        dx, dy = 0, 0
        if player2_movement['I']:
            dy += player2_speed
        if player2_movement['J']:
            dx -= player2_speed
        if player2_movement['K']:
            dy -= player2_speed
        if player2_movement['L']:
            dx += player2_speed

        player2_x += dx
        player2_y += dy
        player2_x, player2_y = resolve_boundary_collision(player2_x, player2_y, player_radius)

        # Check for overlap between players and resolve
        dx = player2_x - player1_x
        dy = player2_y - player1_y
        distance = sqrt(dx**2 + dy**2)
        if distance < 2 * player_radius:
            overlap = 2 * player_radius - distance
            if distance != 0:
                dx /= distance
                dy /= distance
            else:
                dx, dy = 1, 0

            player1_x -= dx * overlap / 2
            player1_y -= dy * overlap / 2
            player2_x += dx * overlap / 2
            player2_y += dy * overlap / 2




def keyboard(key, x, y):
    global player1_movement, player2_movement, football_field_color, current_color_flag



    # Player 1 controls
    if key == b'W' or key == b'w':
        player1_movement['W'] = True
    elif key == b'A' or key == b'a':
        player1_movement['A'] = True
    elif key == b'S' or key == b's':
        player1_movement['S'] = True
    elif key == b'D' or key == b'd':
        player1_movement['D'] = True

    # Player 2 controls
    elif key == b'I' or key == b'i':
        player2_movement['I'] = True
    elif key == b'J' or key == b'j':
        player2_movement['J'] = True
    elif key == b'K' or key == b'k':
        player2_movement['K'] = True
    elif key == b'L' or key == b'l':
        player2_movement['L'] = True
        
        
    # Change football field color based on keyboard input
    
    if key == b'1':
        football_field_color = [0.0, 1.0, 0.0]  # Green
        current_color_flag = 1
    elif key == b'2':
        football_field_color = [0.0, 0.0, 1.0]  # Blue
        current_color_flag = 2
    elif key == b'3':
        football_field_color = [1.0, 0.0, 0.0]  # Red
        current_color_flag = 3
    elif key == b'4':
        football_field_color = [0.529, 0.808, 0.922]  # Light blue (default)
        current_color_flag = 0

    glutPostRedisplay()


def keyboard_release(key, x, y):
    global player1_movement, player2_movement

    # Player 1 controls
    if key == b'W' or key == b'w':
        player1_movement['W'] = False
    elif key == b'A' or key == b'a':
        player1_movement['A'] = False
    elif key == b'S' or key == b's':
        player1_movement['S'] = False
    elif key == b'D' or key == b'd':
        player1_movement['D'] = False

    # Player 2 controls
    elif key == b'I' or key == b'i':
        player2_movement['I'] = False
    elif key == b'J' or key == b'j':
        player2_movement['J'] = False
    elif key == b'K' or key == b'k':
        player2_movement['K'] = False
    elif key == b'L' or key == b'l':
        player2_movement['L'] = False

    glutPostRedisplay()

football = Football(ball_x, ball_y, ball_radius, ball_speed)

#__________________________________________________________Ball Movement________________________________________________

def check_collision_with_resolution(player_x, player_y, player_radius, ball):
    """
    Check and resolve collision between a player and the ball.
    """
    dx = ball.x - player_x
    dy = ball.y - player_y
    distance = sqrt(dx**2 + dy**2)

    if distance < player_radius + ball.radius:
        # Resolve overlap
        overlap = player_radius + ball.radius - distance
        if distance != 0:  # Avoid division by zero
            dx /= distance
            dy /= distance
        else:  # Assign arbitrary direction if distance is zero
            dx, dy = 1, 0

        ball.x += dx * overlap  # Push the ball away
        ball.y += dy * overlap

        # Reflect the ball's direction
        ball.direction[0] = dx
        ball.direction[1] = dy


def resolve_boundary_collision(player_x, player_y, player_radius):
    """
    Ensure the player stays within boundaries.
    """
    if player_x - player_radius < 50:
        player_x = 50 + player_radius
    elif player_x + player_radius > SCREEN_WIDTH - 50:
        player_x = SCREEN_WIDTH - 50 - player_radius

    if player_y - player_radius < 50:
        player_y = 50 + player_radius
    elif player_y + player_radius > SCREEN_HEIGHT - 50:
        player_y = SCREEN_HEIGHT - 50 - player_radius

    return player_x, player_y


        
def update_timer(value):
    global paused

    if not paused:
        football.move()
        update_ball_position()
        glutPostRedisplay()

    glutTimerFunc(10, update_timer, 0)



def update_ball_position():
# def update_ball_position_with_collisions():
    """
    Update ball position and handle collisions with players and boundaries.
    """
    global player1_score, player2_score  # Ensure scores are treated as global

    football.move()

    # Check collisions with players
    check_collision_with_resolution(player1_x, player1_y, player_radius, football)
    check_collision_with_resolution(player2_x, player2_y, player_radius, football)

    # Check for scoring or boundary collision
    if football.x - ball_radius < 50 and SCREEN_HEIGHT // 2 - 100 < football.y < SCREEN_HEIGHT // 2 + 100:
        print("Player 2 scores!")
        player2_score += 1
        reset_ball()
    elif football.x + ball_radius > SCREEN_WIDTH - 50 and SCREEN_HEIGHT // 2 - 100 < football.y < SCREEN_HEIGHT // 2 + 100:
        print("Player 1 scores!")
        player1_score += 1
        reset_ball()

    # Ensure ball doesn't get stuck at boundaries
    if football.x - ball_radius < 50:
        football.x = 50 + ball_radius
        football.direction[0] = abs(football.direction[0])
    elif football.x + ball_radius > SCREEN_WIDTH - 50:
        football.x = SCREEN_WIDTH - 50 - ball_radius
        football.direction[0] = -abs(football.direction[0])

    if football.y - ball_radius < 50:
        football.y = 50 + ball_radius
        football.direction[1] = abs(football.direction[1])
    elif football.y + ball_radius > SCREEN_HEIGHT - 50:
        football.y = SCREEN_HEIGHT - 50 - ball_radius
        football.direction[1] = -abs(football.direction[1])


        
#####################################################################
# resetting

def reset_ball():
    # Reset the ball to the center of the field
    global ball_x, ball_y, ball_direction
    ball_x = SCREEN_WIDTH // 2
    ball_y = SCREEN_HEIGHT // 2
    ball_direction = [0, 0]  # Stop the ball


    
def reset_game():
    global player1_x, player1_y, player2_x, player2_y, ball_x, ball_y, ball_direction, player1_score, player2_score, ball_speed, paused
    player1_x = SCREEN_WIDTH // 3
    player1_y = SCREEN_HEIGHT // 2
    player2_x = 2 * SCREEN_WIDTH // 3
    player2_y = SCREEN_HEIGHT // 2
    ball_x = SCREEN_WIDTH // 2
    ball_y = SCREEN_HEIGHT // 2
    football.x = ball_x
    football.y = ball_y
    ball_direction = [0, 0]  # Stop the ball
    player1_score = 0
    player2_score = 0
    
    paused = True  # To ensure the game is not paused after reset




#___________________________________________DISPLAY________________________________________________________________________________________    

def display():
    glClear(GL_COLOR_BUFFER_BIT)
    glColor3f(1.0, 1.0, 1.0)  # White color for lines
    glPointSize(2.0)
    update_player_positions()
    football.move()
    update_ball_position()
    reset_ball()
    draw_football_field()
    draw_player(player1_x, player1_y)  # Draw player 1
    draw_player2(player2_x, player2_y)  # Draw player 2
    glColor3f(1.0, 1.0, 0.0)
    draw_filled_circle(football.x, football.y, ball_radius)
    global catcher_color
    draw_catcher()
    catcher_color = (0.0, 0.0, 0.0)  # Black color
    draw_second_catcher()
    draw_football_field()
    draw_player(player1_x, player1_y)
    draw_player2(player2_x, player2_y)
    draw_filled_circle(football.x, football.y, ball_radius)
    draw_catcher()
    draw_second_catcher()
    # display_hearts()
    
    
    draw_retry_button(RETRY_BUTTON_LOCATION[0], RETRY_BUTTON_LOCATION[1])
    draw_exit(EXIT_BUTTON_LOCATION[0], EXIT_BUTTON_LOCATION[1])
    if not paused:
        draw_pause_button(PAUSE_BUTTON_LOCATION[0], PAUSE_BUTTON_LOCATION[1])
    else:
        draw_play_button(PAUSE_BUTTON_LOCATION[0], PAUSE_BUTTON_LOCATION[1])

    draw_scoreboard()
    
    glutSwapBuffers()



glutInit()
glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
glutInitWindowSize(SCREEN_WIDTH, SCREEN_HEIGHT)

screen_width = glutGet(GLUT_SCREEN_WIDTH)
screen_height = glutGet(GLUT_SCREEN_HEIGHT)

glutInitWindowPosition((screen_width - SCREEN_WIDTH) // 2, (screen_height - SCREEN_HEIGHT) // 2)
glutCreateWindow(b"Football")

glutDisplayFunc(display)
glutReshapeFunc(reshape)
glutKeyboardFunc(keyboard)
glutKeyboardUpFunc(keyboard_release)  
glutTimerFunc(0, update_timer, 0)
glClearColor(0.529, 0.808, 0.922, 1.0)
glutMouseFunc(handle_mouse)

glutMainLoop()

