from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import math
import random

# Camera-related variables
camera_pos = (0, -500, 200)  # Positioned behind and above the player

fovY = 90  # Field of view
ROAD_LENGTH = 40000  # Length of the road
ROAD_WIDTH = 300  # Width of the road

# Human (player) params
human_x = 0
human_y = -ROAD_LENGTH/2 + 200  # Start near the beginning of the road
human_z = 0
human_rotation = 0

# Environment objects
trees = []
buildings = []

# Initialize environment objects
def init_environment():
    global trees, buildings
    
    # Create trees on both sides of the road
    for i in range(-ROAD_LENGTH//2, ROAD_LENGTH//2, 200):  # Trees along the road
        # Left side trees
        trees.append({
            'pos': [-ROAD_WIDTH/2 - 100, i, 0],
            'height': random.randint(100, 150),
            'trunk_radius': random.randint(5, 10),
            'crown_radius': random.randint(30, 50)
        })
        
        # Right side trees
        trees.append({
            'pos': [ROAD_WIDTH/2 + 100, i, 0],
            'height': random.randint(100, 150),
            'trunk_radius': random.randint(5, 10),
            'crown_radius': random.randint(30, 50)
        })
    
    # Create buildings (boxes) on both sides of the road
    for i in range(-ROAD_LENGTH//2, ROAD_LENGTH//2, 400):  # Buildings along the road
        # Left side buildings
        buildings.append({
            'pos': [-ROAD_WIDTH/2 - 250, i, 0],
            'width': random.randint(100, 150),
            'depth': random.randint(100, 150),
            'height': random.randint(150, 300),
            'color': [random.uniform(0.5, 0.9), random.uniform(0.5, 0.9), random.uniform(0.5, 0.9)]
        })
        
        # Right side buildings
        buildings.append({
            'pos': [ROAD_WIDTH/2 + 250, i, 0],
            'width': random.randint(100, 150),
            'depth': random.randint(100, 150),
            'height': random.randint(150, 300),
            'color': [random.uniform(0.5, 0.9), random.uniform(0.5, 0.9), random.uniform(0.5, 0.9)]
        })

# Draw a tree with trunk and crown
def draw_tree(x, y, z, trunk_height, trunk_radius, crown_radius):
    # Draw trunk (brown cylinder)
    glPushMatrix()
    glColor3f(0.55, 0.27, 0.07)  # Brown color
    glTranslatef(x, y, z)
    glRotatef(0, 1, 0, 0)  # Rotate to align with z-axis
    gluCylinder(gluNewQuadric(), trunk_radius, trunk_radius, trunk_height, 10, 10)
    glPopMatrix()
    
    # Draw crown (green sphere)
    glPushMatrix()
    glColor3f(0.0, 0.5, 0.0)  # Green color
    glTranslatef(x, y, z + trunk_height)
    gluSphere(gluNewQuadric(), crown_radius, 10, 10)
    glPopMatrix()

# Draw a building (box)
def draw_building(x, y, z, width, depth, height, color):
    glPushMatrix()
    glColor3f(color[0], color[1], color[2])
    glTranslatef(x, y, z + height/2)  # Center at the bottom of the building
    draw_rectangular_cuboid(width, depth, height)
    glPopMatrix()

def draw_text(x, y, text, font=GLUT_BITMAP_HELVETICA_18):
    glColor3f(1, 1, 1)
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    
    # Set up an orthographic projection that matches window coordinates
    gluOrtho2D(0, 1000, 0, 800)  # left, right, bottom, top
    
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()
    
    # Draw text at (x, y) in screen coordinates
    glRasterPos2f(x, y)
    for ch in text:
        glutBitmapCharacter(font, ord(ch))
    
    # Restore original projection and modelview matrices
    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)

def draw_human(x=0, y=0, z=0, rotation=90):
    glPushMatrix()  # Save the current matrix state

    # Move the whole figure to (x, y, z)
    glTranslatef(x, y, z)
    # Apply rotation around the Z axis (vertical axis)
    glRotatef(rotation, 0, 0, 1)
    # Scale down the whole figure by 1/3
    glScalef(1/3, 1/3, 1/3)

    # Draw left leg
    glPushMatrix()
    glColor3f(1, 0, 0)
    glTranslatef(50, 0, 0)
    gluCylinder(gluNewQuadric(), 15, 40, 150, 10, 10)
    glPopMatrix()

    # Draw right leg
    glPushMatrix()
    glColor3f(1, 0, 0)
    glTranslatef(-50, 0, 0)
    gluCylinder(gluNewQuadric(), 15, 40, 150, 10, 10)
    glPopMatrix()

    # Draw torso
    glPushMatrix()
    glColor3f(0, 1, 0)
    glTranslatef(0, 0, 200)
    draw_rectangular_cuboid(200, 50, 180)
    glPopMatrix()

    # Draw head
    glPushMatrix()
    glColor3f(0, 0, 1)
    glTranslatef(0, 0, 325)
    gluSphere(gluNewQuadric(), 50, 10, 10)
    glPopMatrix()
    
    # Draw arms
    # Left arm
    glPushMatrix()
    glColor3f(1, 0.5, 0)
    glTranslatef(120, 0, 250)
    glRotatef(-90, 1, 0, 0)
    gluCylinder(gluNewQuadric(), 5, 20, 120, 10, 10)
    glPopMatrix()

    # Right arm
    glPushMatrix()
    glColor3f(1, 0.5, 0)
    glTranslatef(-120, 0, 250)
    glRotatef(-90, 1, 0, 0)
    gluCylinder(gluNewQuadric(), 5, 20, 120, 10, 10)
    glPopMatrix()
    
    # Draw a cylinder in the middle of the torso if needed
    # glPushMatrix()
    # glColor3f(0.5, 0.2, 0.8)
    # glTranslatef(0, 0, 200)  # Move to the center of the torso
    # glRotatef(-90, 1, 0, 0)   # Align cylinder vertically
    # gluCylinder(gluNewQuadric(), 20, 20, 100, 20, 20)
    # glPopMatrix()

    glPopMatrix()  # Restore the original matrix state

def draw_rectangular_cuboid(width, height, depth):
    """
    Draw a rectangular cuboid with specified width, height, and depth.
    Origin is at the center of the cuboid.
    """
    # Calculate half dimensions
    half_width = width / 2
    half_height = height / 2
    half_depth = depth / 2
    
    # Front face
    glBegin(GL_QUADS)
    glVertex3f(-half_width, -half_height, half_depth)  # Bottom left
    glVertex3f(half_width, -half_height, half_depth)   # Bottom right
    glVertex3f(half_width, half_height, half_depth)    # Top right
    glVertex3f(-half_width, half_height, half_depth)   # Top left
    glEnd()
    
    # Back face
    glBegin(GL_QUADS)
    glVertex3f(-half_width, -half_height, -half_depth) # Bottom left
    glVertex3f(half_width, -half_height, -half_depth)  # Bottom right
    glVertex3f(half_width, half_height, -half_depth)   # Top right
    glVertex3f(-half_width, half_height, -half_depth)  # Top left
    glEnd()
    
    # Top face
    glBegin(GL_QUADS)
    glVertex3f(-half_width, half_height, half_depth)   # Front left
    glVertex3f(half_width, half_height, half_depth)    # Front right
    glVertex3f(half_width, half_height, -half_depth)   # Back right
    glVertex3f(-half_width, half_height, -half_depth)  # Back left
    glEnd()
    
    # Bottom face
    glBegin(GL_QUADS)
    glVertex3f(-half_width, -half_height, half_depth)  # Front left
    glVertex3f(half_width, -half_height, half_depth)   # Front right
    glVertex3f(half_width, -half_height, -half_depth)  # Back right
    glVertex3f(-half_width, -half_height, -half_depth) # Back left
    glEnd()
    
    # Right face
    glBegin(GL_QUADS)
    glVertex3f(half_width, -half_height, half_depth)   # Bottom front
    glVertex3f(half_width, -half_height, -half_depth)  # Bottom back
    glVertex3f(half_width, half_height, -half_depth)   # Top back
    glVertex3f(half_width, half_height, half_depth)    # Top front
    glEnd()
    
    # Left face
    glBegin(GL_QUADS)
    glVertex3f(-half_width, -half_height, half_depth)  # Bottom front
    glVertex3f(-half_width, -half_height, -half_depth) # Bottom back
    glVertex3f(-half_width, half_height, -half_depth)  # Top back
    glVertex3f(-half_width, half_height, half_depth)   # Top front
    glEnd()

def keyboardListener(key, x, y):
    """
    Handles keyboard inputs for player movement.
    """
    global human_x, human_y
    
    # Move forward (W key)
    if key == b'w': 
        human_y += 10  # Move forward along the road
        if human_y > ROAD_LENGTH/2 - 100:  # Prevent going past the end
            human_y = ROAD_LENGTH/2 - 100
    
    # Move backward (S key)
    if key == b's':
        human_y -= 10  # Move backward along the road
        if human_y < -ROAD_LENGTH/2 + 100:  # Prevent going past the start
            human_y = -ROAD_LENGTH/2 + 100
    
    # Move left (A key)
    if key == b'a': 
        human_x -= 10
        if human_x < -ROAD_WIDTH/2 + 50:  # Keep player within left boundary
            human_x = -ROAD_WIDTH/2 + 50
    
    # Move right (D key)
    if key == b'd':
        human_x += 10
        if human_x > ROAD_WIDTH/2 - 50:  # Keep player within right boundary
            human_x = ROAD_WIDTH/2 - 50

def specialKeyListener(key, x, y):
    """
    Handles special key inputs (arrow keys) for adjusting the camera angle and height.
    """
    global camera_pos
    x, y, z = camera_pos
    # Move camera up (UP arrow key)
    if key == GLUT_KEY_UP:
        z += 10

    # Move camera down (DOWN arrow key)
    if key == GLUT_KEY_DOWN:
        z -= 10

    # Moving camera left (LEFT arrow key)
    if key == GLUT_KEY_LEFT:
        x -= 10

    # Moving camera right (RIGHT arrow key)
    if key == GLUT_KEY_RIGHT:
        x += 10

    camera_pos = (x, y, z)

def mouseListener(button, state, x, y):
    """
    Handles mouse inputs.
    """
    pass  # No mouse functionality required for now

def setupCamera():
    """
    Configures the camera's projection and view settings.
    Uses a perspective projection and positions the camera to look at the player.
    """
    glMatrixMode(GL_PROJECTION)  # Switch to projection matrix mode
    glLoadIdentity()  # Reset the projection matrix
    
    # Set up a perspective projection (field of view, aspect ratio, near clip, far clip)
    gluPerspective(fovY, 1.25, 0.1, 5000)
    
    glMatrixMode(GL_MODELVIEW)  # Switch to model-view matrix mode
    glLoadIdentity()  # Reset the model-view matrix

    # Position the camera and set its orientation to follow the player
    gluLookAt(
        human_x + camera_pos[0], human_y + camera_pos[1], human_z + camera_pos[2],  # Camera position
        human_x, human_y + 300, human_z + 50,  # Look-at target (ahead of player)
        0, 0, 1  # Up vector (z-axis)
    )

def idle():
    """
    Idle function that runs continuously.
    """
    # Ensure the screen updates with the latest changes
    glutPostRedisplay()

def draw_road():
    """
    Draw a long static road with lane markings.
    """
    # Draw the road surface
    glColor3f(0.2, 0.2, 0.2)  # Dark gray for asphalt
    glBegin(GL_QUADS)
    glVertex3f(-ROAD_WIDTH/2, -ROAD_LENGTH/2, 0)
    glVertex3f(ROAD_WIDTH/2, -ROAD_LENGTH/2, 0)
    glVertex3f(ROAD_WIDTH/2, ROAD_LENGTH/2, 0)
    glVertex3f(-ROAD_WIDTH/2, ROAD_LENGTH/2, 0)
    glEnd()
    
    # Draw road markings (white dashed lines)
    glColor3f(1, 1, 1)  # White for lane markings
    
    # Calculate how many lines to draw based on the road length
    num_lines = int(ROAD_LENGTH / 50)  # One line every 50 units
    
    # Draw the center line
    for i in range(num_lines):
        line_pos = -ROAD_LENGTH/2 + i * 50
        if i % 2 == 0:  # Draw dashed lines
            glBegin(GL_QUADS)
            glVertex3f(-5, line_pos, 1)
            glVertex3f(5, line_pos, 1)
            glVertex3f(5, line_pos + 30, 1)
            glVertex3f(-5, line_pos + 30, 1)
            glEnd()
    
    # Draw the side lines (continuous)
    glBegin(GL_QUADS)
    # Left side
    glVertex3f(-ROAD_WIDTH/2, -ROAD_LENGTH/2, 1)
    glVertex3f(-ROAD_WIDTH/2 + 5, -ROAD_LENGTH/2, 1)
    glVertex3f(-ROAD_WIDTH/2 + 5, ROAD_LENGTH/2, 1)
    glVertex3f(-ROAD_WIDTH/2, ROAD_LENGTH/2, 1)
    # Right side
    glVertex3f(ROAD_WIDTH/2 - 5, -ROAD_LENGTH/2, 1)
    glVertex3f(ROAD_WIDTH/2, -ROAD_LENGTH/2, 1)
    glVertex3f(ROAD_WIDTH/2, ROAD_LENGTH/2, 1)
    glVertex3f(ROAD_WIDTH/2 - 5, ROAD_LENGTH/2, 1)
    glEnd()
    
    # Draw lane dividers (create 3 lanes)
    lane_width = ROAD_WIDTH / 3
    
    # First lane divider
    for i in range(num_lines):
        line_pos = -ROAD_LENGTH/2 + i * 50
        if i % 2 == 0:  # Draw dashed lines
            glBegin(GL_QUADS)
            glVertex3f(-lane_width/2 - 2.5, line_pos, 1)
            glVertex3f(-lane_width/2 + 2.5, line_pos, 1)
            glVertex3f(-lane_width/2 + 2.5, line_pos + 30, 1)
            glVertex3f(-lane_width/2 - 2.5, line_pos + 30, 1)
            glEnd()
    
    # Second lane divider
    for i in range(num_lines):
        line_pos = -ROAD_LENGTH/2 + i * 50
        if i % 2 == 0:  # Draw dashed lines
            glBegin(GL_QUADS)
            glVertex3f(lane_width/2 - 2.5, line_pos, 1)
            glVertex3f(lane_width/2 + 2.5, line_pos, 1)
            glVertex3f(lane_width/2 + 2.5, line_pos + 30, 1)
            glVertex3f(lane_width/2 - 2.5, line_pos + 30, 1)
            glEnd()
    
    # Draw start line
    glColor3f(1, 1, 0)  # Yellow color
    glBegin(GL_QUADS)
    glVertex3f(-ROAD_WIDTH/2, -ROAD_LENGTH/2 + 100, 1)
    glVertex3f(ROAD_WIDTH/2, -ROAD_LENGTH/2 + 100, 1)
    glVertex3f(ROAD_WIDTH/2, -ROAD_LENGTH/2 + 110, 1)
    glVertex3f(-ROAD_WIDTH/2, -ROAD_LENGTH/2 + 110, 1)
    glEnd()
    
    # Draw finish line
    glColor3f(1, 0, 0)  # Red color
    glBegin(GL_QUADS)
    glVertex3f(-ROAD_WIDTH/2, ROAD_LENGTH/2 - 100, 1)
    glVertex3f(ROAD_WIDTH/2, ROAD_LENGTH/2 - 100, 1)
    glVertex3f(ROAD_WIDTH/2, ROAD_LENGTH/2 - 90, 1)
    glVertex3f(-ROAD_WIDTH/2, ROAD_LENGTH/2 - 90, 1)
    glEnd()

def draw_environment():
    """
    Draw all environment objects (trees, buildings).
    """
    global trees, buildings
    
    # Draw all trees
    for tree in trees:
        draw_tree(tree['pos'][0], tree['pos'][1], tree['pos'][2], 
                 tree['height'], tree['trunk_radius'], tree['crown_radius'])
    
    # Draw all buildings
    for building in buildings:
        draw_building(building['pos'][0], building['pos'][1], building['pos'][2],
                     building['width'], building['depth'], building['height'], 
                     building['color'])

def draw_game_info():
    """
    Draw game information on screen.
    """
    draw_text(10, 770, f"Position: ({human_x:.1f}, {human_y:.1f})")
    draw_text(10, 740, f"Use W,A,S,D to move")
    draw_text(10, 710, f"Arrow keys to adjust camera")

def showScreen():
    """
    Display function to render the game scene.
    """
    # Set clear color to white
    glClearColor(0, 1.0, 1.0, 1.0)
    # Clear color and depth buffers
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()  # Reset modelview matrix
    glViewport(0, 0, 1000, 800)  # Set viewport size

    setupCamera()  # Configure camera perspective

    # Draw the road
    draw_road()
    
    # Draw environment objects
    draw_environment()
    
    # Draw the player
    draw_human(human_x, human_y, human_z, human_rotation)
    
    # Draw game information
    draw_game_info()

    # Swap buffers for smooth rendering (double buffering)
    glutSwapBuffers()

# Main function to set up OpenGL window and loop
def main():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)  # Double buffering, RGB color, depth test
    glutInitWindowSize(1000, 800)  # Window size
    glutInitWindowPosition(0, 0)  # Window position
    wind = glutCreateWindow(b"3D Dodge the Obstacles")  # Create the window

    # Enable depth testing
    glEnable(GL_DEPTH_TEST)
    
    # Initialize environment
    init_environment()
    
    glutDisplayFunc(showScreen)  # Register display function
    glutKeyboardFunc(keyboardListener)  # Register keyboard listener
    glutSpecialFunc(specialKeyListener)
    glutMouseFunc(mouseListener)
    glutIdleFunc(idle)  # Register the idle function

    glutMainLoop()  # Enter the GLUT main loop

if __name__ == "__main__":
    main()