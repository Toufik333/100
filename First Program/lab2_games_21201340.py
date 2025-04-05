from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random
import time


frame_w = 500
frame_h = 600

diamond_speed = 0.1
catcher_x = 20
catcher_y = 30
catcher_width = 120
catcher_height=0
stopg = False
end_game = False
color = (random.random(), random.random(), random.random())
diamond_x = random.randint(-240, 240)
diamond_y = 200
diamond_width = 20
diamond_height = 30
score = 0
delta_time = 0.0
time_inc = time.time()


def points_draw(x, y):
    glPointSize(2)
    glBegin(GL_POINTS)
    glVertex2f(x, y)
    glEnd()


def dline(x1, y1, x2, y2):
    zone = locate(x1, y1, x2, y2)
    x1, y1, x2, y2 = all_zero_convert(zone, x1, y1, x2, y2)
    points = midpointAlgo(x1, y1, x2, y2)
    main_zone_convert(zone, points)


def midpointAlgo(x1, y1, x2, y2):
    points = []
    dx = x2 - x1
    dy = y2 - y1
    del_d = 2 * dy - dx
    North_E = 2 * (dy - dx)
    E = 2 * dy
    
    x = x1
    y = y1
    points.append([x, y])

    while x < x2:
        if del_d <= 0:
            del_d += E
        else:
            del_d += North_E
            y += 1
        x += 1
        points.append([x, y])
        

    return points
    


def locate(x1, y1, x2, y2):
    dx = x2 - x1
    dy = y2 - y1
    if dx > 0 and dy >= 0:
        if abs(dx) > abs(dy):
            return 0
        else:
            return 1
    elif dx <= 0 <= dy:
        if abs(dx) > abs(dy):
            return 3
        else:
            return 2
    elif dx < 0 and dy < 0:
        if abs(dx) > abs(dy):
            return 4
        else:
            return 5
    elif dx >= 0 > dy:
        if abs(dx) > abs(dy):
            return 7
        else:
            return 6


def all_zero_convert(zone, x1, y1, x2, y2):
    if zone == 1:
        x1, y1 = y1, x1
        x2, y2 = y2, x2
    elif zone == 2:
        x1, y1 = y1, -x1
        x2, y2 = y2, -x2
    elif zone == 3:
        x1, y1 = -x1, y1
        x2, y2 = -x2, y2
    elif zone == 4:
        x1, y1 = -x1, -y1
        x2, y2 = -x2, -y2
    elif zone == 5:
        x1, y1 = -y1, -x1
        x2, y2 = -y2, -x2
    elif zone == 6:
        x1, y1 = -y1, x1
        x2, y2 = -y2, x2
    elif zone == 7:
        x1, y1 = x1, -y1
        x2, y2 = x2, -y2
    return x1, y1, x2, y2


def main_zone_convert(zone, points):
    if zone == 0:
        for x, y in points:
            points_draw(x, y)
    elif zone == 1:
        for x, y in points:
            points_draw(y, x)
    elif zone == 2:
        for x, y in points:
            points_draw(-y, x)
    elif zone == 3:
        for x, y in points:
            points_draw(-x, y)
    elif zone == 4:
        for x, y in points:
            points_draw(-x, -y)
    elif zone == 5:
        for x, y in points:
            points_draw(-y, -x)
    elif zone == 6:
        for x, y in points:
            points_draw(y, -x)
    elif zone == 7:
        for x, y in points:
            points_draw(x, -y)


def diamond_draw(x, y, dwidth, dheight):
    dline(x, y, x + dwidth // 2, y - dheight)  # top edge 
    dline(x + dwidth // 2, y - dheight, x + dwidth, y)  # bottom edge
    dline(x, y, x + dwidth // 2, y + dheight)  # left edge
    dline(x + dwidth // 2, y + dheight, x + dwidth, y)  # right edge 


def display():
    global diamond_x, diamond_y, diamond_width, diamond_height, color, end_game

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glClearColor(0, 0, 0, 0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluLookAt(0, 0,200, 0, 0, 0, 0, 1, 0)
    glMatrixMode(GL_MODELVIEW)

    '''BUTTONS'''

    #PLAY-PAUSE BUTTON
    glColor3f(0.82, 0.93, 0.53)
    if stopg:
        dline(-13, 225, 13, 235)
        dline(13, 235, -13, 240)
        dline(-13, 240, -13, 225)
    else:
        dline(-4, 225, -4, 245)
        dline(4, 225, 4, 245)

    #RESTART BUTTON
    glColor3f(0.26, 0.77, 0.89)
    dline(-240, 235, -230, 245)
    dline(-240, 235, -230, 225)
    dline(-240, 235, -215, 235)

    #EXIT BUTTON
    glColor3f(0.88, 0.21, 0.21)
    dline(240, 223, 220, 243)
    dline(240, 243, 220, 222)

    #DIAMOND_DESIGN
    glColor3f(*color) #current color
    diamond_draw(diamond_x, diamond_y, diamond_width, diamond_height)

    #CATCHER_DESIGN
    global catcher_x, catcher_y, catcher_width, catcher_height

    if end_game:
        glColor3f(1.0, 0.0, 0.0) 
         
    else:
        glColor3f(1.0, 1.0, 1.0) 
    dline(catcher_x - 60, -235, catcher_x + 60, -235)
    dline(catcher_x - 45, -250, catcher_x + 45, -250)
    dline(catcher_x - 45, -250, catcher_x - 60, -235)
    dline(catcher_x + 45, -250, catcher_x + 60, -235)

    glutSwapBuffers()




def new_game(over=False):
    global diamond_x, diamond_y, catcher_x, score, diamond_speed, stopg, color, end_game
    diamond_x = random.randint(-245, 245)
    diamond_y = 210
    catcher_x = 0
    if over:
        score=0
    else:
        score=score
    diamond_speed = 0.01
    color = (random.random(), random.random(), random.random())
    end_game= True
    stopg = False
    if over:
        print("over")
        

def new_diamond():
    global diamond_x, diamond_y, color
    diamond_x = random.randint(-245, 245)
    diamond_y = 210
    
    color = (random.random(), random.random(), random.random())  
    glutPostRedisplay()


def keyboard_listener(key, x, y):
    global catcher_x
    valset = 25
    if key == GLUT_KEY_LEFT:
        if catcher_x - 60 <= -250:  # left boundary
            pass
        else:
            if not stopg:
                catcher_x -= valset

    if key == GLUT_KEY_RIGHT:
        if catcher_x + 60 >= 250:  # right boundary
            pass
        else:
            if not stopg:
                catcher_x += valset

    glutPostRedisplay()



def mouse_listener(button, press, x, y):
    global catcher_x, catcher_y, diamond_x, diamond_y, stopg
    if button == GLUT_LEFT_BUTTON and press == GLUT_DOWN:
        if 230 <= x <= 260 and 0 <= y <= 50:
            if stopg == False:
                stopg = True
                print("pause")
            elif stopg == True:
                stopg = False
                print("resume")
        elif 10 <= x <= 50 and 20 <= y <= 50:  
            print("Starting Over!")
           
            catcher_x = 0  
            catcher_y = 60  #resets catcher
            diamond_x = random.randint(-245, 245) 
            diamond_y = 120 
            stopg = False  #resume
            
        elif 445 <= x <= 490 and 10 <= y <= 50:
            glutLeaveMainLoop()

def animate():
    global diamond_y, diamond_speed, score, end_game

    if not stopg and not end_game:
        diamond_y -= diamond_speed  
        diamond_speed += 0.001 

        #collision check
        if (catcher_x - 60 <= diamond_x <= catcher_x + 60) and (diamond_y <= -245):
            score += 1
            print("Score:", score)
            new_diamond()  

        elif diamond_y <= -250: 
            print("Game Over! Final Score:", score)
            end_game = True
            new_game(over=True)
            glColor3f(1.0, 1.0, 1.0)

    glutPostRedisplay()

   
def init():
    glClearColor(0, 0, 0, 0)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(103, 1, 1, 1000.0)


glutInit()
glutInitWindowSize(frame_w, frame_h)
glutInitWindowPosition(500, 0)
glutInitDisplayMode(GLUT_DEPTH | GLUT_DOUBLE | GLUT_RGB)
frame = glutCreateWindow(b"Catch The Diamond")
init()
glutDisplayFunc(display)
glutIdleFunc(animate)
glutSpecialFunc(keyboard_listener)
glutMouseFunc(mouse_listener)
glutMainLoop()

