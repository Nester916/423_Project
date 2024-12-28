from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random as rand
import math

# window
width, height = 800, 700

pause=False
dead=False
# shooter
shooter1_cx, shooter1_cy, shooter_r, shooter_s = 30, 300, 20, 15
shooter2_cx, shooter2_cy = 770, 300
shooter1_shift, shooter2_shift, shooter1_incr, shooter2_incr = 0, 0, 8, 8
shooter1_mode=0
shooter2_mode=2
life1=3
life2=3
shotBubble1_cx, shotBubble1_cy, shotBubble1_cl, shotBubble_r = [], [], [], 5
shotBubble2_cx, shotBubble2_cy, shotBubble2_cl = [], [], []
shot1_stat=[]
shot2_stat=[]
shtr1_scor=0
shtr2_scor=0
key_state = {
    b'w': False,  # for shooter1 go up
    b's': False,  # for shooter1 go down
    b'e': False,  #1 shoot red bullet
    b'r': False,  #1 shoot green bullet
    b't': False,  #1 shoot blue bullet
    'up': False,  # for shooter2 go up
    'down': False,  # for shooter2 go down
    b'/': False,  #2 shoot red bullet
    b'.': False,  #2 shoot green bullet
    b',': False,  #2 shoot blue bullet
}


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

def mid_circle(cx, cy, rad):
    d = 1 - rad
    x = 0
    y = rad

    while x < y:
        if d < 0:
            d = d + 2 * x + 3
        else:
            d = d + 2 * x - 2 * y + 5
            y = y - 1
        x = x + 1
        circ_points(x, y, cx, cy)

def circ_points(x, y, cx, cy):
    print(x + cx, y + cy)
    glVertex2f(x + cx, y + cy)
    glVertex2f(y + cx, x + cy)

    glVertex2f(y + cx, -x + cy)
    glVertex2f(x + cx, -y + cy)

    glVertex2f(-x + cx, -y + cy)
    glVertex2f(-y + cx, -x + cy)

    glVertex2f(-y + cx, x + cy)
    glVertex2f(-x + cx, y + cy)

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
    global shooter1_cx, shooter1_cy, shooter_r, shooter1_shift
    m= shooter1_cx
    n= shooter1_cy+shooter1_shift
    if shooter1_mode==0:
        glColor3f(1,0,0)
    elif shooter1_mode==1:
        glColor3f(0,1,0)
    elif shooter1_mode==2:
        glColor3f(0,0,1)
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
    global shooter2_cx, shooter2_cy, shooter_r, shooter2_shift
    m= shooter2_cx
    n= shooter2_cy+shooter2_shift
    if shooter2_mode==0:
        glColor3f(1,0,0)
    elif shooter2_mode==1:
        glColor3f(0,1,0)
    elif shooter2_mode==2:
        glColor3f(0,0,1)
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

def shooter_mode(n=0):
    global shooter1_mode, shooter2_mode
    shooter1_mode=(shooter1_mode+1)%3
    shooter2_mode=(shooter2_mode+1)%3
    glutTimerFunc(6000, shooter_mode, 0)

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
    animate()
    glEnd()
    glutSwapBuffers()
    glutPostRedisplay()

def keyboardListener(key, x, y):
    global shooter1_cx, shooter1_cy, shotBubble1_cx, shotBubble1_cy, shooter1_shift, shooter2_cx, shooter2_cy, shotBubble2_cx, shotBubble2_cy, shooter2_shift
    global shot1_stat, shot2_stat, pause, dead
    if key == b"e":
        shot1_stat+=[0]
        shotBubble1_cx += [25+shooter1_cx]
        shotBubble1_cy += [shooter1_cy+ shooter1_shift]
    if key == b"r":
        shot1_stat+=[1]
        shotBubble1_cx += [25+shooter1_cx]
        shotBubble1_cy += [shooter1_cy+ shooter1_shift]
    if key == b"t":
        shot1_stat+=[2]
        shotBubble1_cx += [25+shooter1_cx]
        shotBubble1_cy += [shooter1_cy+ shooter1_shift]
    if key == b"/":
        shot2_stat+=[0]
        shotBubble2_cx += [-25+shooter2_cx]
        shotBubble2_cy += [shooter2_cy+ shooter2_shift]
    if key == b".":
        shot2_stat+=[1]
        shotBubble2_cx += [-25+shooter2_cx]
        shotBubble2_cy += [shooter2_cy+ shooter2_shift]
    if key == b",":
        shot2_stat+=[2]
        shotBubble2_cx += [-25+shooter2_cx]
        shotBubble2_cy += [shooter2_cy+ shooter2_shift]


def animate():
    global shooter1_incr, shooter1_shift, shotBubble1_cx, shotBubble1_cy, shooter1_incr, shooter1_shift, shotBubble1_cx, shotBubble1_cy, shotBubble_r
    global pause, dead, shot1_stat, shot2_stat
    global life
    if not pause and not dead:
        for i in range(len(shotBubble1_cy)):
            if shotBubble1_cx[i]+5 <= 800 and shot1_stat[i] in [0,1,2]:
                if shot1_stat[i]==0:
                    glColor3f(1,0,0)
                if shot1_stat[i]==1:
                    glColor3f(0,1,0)
                if shot1_stat[i]==2:
                    glColor3f(0,0,1)
                print(shotBubble1_cx[i], shotBubble1_cy[i])
                print(3)
                shotBubble1_cx[i] = shotBubble1_cx[i] + shooter1_incr
                mid_circle(shotBubble1_cx[i], shotBubble1_cy[i], shotBubble_r)
            elif shotBubble1_cy[i]+5 >= 800 and shot1_stat[i] in [0,1,2]:
                life-=1
                #shtr_rst(i)
                print("Remaining life:", life)
            else:
                print(1)
                #shtr_rst(i)
        #game_over()
        for i in range(len(shotBubble2_cy)):
            if shotBubble2_cx[i]+5 >= 0 and shot2_stat[i] in [0,1,2]:
                if shot2_stat[i]==0:
                    glColor3f(1,0,0)
                if shot2_stat[i]==1:
                    glColor3f(0,1,0)
                if shot2_stat[i]==2:
                    glColor3f(0,0,1)
                print(shotBubble2_cx[i], shotBubble2_cy[i])
                shotBubble2_cx[i] = shotBubble2_cx[i] - shooter2_incr
                mid_circle(shotBubble2_cx[i], shotBubble2_cy[i], shotBubble_r)
            elif shotBubble2_cy[i]+5 <= 0 and shot1_stat[i] in [0,1,2]:
                life-=1
                #shtr_rst(i)
                print("Remaining life:", life)
            else:
                print(1)
                #shtr_rst(i)
        #game_over()
    else:
        for i in range(len(shotBubble1_cy)):
            if shotBubble1_cy[i]+5 <= 800 and shot1_stat[i] in [0,1,2]:
                mid_circle(shotBubble1_cx[i], shotBubble1_cy[i], shotBubble_r)
        for i in range(len(shotBubble2_cy)):
            if shotBubble2_cy[i]+5 >= 0 and shot1_stat[i] in [0,1,2]:
                mid_circle(shotBubble2_cx[i], shotBubble2_cy[i], shotBubble_r)
            
    glutPostRedisplay()


glutInit()
glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
glutInitWindowSize(width, height)
shooter2p = glutCreateWindow(b"Space Shooter - 2P")
init()
shooter_mode()
glutDisplayFunc(display)
#glutIdleFunc(animate)
glutKeyboardFunc(keyboardListener)
#glutKeyboardUpFunc(keyboard_up)
#glutSpecialFunc(special_keyboard)
#glutSpecialUpFunc(special_keyboard_up)
#glutIdleFunc(update_game)
glEnable(GL_DEPTH_TEST)
glutMainLoop()