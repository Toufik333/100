from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random

points = []  # Will store (x, y, color_r, color_g, color_b, dx, dy)
point_size = 7.0
is_frozen = False
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
    global points
    
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