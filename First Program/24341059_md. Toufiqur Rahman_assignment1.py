'''
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random
import math

is_day = True
rain_direction_angle = 0.0
rain_density = 250
raindrops = []
is_raining = False  # Toggle for rain on/off

def init_raindrops():
    global raindrops
    raindrops = [(random.uniform(0, 500), random.uniform(0, 500)) for i in range(rain_density)]



def draw_points(x, y,colour=(0,0,0)):
    glColor3f(*colour)
    glPointSize(5) #pixel size. by default 1 thake
    glBegin(GL_POINTS)
    glVertex2f(x,y) #jekhane show korbe pixel
    glEnd()
    
def drawquadsWithTriangles(a,b,c,d,colour): 
    glColor3f(*colour)
    glBegin(GL_TRIANGLES)
    glVertex2f(a, b)
    glVertex2f(c, b)
    glVertex2f(a, d)
    glEnd()

    glBegin(GL_TRIANGLES)
    glVertex2f(c, b)
    glVertex2f(c, d)
    glVertex2f(a, d)
    glEnd()
def drawWindow(a,b,c,d,colour):
    drawquadsWithTriangles(a,b,c,d,colour)
    drawLine((a+c)/2, b, (a+c)/2, d, (0,0,0))
    drawLine(a, (b+d)/2, c, (b+d)/2, (0,0,0))
def drawDoor(a,b,c,d,colour):
    drawquadsWithTriangles(a,b,c,d,colour)
    draw_points((a+c)/2, b)
    

def drawbackground(a,b,c,d,day=True):
    if day:
        drawquadsWithTriangles(a,b,c,d, (255/255, 230/255, 161/255))
    else:
        drawquadsWithTriangles(a,b,c,d, (54/255, 50/255, 42/255))
    
    
    
def drawTriangle(a, b, c, d, e, f,colour): #a,b = 1st point, c,d = 2nd point, e,f = 3rd point, colour = colour of the triangle touple
    glColor3f(*colour)
    glBegin(GL_TRIANGLES)
    glVertex2f(a, b)
    glVertex2f(c, d)
    glVertex2f(e, f)
    glEnd()

def drawLine(a, b, c, d ,colour): #a,b = 1st point, c,d = 2nd point colour = colour of the line touple
    glColor3f(*colour)
    glBegin(GL_LINES)
    glVertex2f(a, b)
    glVertex2f(c, d)
    glEnd()
    
    
def drawRain():
    global raindrops
    #print(raindrops)
    glColor3f(0.6, 0.7, 0.9)  # Light blue for day
    
    glPointSize(1.5)  # Raindrop size
    glBegin(GL_LINES)
    for drop in raindrops:
        glVertex2f(drop[0], drop[1])
        glVertex2f(drop[0]+ 2 * math.sin(rain_direction_angle), drop[1] - 10.0)  # Adjusted for direction
    glEnd()

def iterate():
    glViewport(0, 0, 500, 500)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0.0, 500, 0.0, 500, 0.0, 1.0)
    glMatrixMode (GL_MODELVIEW)
    glLoadIdentity()

def showScreen():
    global is_day
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    iterate()
    glColor3f(1.0, 1.0, 0.0) #konokichur color set (RGB)
    #call the draw methods here
    drawbackground(0,500,500,0, is_day) #day
    if is_day:
        drawquadsWithTriangles(0,300,500,0, (252/255, 186/255, 3/255))
    else:
        drawquadsWithTriangles(0,300,500,0, (200/255, 140/255, 2/255))
    for i in range(10):
        shift = 50*i
        a,b,c,d,e,f = 5+shift ,280 ,10+shift ,340, 20+shift ,280
        drawTriangle(a,b,c,d,e,f, (113/255, 156/255, 39/255))
        #drawTriangle(5,280, 10,310, 15,280, (0, 0, 0))
    
    drawTriangle(250, 350, 150, 275, 350, 275, (139/255, 69/255, 19/255))  
    drawquadsWithTriangles(160,275,340,230, (242/255, 242/255, 242/255))
    drawWindow(170, 265, 190, 245, (42/255, 93/255, 120/255))
    drawWindow(300, 265, 320, 245, (42/255, 93/255, 120/255))
    drawDoor(230, 260, 270, 230, (42/255, 93/255, 120/255))
    if is_day:
        drawquadsWithTriangles(50,350,150,450, (0.9, 0.3, 0.2)) 
    else:
        drawquadsWithTriangles(50,350,150,450, (242/255, 242/255, 242/255))
    
    if is_raining:
        drawRain()
    
    
    glutSwapBuffers()
    
    
def rain_animation(value):
    global raindrops, rain_direction_angle
    
    if is_raining:
        new_drops = []
        for (x, y) in raindrops:
            new_x = x + math.sin(rain_direction_angle) * 2.0
            new_y = y - 7.0  # Rain falls downward
            
            if new_y < 0:
                new_y = 500
                new_x = random.uniform(0, 500)
            if new_x < 0 or x > 500:
                new_x = random.uniform(0, 500)
                
            new_drops.append((new_x, new_y))
        raindrops = new_drops
        glutPostRedisplay()
    
    glutTimerFunc(16, rain_animation, 0)  # ~60 FPS
    
    
def keyboard(key, x, y):
    global is_day, is_raining, rain_density
    
    if key == b'\x1b':
        print("ESC pressed: Exiting program.")
        glutLeaveMainLoop() 
    elif key == b'd':
        is_day = True
        print("Day mode activated")
    elif key == b'n':
        is_day = False
        print("Night mode activated")
    elif key == b'r':
        is_raining = not is_raining
        if is_raining:
            print("Rain started")
            init_raindrops()  
        else:
            print("Rain stopped")
    
    glutPostRedisplay() 

def special_input(key, x, y):
    global rain_direction_angle, rain_density
    
    if key == GLUT_KEY_LEFT:  # Left arrow
        rain_direction_angle -= 0.1
        print(f"Rain direction: {rain_direction_angle:.2f}")
    elif key == GLUT_KEY_RIGHT:  # Right arrow
        rain_direction_angle += 0.1
        print(f"Rain direction: {rain_direction_angle:.2f}")
    elif key == GLUT_KEY_UP:  # Up arrow - increase rain density
        if rain_density < 500:
            rain_density += 50
            init_raindrops()
            print(f"Rain density: {rain_density}")
    elif key == GLUT_KEY_DOWN:  # Down arrow - decrease rain density
        if rain_density > 50:
            rain_density -= 50
            init_raindrops()
            print(f"Rain density: {rain_density}")
    
    glutPostRedisplay()

glutInit()
glutInitDisplayMode(GLUT_RGBA)
glutInitWindowSize(500, 500) #window size
glutInitWindowPosition(0, 0)
wind = glutCreateWindow(b"OpenGL Coding Practice") #window name
glutDisplayFunc(showScreen)
glutKeyboardFunc(keyboard)
glutSpecialFunc(special_input)
init_raindrops()  # Initialize raindrops
glutTimerFunc(16, rain_animation, 0)  # Start animation timer

glutMainLoop()

'''

#task2
'''     ..............................................................................           '''


from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random

points = []  # Will store (x, y, color_r, color_g, color_b, dx, dy)
point_size = 7.0
is_frozen = False
is_blinking = False
last_blink_time = 0
blink_interval = 0.5  # Half a second for complete blink cycle
base_speed = 1.0
speed_multiplier = 1.0

def random_color():
  r = random.uniform(0.0, 1.0)
  g = random.uniform(0.0, 1.0)
  b = random.uniform(0.0, 1.0)
  return (r, g, b)

def create_point(x, y):
    # Generate random color
    r, g, b = random_color()
    
    # Random diagonal direction
    dx = random.choice([-1, 1]) * random.uniform(0.5, 1.0)
    dy = random.choice([-1, 1]) * random.uniform(0.5, 1.0)
    
    # Add to points list
    points.append([x, y, r, g, b, dx, dy])
    



def iterate():
    glViewport(0, 0, 500, 500)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0.0, 500, 0.0, 500, 0.0, 1.0)
    glMatrixMode (GL_MODELVIEW)
    glLoadIdentity()
    
    
def update_points():
    global points
    
    if is_frozen:
        return
    
    for point in points:
        # Update position with current speed
        point[0] += point[5] * speed_multiplier
        point[1] += point[6] * speed_multiplier
        
        # Bounce off walls
        if point[0] <= 0 or point[0] >= 500:
            point[5] = -point[5]  # Reverse x direction
            
        if point[1] <= 0 or point[1] >= 500:
            point[6] = -point[6]  # Reverse y direction
            
            

def showScreen():
    global points, is_blinking, last_blink_time
    
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    iterate()
    
    

    glPointSize(point_size)
    for point in points:
        glColor3f(point[2], point[3], point[4])  # Use point's color
        glBegin(GL_POINTS)
        glVertex2f(point[0], point[1])
        glEnd()
    
    glutSwapBuffers()

def mouse(button, state, x, y):
    
    # Don't process input if frozen
    if is_frozen:
        return
    
    # Convert y coordinate (OpenGL origin is bottom-left)
    y = 500 - y
    
    if state == GLUT_DOWN:
        if button == GLUT_RIGHT_BUTTON:
            # Right-click to spawn a new point
            create_point(x, y)
            print(f"New point created at ({x}, {y})")
            
        
            
def keyboard(key, x, y):
    global is_frozen
    
    if key == b' ': 
        is_frozen = not is_frozen
        print(f"Animation {'frozen' if is_frozen else 'unfrozen'}")
        
def special_keys(key, x, y):
    global speed_multiplier
    
    # Don't process input if frozen
    if is_frozen:
        return
    
    if key == GLUT_KEY_UP:
        # Increase speed
        speed_multiplier += 0.1
        print(f"Speed increased to {speed_multiplier:.1f}x")
        
    elif key == GLUT_KEY_DOWN:
        # Decrease speed, but don't go below 0.1
        if speed_multiplier > 0.1:
            speed_multiplier -= 0.1
            print(f"Speed decreased to {speed_multiplier:.1f}x")
            
def timer(value):
    update_points()
    glutPostRedisplay()
    glutTimerFunc(16, timer, 0)  # ~60 FPS

glutInit()
glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGBA)
glutInitWindowSize(500, 500)
glutInitWindowPosition(0, 0)
glutCreateWindow(b"Interactive Bouncing Points")

# Set background color to black
glClearColor(0.0, 0.0, 0.0, 1.0)

# Register callbacks
glutDisplayFunc(showScreen)
glutMouseFunc(mouse)
glutKeyboardFunc(keyboard)
glutSpecialFunc(special_keys)
glutTimerFunc(16, timer, 0)  # Start animation timer

glutMainLoop()

