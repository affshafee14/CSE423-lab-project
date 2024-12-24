import pygame
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import math
pygame.init()
display = (800, 600)
pygame.display.set_mode(display, pygame.DOUBLEBUF | pygame.OPENGL)

ball_pos = [0, 0]
player1_pos = [-0.5, 0]
player2_pos = [0.5, 0]
selected_player = None

def draw_circle_border(x, y, radius):
    """Draw a circle border using GL_POINTS and MPC."""
    glBegin(GL_POINTS)
    x_pos = 0
    y_pos = radius
    decision = 1 - radius

    while x_pos <= y_pos:
        glVertex2f(x + x_pos / 400, y + y_pos / 300)
        glVertex2f(x - x_pos / 400, y + y_pos / 300)
        glVertex2f(x + x_pos / 400, y - y_pos / 300)
        glVertex2f(x - x_pos / 400, y - y_pos / 300)
        glVertex2f(x + y_pos / 400, y + x_pos / 300)
        glVertex2f(x - y_pos / 400, y + x_pos / 300)
        glVertex2f(x + y_pos / 400, y - x_pos / 300)
        glVertex2f(x - y_pos / 400, y - x_pos / 300)

        if decision < 0:
            decision += 2 * x_pos + 3
        else:
            decision += 2 * (x_pos - y_pos) + 5
            y_pos -= 1
        x_pos += 1
    glEnd()

def draw_filled_circle(x, y, radius):
    """Draw a filled circle using GL_POINTS and MPC."""
    glBegin(GL_POINTS)
    for i in range(-radius, radius + 1):
        for j in range(-radius, radius + 1):
            if i * i + j * j <= radius * radius:
                glVertex2f(x + i / 400, y + j / 300)
    glEnd()

def draw_line(start_x, start_y, end_x, end_y):
    glBegin(GL_LINES)
    glVertex2f(start_x, start_y)
    glVertex2f(end_x, end_y)
    glEnd()

def draw_goal(x, width, height):
    draw_line(x, -height / 2, x, height / 2)
    draw_line(x - width, height / 2, x, height / 2)
    draw_line(x - width, -height / 2, x, -height / 2)
    draw_line(x - width, -height / 2, x - width, height / 2)

def draw():
    glClear(GL_COLOR_BUFFER_BIT)
    
    # Field markings
    glColor3f(1, 1, 1)
    draw_line(0, -1, 0, 1)
    draw_circle_border(0, 0, 80)  # Center circle border

    # Goals
    draw_goal(-0.9, 0.1, 0.6)
    draw_goal(0.9, -0.2, 0.6)

    # Players and Ball
    glColor3f(1, 0, 0)  # Player 1
    draw_filled_circle(player1_pos[0], player1_pos[1], 15)  
    glColor3f(0, 0, 1)  # Player 2
    draw_filled_circle(player2_pos[0], player2_pos[1], 15)  
    glColor3f(1, 1, 0)  # Ball
    draw_filled_circle(ball_pos[0], ball_pos[1], 10)  
    
    pygame.display.flip()

def handle_input():
    global selected_player, player1_pos, player2_pos, ball_pos
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
            
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            x = (x / display[0] * 2 - 1)
            y = -(y / display[1] * 2 - 1)
            
            dist1 = ((x - player1_pos[0])**2 + (y - player1_pos[1])**2)**0.5
            dist2 = ((x - player2_pos[0])**2 + (y - player2_pos[1])**2)**0.5
            selected_player = 1 if dist1 < dist2 else 2
            
        elif event.type == pygame.MOUSEBUTTONUP:
            selected_player = None
            
        elif event.type == pygame.MOUSEMOTION and selected_player:
            x, y = pygame.mouse.get_pos()
            x = (x / display[0] * 2 - 1)
            y = -(y / display[1] * 2 - 1)
            
            # Allow full movement for both players across the field
            if selected_player == 1:
                player1_pos = [x, y]
            else:
                player2_pos = [x, y]
    
    return True

def main():
    while handle_input():
        draw()

if __name__ == "__main__":
    main()
