from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random as rand
import math

# window
width, height = 800, 700

pause=False
# shooter
shooter_cx1, shooter_cy1, shooter_r, shooter_s = 30, 300, 20, 15
shooter_cx2, shooter_cy2, shooter_r, shooter_s = 770, 300, 20, 15
shooter_shift, shooter_incr = 0, 0.4

def init():
    glClearColor(0, 0, 0, 0)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0, width, 0, height, 0, 1)
    glMatrixMode(GL_MODELVIEW)

def draw_line(a1, b1, a2, b2):
    zone, x1, y1, x2, y2 = findZone_convertToZero(a1, b1, a2, b2)
    midpoint_line_algo(x1, y1, x2, y2, zone)

def findZone_convertToZero(x1, y1, x2, y2):
    dx = x2 - x1
    dy = y2 - y1

    if abs(dx) >= abs(dy):  # zone 0, 3, 4, and 7
        if x2 >= x1:
            if y2 >= y1:
                return 0, x1, y1, x2, y2
            else:
                return 7, x1, -y1, x2, -y2
        else:
            if y2 >= y1:
                return 3, -x1, y1, -x2, y2
            else:
                return 4, -x1, -y1, -x2, -y2
    else:  # zone 1, 2, 5, and 6
        if x2 >= x1:
            if y2 >= y1:
                return 1, y1, x1, y2, x2
            else:
                return 6, -y1, x1, -y2, x2

        else:
            if y2 >= y1:
                return 2, y1, -x1, y2, -x2
            else:
                return 5, -y1, -x1, -y2, -x2

def midpoint_line_algo(x1, y1, x2, y2, zone):

    dx = x2 - x1
    dy = y2 - y1

    d = 2 * dy - dx

    incr_NE = dy - dx
    incr_E = dy

    start = int(x1)
    end = int(x2)
    y = y1

    for x in range(start, end + 1):
        draw_point(x, y, zone)

        if d > 0:
            d = d + incr_NE
            y += 1
        else:
            d += incr_E

def draw_point(x, y, zone):
    if zone == 0:
        draw_pixel(x, y)
    elif zone == 1:
        draw_pixel(y, x)
    elif zone == 2:
        draw_pixel(-y, x)
    elif zone == 3:
        draw_pixel(-x, y)
    elif zone == 4:
        draw_pixel(-x, -y)
    elif zone == 5:
        draw_pixel(-y, -x)
    elif zone == 6:
        draw_pixel(y, -x)
    elif zone == 7:
        draw_pixel(x, -y)

def draw_pixel(x, y):

    glPointSize(3)
    glBegin(GL_POINTS)
    glVertex2f(x, y)
    glEnd()

def draw_res():
    glColor3f(0.0, 0.5, 0.8)
    draw_line(30, 690, 5, 670)
    draw_line(5, 670, 30, 650)
    draw_line(5, 670, 60, 670)

def draw_cross():
    glColor3f(1.0, 0.0, 0.0)
    draw_line(760, 690, 790, 650)
    draw_line(760, 650, 790, 690)

def draw_pause():
    global pause
    glColor3f(1.0, 1.0, 0.0)
    if pause == True:
        draw_line(380, 690, 420, 670)
        draw_line(420, 670, 380, 650)
        draw_line(380, 650, 420, 690)
    else:
        draw_line(390, 690, 390, 650)
        draw_line(410, 690, 410, 650)

def draw_shtr1():
    global shooter_cx1, shooter_cy1, shooter_r, shooter_shift
    m= shooter_cx1
    n= shooter_cy1+shooter_shift
    #draw_line(m+7, n+10, m-7, n+10)
    draw_line(m+10, n+7, m-15, n+7)
    draw_line(m+10, n-7, m-15, n-7)
    draw_line(m-15, n-7, m-15, n+7)
    draw_line(m+10, n-7, m+20, n)
    draw_line(m+10, n+7, m+20, n)
    #draw_line(m-20, n+15, m-20, n-15)
    draw_line(m-20, n+15, m-10, n+15)
    draw_line(m-10, n+15, m-5, n+7)
    draw_line(m-20, n-15, m-10, n-15)
    draw_line(m-10, n-15, m-5, n-7)
    draw_line(m-20, n+15, m-15, n+7)
    draw_line(m-20, n-15, m-15, n-7)

def draw_shtr2():
    global shooter_cx1, shooter_cy1, shooter_r, shooter_shift
    m= shooter_cx2
    n= shooter_cy2+shooter_shift
    #draw_line(m+7, n+10, m-7, n+10)
    draw_line(m-10, n+7, m+15, n+7)
    draw_line(m-10, n-7, m+15, n-7)
    draw_line(m+15, n-7, m+15, n+7)
    draw_line(m-10, n-7, m-20, n)
    draw_line(m-10, n+7, m-20, n)
    # Rocket fins
    draw_line(m+20, n+15, m+10, n+15)
    draw_line(m+10, n+15, m+5, n+7)
    draw_line(m+20, n-15, m+10, n-15)
    draw_line(m+10, n-15, m+5, n-7)
    draw_line(m+20, n+15, m+15, n+7)
    draw_line(m+20, n-15, m+15, n-7)

def display():

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    draw_res()
    draw_cross()
    draw_pause()
    glPointSize(2)
    draw_shtr1()
    draw_shtr2()
    glColor3f(1, 1, 1)
    glBegin(GL_POINTS)
    #draw_bubbles()
    #animate()
    glEnd()
    glutSwapBuffers()
    glutPostRedisplay()



def KeyboardListener(key, x, y):
    global shooter_cy1
    
    
    if key == b'w':
        if shooter_cy1 > 600:
            pass
        else:
            shooter_cy1 += 10 
    
    if key == b's':
        if shooter_cy1 < 50:
            pass
        else:
            shooter_cy1 -= 10
    

def specialKeyListener(key, x, y):
    global shooter_cy2
    
    if key == GLUT_KEY_DOWN:
        if shooter_cy2 < 50:
            pass
        else:
            shooter_cy2 -= 10
    
    if key == GLUT_KEY_UP:
        if shooter_cy2 > 600:
            pass
        else:
            shooter_cy2 += 10
        
    

glutInit()
glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
glutInitWindowSize(width, height)
shooter2p = glutCreateWindow(b"HUE HAVOC - 2P")
init()
glutDisplayFunc(display)
glEnable(GL_DEPTH_TEST)
glutKeyboardFunc(KeyboardListener)
glutSpecialFunc(specialKeyListener)
glutMainLoop()