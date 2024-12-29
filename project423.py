from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random as rand
import math

# window
width, height = 800, 700

pause=False
# shooter
shooter1_cx, shooter1_cy, shooter_r, shooter_s = 30, 300, 20, 15
shooter2_cx, shooter2_cy = 770, 300
shooter1_shift, shooter2_shift, shooter1_incr, shooter2_incr = 0, 0, 3, 3
shooter1_mode=0
shooter2_mode=2
life1=3
life2=3
shotBubble1_cx, shotBubble1_cy, shotBubble1_cl, shotBubble_r = [], [], [], 5
shotBubble2_cx, shotBubble2_cy, shotBubble2_cl = [], [], []
shot1_stat=[]
shot2_stat=[]
score1=10
score2=10
dead=False
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
        draw_line(390, 690, 390, 650)
        draw_line(390, 690, 420, 670)
        draw_line(390, 650, 420, 670)
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
    if pause!=True:
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
    collision2()
    collision1()
    glutSwapBuffers()
    glutPostRedisplay()


# Keyboard press event handler for regular keys
def keyboard(key, x, y):
    global key_state
    if key in key_state:
        key_state[key] = True

# Keyboard release event handler for regular keys
def keyboard_up(key, x, y):
    global key_state
    if key in key_state:
        key_state[key] = False

# Special key press event handler for arrow keys
def special_keyboard(key, x, y):
    global key_state
    if key == GLUT_KEY_UP:
        key_state['up'] = True  # Shooter2 move up
    elif key == GLUT_KEY_DOWN:
        key_state['down'] = True  # Shooter2 move down

# Special key release event handler for arrow keys
def special_keyboard_up(key, x, y):
    global key_state
    if key == GLUT_KEY_UP:
        key_state['up'] = False  # Shooter2 stop moving up
    elif key == GLUT_KEY_DOWN:
        key_state['down'] = False  # Shooter2 stop moving down

# Game update function
def update_game():
    global shooter1_cx, shooter1_cy, shotBubble1_cx, shotBubble1_cy, shooter1_shift, shooter2_cx, shooter2_cy, shotBubble2_cx, shotBubble2_cy, shooter2_shift
    global shot1_stat, shot2_stat, pause
    if not pause:
        # Shooter1 movement
        if key_state[b'w'] and shooter1_shift + shooter1_cy < 600:  # Move up
            shooter1_shift += 10
        if key_state[b's'] and shooter1_shift + shooter1_cy > 50:  # Move down
            shooter1_shift -= 10

        # Shooter2 movement
        if key_state['up'] and shooter2_shift + shooter2_cy < 600:  # Move up
            shooter2_shift += 10
        if key_state['down'] and shooter2_shift + shooter2_cy > 50:  # Move down
            shooter2_shift -= 10

        # Shooter1 shooting
        if key_state[b'e']:  # Red bullet
            shot1_stat+=[0]
            shotBubble1_cx += [25+shooter1_cx]
            shotBubble1_cy += [shooter1_cy+ shooter1_shift]
            key_state[b'e'] = False  # Prevent continuous shooting
        if key_state[b'r']:  # Green bullet
            shot1_stat+=[1]
            shotBubble1_cx += [25+shooter1_cx]
            shotBubble1_cy += [shooter1_cy+ shooter1_shift]
            key_state[b'r'] = False
        if key_state[b't']:  # Blue bullet
            shot1_stat+=[2]
            shotBubble1_cx += [25+shooter1_cx]
            shotBubble1_cy += [shooter1_cy+ shooter1_shift]
            key_state[b't'] = False

        # Shooter2 shooting
        if key_state[b'/']:  # Red bullet
            shot2_stat+=[0]
            shotBubble2_cx += [-25+shooter2_cx]
            shotBubble2_cy += [shooter2_cy+ shooter2_shift]
            key_state[b'/'] = False
        if key_state[b'.']:  # Green bullet
            shot2_stat+=[1]
            shotBubble2_cx += [-25+shooter2_cx]
            shotBubble2_cy += [shooter2_cy+ shooter2_shift]
            key_state[b'.'] = False
        if key_state[b',']:  # Blue bullet
            shot2_stat+=[2]
            shotBubble2_cx += [-25+shooter2_cx]
            shotBubble2_cy += [shooter2_cy+ shooter2_shift]
            key_state[b','] = False


def animate():
    global shooter1_incr, shooter1_shift, shotBubble1_cx, shotBubble1_cy, shooter1_incr, shooter1_shift, shotBubble1_cx, shotBubble1_cy, shotBubble_r
    global pause, shot1_stat, shot2_stat, score1, score2
    global life
    if not pause:
        for i in range(len(shotBubble1_cy)):
            if shotBubble1_cx[i]+5 <= 800 and shot1_stat[i] in [0,1,2]:
                if shot1_stat[i]==0:
                    glColor3f(1,0,0)
                if shot1_stat[i]==1:
                    glColor3f(0,1,0)
                if shot1_stat[i]==2:
                    glColor3f(0,0,1)
                shotBubble1_cx[i] = shotBubble1_cx[i] + shooter1_incr
                mid_circle(shotBubble1_cx[i], shotBubble1_cy[i], shotBubble_r)
            elif shotBubble1_cx[i]+5 > 800 and shot1_stat[i] in [0,1,2]:
                shot1_stat[i]=3
                score1-=1
                print(f"Score: Player_1={score1}, Player_2={score2}" )
                
        for i in range(len(shotBubble2_cy)):
            if shotBubble2_cx[i]+5 >= 0 and shot2_stat[i] in [0,1,2]:
                if shot2_stat[i]==0:
                    glColor3f(1,0,0)
                if shot2_stat[i]==1:
                    glColor3f(0,1,0)
                if shot2_stat[i]==2:
                    glColor3f(0,0,1)
                shotBubble2_cx[i] = shotBubble2_cx[i] - shooter2_incr
                mid_circle(shotBubble2_cx[i], shotBubble2_cy[i], shotBubble_r)
            elif shotBubble2_cx[i]+5 < 0 and shot2_stat[i] in [0,1,2]:
                shot2_stat[i]=3
                score2-=1
                print(f"Score: Player_1={score1}, Player_2={score2}" )
        game_over()

    else:
        for i in range(len(shotBubble1_cy)):
            if shotBubble1_cx[i]+5 <= 800 and shot1_stat[i] in [0,1,2]:
                if shot1_stat[i]==0:
                    glColor3f(1,0,0)
                if shot1_stat[i]==1:
                    glColor3f(0,1,0)
                if shot1_stat[i]==2:
                    glColor3f(0,0,1)
                mid_circle(shotBubble1_cx[i], shotBubble1_cy[i], shotBubble_r)
        for i in range(len(shotBubble2_cy)):
            if shotBubble2_cx[i]+5 >= 0 and shot2_stat[i] in [0,1,2]:
                if shot2_stat[i]==0:
                    glColor3f(1,0,0)
                if shot2_stat[i]==1:
                    glColor3f(0,1,0)
                if shot2_stat[i]==2:
                    glColor3f(0,0,1)
                mid_circle(shotBubble2_cx[i], shotBubble2_cy[i], shotBubble_r)
            

def collision2():
    global shooter1_cx, shooter1_cy, shotBubble1_cx, shotBubble1_cy, shot1_stat, shot2_stat, shotBubble_r
    global shooter2_cx, shooter2_cy, shotBubble2_cx, shotBubble2_cy, shot2_stat
    global score1, score2, shooter1_mode
    global shooter1_shift, shooter2_shift, shooter_r, shooter_s
    c2x, c2y, r2= (
        shotBubble2_cx,
        shotBubble2_cy,
        shotBubble_r,
    )

    for j in range(len(c2x)):
        if shot2_stat[j] in [0, 1, 2]:
            sleft, sright = c2x[j] - r2, c2x[j] + r2
            sup, sdown = c2y[j] + r2, c2y[j] - r2

            shdown, shup = (
                shooter1_cy - shooter_s + shooter1_shift,
                shooter1_cy + shooter_s + shooter1_shift,
            )

            shright = shooter1_cx + shooter_r
            if shright >= sleft and shot2_stat[j] in [0,1,2]:
                if (shup >= sup and sup >= shdown) or (
                    shup >= sdown and sdown >= shdown
                    ):
                    if shooter1_mode==shot2_stat[j]:
                        score2 += 50
                        shot2_stat[j]=3
                        print(f"Score: Player_1={score1}, Player_2={score2}" )
                    else:
                        shot2_stat[j]=3

def collision1():
    global shooter1_cx, shooter1_cy, shotBubble1_cx, shotBubble1_cy, shot1_stat, shot2_stat, shotBubble_r
    global shooter2_cx, shooter2_cy, shotBubble2_cx, shotBubble2_cy, shot2_stat
    global score1, score2, shooter1_mode
    global shooter1_shift, shooter2_shift, shooter_r, shooter_s
    c2x, c2y, r2= (
        shotBubble1_cx,
        shotBubble1_cy,
        shotBubble_r,
    )

    for j in range(len(c2x)):
        if shot1_stat[j] in [0, 1, 2]:
            sleft, sright = c2x[j] - r2, c2x[j] + r2
            sup, sdown = c2y[j] + r2, c2y[j] - r2

            shdown, shup = (
                shooter2_cy - shooter_s + shooter2_shift,
                shooter2_cy + shooter_s + shooter2_shift,
            )

            shleft = shooter2_cx - shooter_r
            if shleft <= sright and shot1_stat[j] in [0,1,2]:
                if (shup >= sup and sup >= shdown) or (
                    shup >= sdown and sdown >= shdown
                    ):
                    if shooter2_mode==shot1_stat[j]:
                        score1 += 50
                        shot1_stat[j]=3
                        print(f"Score: Player_1={score1}, Player_2={score2}" )
                    else:
                        shot1_stat[j]=3

def mouselistener(button, state, x, y):
    global height, width, pause, score1, score2, dead

    nx = x
    ny = height - y

    if button == GLUT_LEFT_BUTTON:
        if state == GLUT_DOWN:
            # setting pause
            if nx > 390 and nx < 420 and ny > 650 and ny < 690:
                if dead==False:
                    pause = not pause
                if pause == False:
                    print("Game Resumed")
                else:
                    print("Game Paused")
            # setting reset
            elif nx > 5 and nx < 60 and ny >650 and ny < 690:
                print(f"Score: Player_1={score1}, Player_2={score2}" )
                print("Starting Over! New Game.")
                re_start()
            # setting cross
            elif nx > 760 and nx < 790 and ny > 650 and ny < 690:
                print(f"Score: Player_1={score1}, Player_2={score2}" )
                print("Goodbye!")
                glutDestroyWindow(shooter2p)

def re_start():
    global pause, score1, score2, shooter1_shift, shooter2_shift, shotBubble1_cx, shotBubble1_cy, shot1_stat, shotBubble2_cx, shotBubble2_cy, shot2_stat
    pause= False

    score1, score2 = 0, 0
    shotBubble1_cx, shotBubble1_cy, shot1_stat = [], [], []
    shotBubble2_cx, shotBubble2_cy, shot2_stat = [], [], []
    shooter1_shift, shooter2_shift = 0, 0

def game_over():
    global score1, score2, pause, dead
    if score1 >= 100:
        print("Game Over. Player 1 Wins!!!")
        dead=True
        pause = True
    elif score2 >= 100:
        print("Game Over. Player 2 Wins!!!")
        dead=True
        pause = True
    elif score1 < 0:
        print("Game Over. Player 2 Wins!!!")
        dead=True
        pause = True
    elif score2 < 0:
        print("Game Over. Player 1 Wins!!!")
        dead=True
        pause = True
    

glutInit()
glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
glutInitWindowSize(width, height)
shooter2p = glutCreateWindow(b"Space Shooter - 2P")
init()
shooter_mode()
glutDisplayFunc(display)
glutIdleFunc(animate)
glutKeyboardFunc(keyboard)
glutKeyboardUpFunc(keyboard_up)
glutSpecialFunc(special_keyboard)
glutSpecialUpFunc(special_keyboard_up)
glutIdleFunc(update_game)
glutMouseFunc(mouselistener)
glEnable(GL_DEPTH_TEST)
glutMainLoop()