import random
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import math

# Camera-related variables
camera_pos = (0,100,500) 
bullets=[]
bullet_radius =10
fovY = 120  # Field of view
GRID_LENGTH = 600  # Length of grid lines
rand_var = 423
#human params
human_x = 0
human_y = 0
human_z = 0
human_rotation = 0
bullet_speed = 5
first_person_camera = False  # Flag for first-person camera mode
npc_max = 5
npc_data = []


def draw_text(x, y, text, font=GLUT_BITMAP_HELVETICA_18):
    glColor3f(1,1,1)
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



def draw_bullet(bullet):
    """
    Draw a single bullet as a black sphere
    """
    glPushMatrix()
    glColor3f(0, 0, 0)  # Black color
    glTranslatef(bullet['pos'][0], bullet['pos'][1], bullet['pos'][2])
    gluSphere(gluNewQuadric(), bullet['radius'], 10, 10)
    glPopMatrix()

def update_bullets():

    global bullets
    bullets_to_remove = []
    
    for i, bullet in enumerate(bullets):
        # Update bullet position based on direction and speed
        bullet['pos'][0] += bullet['dir'][0] * bullet_speed
        bullet['pos'][1] += bullet['dir'][1] * bullet_speed
        bullet['pos'][2] += bullet['dir'][2] * bullet_speed
        
        # Check collision with walls (considering bullet radius)
        x, y, z = bullet['pos']
        radius = bullet['radius']
        
        # Check if bullet hits any wall
        if (x + radius >= GRID_LENGTH or x - radius <= -GRID_LENGTH or
            y + radius >= GRID_LENGTH or y - radius <= -GRID_LENGTH or
            z - radius <= 0 or z + radius >= 200):  # 200 is wall height
            bullets_to_remove.append(i)
    
    # Remove bullets that hit walls (reverse order to maintain indices)
    for i in reversed(bullets_to_remove):
        bullets.pop(i)

def draw_npc(x=0, y=0, z=0, rotation=0):
    """
    Draws an NPC as a red cuboid, same height as human but half the width.
    """
    glPushMatrix()
    glColor3f(1, 0, 0)  # Red color
    glTranslatef(x, y, z + 90)  # Elevate NPC above ground (half of human torso height)
    glRotatef(rotation, 0, 0, 1)
    # Human torso: width=200, height=50, depth=180 (scaled by 1/3)
    # NPC: half width, same height/depth but not scaled
    draw_rectangular_cuboid(100, 50, 180)
    glPopMatrix()

def draw_shapes():

    # glPushMatrix()  # Save the current matrix state
    # glColor3f(1, 0, 0)
    # glTranslatef(0, 0, 0)  
    # glutSolidCube(60) # Take cube size as the parameter
    # glTranslatef(0, 0, 60) 
    # glColor3f(0, 1, 0)
    # glutSolidCube(60) 

    # glColor3f(1, 1, 0)
    # gluCylinder(gluNewQuadric(), 40, 5, 150, 10, 10)  # parameters are: quadric, base radius, top radius, height, slices, stacks
    # glTranslatef(100, 0, 100) 
    # glRotatef(90, 0, 1, 0)  # parameters are: angle, x, y, z
    # gluCylinder(gluNewQuadric(), 40, 5, 150, 10, 10)

    # glColor3f(0, 1, 1)
    # glTranslatef(300, 0, 100) 
    # gluSphere(gluNewQuadric(), 80, 10, 10)  # parameters are: quadric, radius, slices, stacks

    glPopMatrix()  # Restore the previous matrix state
    
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
    
    # Draw a cylinder in the middle of the torso
    glPushMatrix()
    glColor3f(0.5, 0.2, 0.8)
    glTranslatef(0, 0, 200)  # Move to the center of the torso
    glRotatef(-90, 1, 0, 0)   # Align cylinder vertically
    gluCylinder(gluNewQuadric(), 20, 20, 100, 20, 20)
    glPopMatrix()

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
    Handles keyboard inputs for player movement, gun rotation, camera updates, and cheat mode toggles.
    """
    global human_x, human_y, human_z, human_rotation,first_person_camera
    # # Move forward (W key)
    if key == b'w': 
        human_y +=3 * math.cos(math.radians(-human_rotation))
        human_x +=3 * math.sin(math.radians(-human_rotation))
        
        #keep player inside the grid
        if human_x > GRID_LENGTH:
            human_x = GRID_LENGTH
        if human_x < -GRID_LENGTH:
            human_x = -GRID_LENGTH
        if human_y > GRID_LENGTH:
            human_y = GRID_LENGTH
        if human_y < -GRID_LENGTH:
            human_y = -GRID_LENGTH

    # # Move backward (S key)
    if key == b's':
        human_y -=3 * math.cos(math.radians(-human_rotation))
        human_x -=3 * math.sin(math.radians(-human_rotation))
        
        if human_x > GRID_LENGTH:
            human_x = GRID_LENGTH
        if human_x < -GRID_LENGTH:
            human_x = -GRID_LENGTH
        if human_y > GRID_LENGTH:
            human_y = GRID_LENGTH
        if human_y < -GRID_LENGTH:
            human_y = -GRID_LENGTH

    # # Rotate gun left (A key)
    if key == b'a':
        human_rotation += 3  

    # # Rotate gun right (D key)
    if key == b'd':
        human_rotation -= 3

    # # Toggle cheat mode (C key)
    # if key == b'c':

    # # Toggle cheat vision (V key)
    if key == b'v':
        first_person_camera = not first_person_camera

    # # Reset the game if R key is pressed
    # if key == b'r':


def specialKeyListener(key, x, y):
    """
    Handles special key inputs (arrow keys) for adjusting the camera angle and height.
    """
    global camera_pos
    x, y, z = camera_pos
    # Move camera up (UP arrow key)
    if key == GLUT_KEY_UP:
        y += 3
        z += 3  # Uncomment if you want to move camera up in z direction

    # # Move camera down (DOWN arrow key)
    if key == GLUT_KEY_DOWN:
        y -= 3
        z -= 3  # Uncomment if you want to move camera down in z direction

    # moving camera left (LEFT arrow key)
    if key == GLUT_KEY_LEFT:
        x -= 3  # Small angle decrement for smooth movement

    # moving camera right (RIGHT arrow key)
    if key == GLUT_KEY_RIGHT:
        x += 3  # Small angle increment for smooth movement

    camera_pos = (x, y, z)

def mouseListener(button, state, x, y):
    global bullet_radius
    """
    Handles mouse inputs for firing bullets (left click) and toggling camera mode (right click).
    """
    # # Left mouse button fires a bullet
    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        # Start bullet position from the middle of the torso, slightly in front
        angle_rad = math.radians(-human_rotation)
        offset_distance = 30  # Distance in front of the character
        
        cyl_x = human_x + math.sin(angle_rad) * offset_distance
        cyl_y = human_y + math.cos(angle_rad) * offset_distance
        cyl_z = human_z + (200 / 3)  # Torso center z position

        # Bullet direction based on human_rotation
        dir_x = math.sin(angle_rad)
        dir_y = math.cos(angle_rad)
        dir_z = 0  # Bullets move parallel to the ground

        # Store bullet as a dict with position, direction, and size
        bullets.append({
            'pos': [cyl_x, cyl_y, cyl_z],
            'dir': [dir_x, dir_y, dir_z],
            'radius': bullet_radius
        })
        print(f"Bullet fired from ({cyl_x:.1f}, {cyl_y:.1f}, {cyl_z:.1f}) in direction ({dir_x:.2f}, {dir_y:.2f}, {dir_z:.2f})")
        print(f"Total bullets: {len(bullets)}")

    # # Right mouse button toggles camera tracking mode
    # if button == GLUT_RIGHT_BUTTON and state == GLUT_DOWN:


def setupCamera():
    global first_person_camera, camera_pos, fovY
    """
    Configures the camera's projection and view settings.
    Uses a perspective projection and positions the camera to look at the target.
    """
    glMatrixMode(GL_PROJECTION)  # Switch to projection matrix mode
    glLoadIdentity()  # Reset the projection matrix
    # Set up a perspective projection (field of view, aspect ratio, near clip, far clip)
    gluPerspective(fovY, 1.25, 0.1, 1500) # Think why aspect ration is 1.25?
    glMatrixMode(GL_MODELVIEW)  # Switch to model-view matrix mode
    glLoadIdentity()  # Reset the model-view matrix

    # Extract camera position and look-at target
    if first_person_camera:
        # First-person camera mode: position just outside the human's head and look in the direction the human is facing
        head_radius = 50 / 3  # Scaled head radius
        x = human_x + math.sin(math.radians(-human_rotation)) * (head_radius + 5)
        y = human_y + math.cos(math.radians(-human_rotation)) * (head_radius + 5)
        z = human_z + (325 / 3)  # Head center z position

        # Calculate look-at target based on human_rotation
        angle_rad = math.radians(-human_rotation)
        look_x = x + math.sin(angle_rad) * 50
        look_y = y + math.cos(angle_rad) * 50
        look_z = z   # Keep the same height

        gluLookAt(x, y, z,  # Camera position (just outside the head)
                  look_x, look_y, look_z,  # Look-at target (in front of human)
                  0, 0, 1)  # Up vector (z-axis)
    else:
        # Default camera position
        x, y, z = camera_pos
    # Position the camera and set its orientation
        gluLookAt(x, y, z,  # Camera position
                0, 0, 0,  # Look-at target
                0, 0, 1)  # Up vector (z-axis)


def idle():
    """
    Idle function that runs continuously:
    - Updates bullet positions and removes bullets that hit walls
    - Triggers screen redraw for real-time updates.
    """
    # Update bullet positions and handle collisions
    update_bullets()
    
    # Ensure the screen updates with the latest changes
    glutPostRedisplay()


def showScreen():
    """
    Display function to render the game scene:
    - Clears the screen and sets up the camera.
    - Draws everything of the screen
    """
    global npc_data, npc_max
    
    # Generate random NPCs if not already created
    if not npc_data:
        for _ in range(npc_max):
            npc_x = random.randint(-GRID_LENGTH + 100, GRID_LENGTH - 100)  # Keep away from walls
            npc_y = random.randint(-GRID_LENGTH + 100, GRID_LENGTH - 100)  # Keep away from walls
            npc_z = 0  # Ground level
            npc_rotation = random.randint(0, 360)
            npc_data.append({'x': npc_x, 'y': npc_y, 'z': npc_z, 'rotation': npc_rotation})

    # Clear color and depth buffers
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()  # Reset modelview matrix
    glViewport(0, 0, 1000, 800)  # Set viewport size

    setupCamera()  # Configure camera perspective

    # Draw a random points
    glPointSize(20)
    glBegin(GL_POINTS)
    glVertex3f(-GRID_LENGTH, GRID_LENGTH, 0)
    glEnd()

    # Draw the grid (game floor) as 8x8 tiles
    tile_size = GRID_LENGTH * 2 // 8  # Each tile's size
    start = -GRID_LENGTH
    glBegin(GL_QUADS)
    for i in range(8):
        for j in range(8):
            # Alternate colors for a checkerboard effect
            if (i + j) % 2 == 0:
                glColor3f(1, 1, 1)
            else:
                glColor3f(0.7, 0.5, 0.95)
            x0 = start + i * tile_size
            y0 = start + j * tile_size
            x1 = x0 + tile_size
            y1 = y0 + tile_size
            glVertex3f(x0, y0, 0)
            glVertex3f(x1, y0, 0)
            glVertex3f(x1, y1, 0)
            glVertex3f(x0, y1, 0)
    glEnd()
    
    # Draw a tall boundary (walls) around the grid, each with a different color
    wall_thickness = 20
    wall_height = 200
    # Left wall - Red
    glColor3f(1.0, 0.2, 0.2)
    glPushMatrix()
    glTranslatef(-GRID_LENGTH - wall_thickness / 2, 0, wall_height / 2)
    draw_rectangular_cuboid(wall_thickness, GRID_LENGTH * 2 + wall_thickness * 2, wall_height)
    glPopMatrix()
    # Right wall - Green
    glColor3f(0.2, 1.0, 0.2)
    glPushMatrix()
    glTranslatef(GRID_LENGTH + wall_thickness / 2, 0, wall_height / 2)
    draw_rectangular_cuboid(wall_thickness, GRID_LENGTH * 2 + wall_thickness * 2, wall_height)
    glPopMatrix()
    # Top wall - Blue
    glColor3f(0.2, 0.2, 1.0)
    glPushMatrix()
    glTranslatef(0, GRID_LENGTH + wall_thickness / 2, wall_height / 2)
    draw_rectangular_cuboid(GRID_LENGTH * 2 + wall_thickness * 2, wall_thickness, wall_height)
    glPopMatrix()
    # Bottom wall - Yellow
    glColor3f(1.0, 1.0, 0.2)
    glPushMatrix()
    glTranslatef(0, -GRID_LENGTH - wall_thickness / 2, wall_height / 2)
    draw_rectangular_cuboid(GRID_LENGTH * 2 + wall_thickness * 2, wall_thickness, wall_height)
    glPopMatrix()

    # Display game info text at a fixed screen position
    draw_text(10, 770, f"Assignment 3")
    
    
    

    #draw_shapes()
    draw_human(human_x, human_y, human_z, human_rotation)  # Draw the human figure

    # Draw all NPCs
    for npc in npc_data:
        draw_npc(npc['x'], npc['y'], npc['z'], npc['rotation'])

    # Draw all bullets
    for bullet in bullets:
        draw_bullet(bullet)

    # Swap buffers for smooth rendering (double buffering)
    glutSwapBuffers()


# Main function to set up OpenGL window and loop
def main():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)  # Double buffering, RGB color, depth test
    glutInitWindowSize(1000, 800)  # Window size
    glutInitWindowPosition(0, 0)  # Window position
    wind = glutCreateWindow(b"3D OpenGL Intro")  # Create the window

    glutDisplayFunc(showScreen)  # Register display function
    glutKeyboardFunc(keyboardListener)  # Register keyboard listener
    glutSpecialFunc(specialKeyListener)
    glutMouseFunc(mouseListener)
    glutIdleFunc(idle)  # Register the idle function to move the bullet automatically

    glutMainLoop()  # Enter the GLUT main loop

if __name__ == "__main__":
    main()
