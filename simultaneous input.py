from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

key_states = {}
window_width = 500
window_height = 500
def key_down(key, x, y):
    key_states[key] = True
def key_up(key, x, y):
    key_states[key] = False
def game_logic():
    if key_states.get(b'w', False):
        print("Player 1 moves up")
    if key_states.get(b's', False): 
        print("Player 1 moves down")
    if key_states.get(b'a', False):
        print("Player 1 moves left")
    if key_states.get(b'd', False):
        print("Player 1 moves right")
    if key_states.get(b'i', False):
        print("Player 2 moves up")
    if key_states.get(b'k', False):
        print("Player 2 moves down")
    if key_states.get(b'j', False):
        print("Player 2 moves left")
    if key_states.get(b'l', False):
        print("Player 2 moves right")
def render():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    game_logic()
    glutSwapBuffers()
def idle():
    glutPostRedisplay()
def init():
    glClearColor(0.0, 0.0, 0.0, 1.0)
    gluOrtho2D(0, window_width, 0, window_height)

glutInit()
glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
glutInitWindowSize(window_width, window_height)
glutCreateWindow(b"Multiplayer Game Example")  
init()
glutDisplayFunc(render)
glutIdleFunc(idle)
glutKeyboardFunc(key_down)
glutKeyboardUpFunc(key_up)
glutMainLoop()
