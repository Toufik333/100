from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random

score = 0
diamond_speed = 0.8
frameWidth=500
frameHeight=700
diamond_x = random.randint(-240, 240)
diamond_y = 200
diamond_width = 20
diamond_height = 30
color = (random.random(), random.random(), random.random())
end_game = False
stopGame = False
catcher_x = 20
catcher_y = 30
catcher_width = 120
catcher_height=0

def draw_points(x, y):
    glPointSize(2) #pixel size. by default 1 thake
    glBegin(GL_POINTS)
    glVertex2f(x,y) #jekhane show korbe pixel
    glEnd()
    

def DrawLine(x1, y1, x2, y2):
    zone =FindZone(x1, y1, x2, y2)
    x1, y1, x2, y2 = convert_to_zero(zone, x1, y1, x2, y2)
    points = midpointAlgo(x1, y1, x2, y2)
    convertBack(zone, points)

def convert_to_zero(zone, x1, y1, x2, y2):
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

def FindZone(x1, y1, x2, y2):
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

def convertBack(zone, points):
    if zone == 0:
        for x, y in points:
            draw_points(x, y)
    elif zone == 1:
        for x, y in points:
            draw_points(y, x)
    elif zone == 2:
        for x, y in points:
            draw_points(-y, x)
    elif zone == 3:
        for x, y in points:
            draw_points(-x, y)
    elif zone == 4:
        for x, y in points:
            draw_points(-x, -y)
    elif zone == 5:
        for x, y in points:
            draw_points(-y, -x)
    elif zone == 6:
        for x, y in points:
            draw_points(y, -x)
    elif zone == 7:
        for x, y in points:
            draw_points(x, -y)
            
            
            
def diamond_draw(x, y, diamondW, diamondH):
    DrawLine(x, y, x + diamondW // 2, y - diamondH) 
    DrawLine(x + diamondW // 2, y - diamondH, x + diamondW, y) 
    DrawLine(x, y, x + diamondW // 2, y + diamondH)  
    DrawLine(x + diamondW // 2, y + diamondH, x + diamondW, y)  


def iterate():
    glViewport(0, 0, frameWidth, frameHeight)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(-frameWidth // 2, frameWidth // 2, -frameHeight // 2, frameHeight // 2, 0.0, 1.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

def showScreen():
    global diamond_x, diamond_y, diamond_width, diamond_height, color, end_game,catcher_x, catcher_y, catcher_width, catcher_height
    
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    iterate() 
    glColor3f(1.0, 1.0, 0.0) 
    
    glColor3f(0.82, 0.93, 0.53)
    if stopGame:
        DrawLine(-13, 265, 13, 275)
        DrawLine(13, 275, -13, 280)
        DrawLine(-13, 280, -13, 265)
    else:
        DrawLine(-4, 265, -4, 285)
        DrawLine(4, 265, 4, 285)

    #restart
    glColor3f(0.26, 0.77, 0.89)
    DrawLine(-240, 275, -230, 285)
    DrawLine(-240, 275, -230, 265)
    DrawLine(-240, 275, -215, 275)

    #exit
    glColor3f(0.88, 0.21, 0.21)
    DrawLine(240, 263, 220, 283)
    DrawLine(240, 283, 220, 262)
    
    glColor3f(1.0, 1.0, 1.0)  # Set line color to white
    DrawLine(-250, 250, 250, 250)  # Horizontal line
    
    glColor3f(*color) 
    diamond_draw(diamond_x, diamond_y, diamond_width, diamond_height)
    
    #CATCHER_DESIGN
    if end_game:
        glColor3f(1.0, 0.0, 0.0) 
         
    else:
        glColor3f(1.0, 1.0, 1.0) 
    DrawLine(catcher_x - 60, -335, catcher_x + 60, -335)
    DrawLine(catcher_x - 45, -350, catcher_x + 45, -350)
    DrawLine(catcher_x - 45, -350, catcher_x - 60, -335)
    DrawLine(catcher_x + 45, -350, catcher_x + 60, -335)
    glutSwapBuffers() 

def new_game(over=False):
    global diamond_x, diamond_y, catcher_x, score, diamond_speed, stopGame, color, end_game
    diamond_x = random.randint(-245, 245)
    diamond_y = 210
    catcher_x = 0
    if over:
        score=0
    diamond_speed = 0.8
    color = (random.random(), random.random(), random.random())
    end_game= False
    stopGame = False
    if over:
        end_game = True

def keyboard_listener(key, x, y):
    global catcher_x
    valset = 15
    if key == GLUT_KEY_LEFT:
        if catcher_x - 60 <= -245:  
            pass
        else:
            if not stopGame:
                catcher_x -= valset

    if key == GLUT_KEY_RIGHT:
        if catcher_x + 60 >= 245:  
            pass
        else:
            if not stopGame:
                catcher_x += valset

    glutPostRedisplay()
def new_diamond():
    global diamond_x, diamond_y, color ,diamond_speed
    diamond_x = random.randint(-240, 240)
    diamond_y = 200
    diamond_speed += 0.1
    color = (random.random(), random.random(), random.random())  
    glutPostRedisplay()
    
def mouse_listener(button, press, x, y):
    global catcher_x, catcher_y, diamond_x, diamond_y, stopGame, score
    if button == GLUT_LEFT_BUTTON and press == GLUT_DOWN:
        
        mouse_x = x - frameWidth // 2
        mouse_y = frameHeight // 2 - y
        
        #pause
        if -13 <= mouse_x <= 13 and 265 <= mouse_y <= 285:
            stopGame = not stopGame
            if stopGame:
                print("Paused!")
            else:
                print("Resumed!")              
        #restarts
        elif -240 <= mouse_x <= -215 and 265 <= mouse_y <= 285:
            print("Starting Over!")
            new_game(over=False)    
        #end
        elif 220 <= mouse_x <= 240 and 263 <= mouse_y <= 283:
            glutLeaveMainLoop()
            
def animate():
    global diamond_y, diamond_speed, score, end_game

    if not stopGame and not end_game:
        diamond_y -= diamond_speed  

        #collision check
        if (catcher_x - 60 <= diamond_x <= catcher_x + 60) and (diamond_y <= -305):
            score += 1
            print("Score:", score)
            new_diamond()  

        elif diamond_y <= -305: 
            print("GAME OVER..! \n Final Score:", score)
            end_game = True
            
            new_game(over=True)
            
            glColor3f(1.0, 1.0, 1.0)

    glutPostRedisplay()
    
glutInit()
glutInitDisplayMode(GLUT_RGBA)
glutInitWindowSize(frameWidth, frameHeight) 
glutInitWindowPosition(frameWidth, 0)
wind = glutCreateWindow(b"OpenGL Coding Practice") 
glutIdleFunc(animate)
glutDisplayFunc(showScreen)
glutSpecialFunc(keyboard_listener)
glutMouseFunc(mouse_listener)
glutMainLoop()