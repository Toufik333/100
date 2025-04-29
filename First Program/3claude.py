from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import math
import random

# Game state variables
game_over = False
score = 0
player_lives = 5
bullets_missed = 0

# Camera-related variables
camera_pos = (0, 500, 500)
camera_angle = 0
camera_height = 500
first_person_mode = False

# Player-related variables
player_pos = [0, 0, 30]  # Center of the grid, z=30 for height
player_angle = 0
player_speed = 10

# Gun dimensions
gun_length = 80
gun_width = 20
gun_height = 15

# Cheats
cheat_mode = False
auto_vision = False

# Bullets
bullets = []  # List to store active bullets
bullet_speed = 15
bullet_size = 10

# Enemies
enemies = []
enemy_speed = .5
num_enemies = 5
enemy_pulse = 0
enemy_pulse_rate = 0.05

# Game settings
fovY = 120  # Field of view
GRID_LENGTH = 600  # Length of grid lines


class Bullet:
    def __init__(self, x, y, z, angle):
        self.x = x
        self.y = y
        self.z = z
        self.angle = angle
        self.active = True

    def update(self):
        # Move bullet in the direction of gun angle
        self.x += bullet_speed * math.cos(math.radians(self.angle))
        self.y += bullet_speed * math.sin(math.radians(self.angle))
        
        # Check if bullet is out of bounds
        if abs(self.x) > GRID_LENGTH or abs(self.y) > GRID_LENGTH:
            self.active = False
            global bullets_missed
            if not game_over:
                bullets_missed += 1
                
    def draw(self):
        glPushMatrix()
        glTranslatef(self.x, self.y, self.z)
        glColor3f(1.0, 0.5, 0.0)  # Orange color for bullets
        glutSolidCube(bullet_size)
        glPopMatrix()


class Enemy:
    def __init__(self):
        self.respawn()
        
    def respawn(self):
        # Spawn at a random position on the grid, but not too close to the player
        while True:
            self.x = random.uniform(-GRID_LENGTH + 50, GRID_LENGTH - 50)
            self.y = random.uniform(-GRID_LENGTH + 50, GRID_LENGTH - 50)
            # Check if far enough from player
            dist = math.sqrt((self.x - player_pos[0])**2 + (self.y - player_pos[1])**2)
            if dist > 200:  # At least 200 units away from player
                break
        self.z = 30  # Height
        self.size = 25  # Base size of enemy
        
    def update(self):
        # Move toward player
        dx = player_pos[0] - self.x
        dy = player_pos[1] - self.y
        distance = math.sqrt(dx*dx + dy*dy)
        
        if distance > 0:
            self.x += (dx / distance) * enemy_speed
            self.y += (dy / distance) * enemy_speed

        # Check for collision with player
        if distance < 50 and not game_over:  # Close enough to be a hit
            global player_lives
            player_lives -= 1
            self.respawn()
            
        # Check for collision with bullets
        for bullet in bullets:
            if bullet.active:
                bullet_distance = math.sqrt((bullet.x - self.x)**2 + (bullet.y - self.y)**2)
                if bullet_distance < 40:  # Hit!
                    bullet.active = False
                    global score
                    score += 10
                    self.respawn()
                    break
        
    def draw(self):
        global enemy_pulse
        pulse_size = math.sin(enemy_pulse) * 5  # Vary size by +/- 5 units
        
        glPushMatrix()
        glTranslatef(self.x, self.y, self.z)
        
        # Main body (bigger sphere)
        glColor3f(0.8, 0.2, 0.2)  # Red color
        gluSphere(gluNewQuadric(), self.size + pulse_size, 16, 16)
        
        # Smaller sphere on top
        glTranslatef(0, 0, self.size + 5)
        glColor3f(0.9, 0.1, 0.1)  # Darker red for the head
        gluSphere(gluNewQuadric(), (self.size/2) + pulse_size/2, 16, 16)
        
        glPopMatrix()


def draw_player():
    if game_over:
        # Draw player lying down
        draw_player_dead()
    else:
        # Draw the player's gun
        glPushMatrix()
        
        # Position at player coordinates
        glTranslatef(player_pos[0], player_pos[1], player_pos[2])
        glRotatef(player_angle, 0, 0, 1)  # Rotate around z-axis based on player angle
        
        # Base (main body) - Sphere
        glColor3f(0.4, 0.4, 0.7)  # Blue-gray color
        gluSphere(gluNewQuadric(), 25, 16, 16)
        
        # Gun barrel (cylinder)
        glColor3f(0.3, 0.3, 0.3)  # Dark gray
        glRotatef(90, 0, 1, 0)  # Orient cylinder along x-axis
        gluCylinder(gluNewQuadric(), 10, 10, gun_length, 12, 1)
        
        # Gun sight on top of the barrel
        glTranslatef(0, 15, gun_length/2)
        glColor3f(0.7, 0.7, 0.7)  # Light gray
        glutSolidCube(10)
        
        glPopMatrix()


def draw_player_dead():
    glPushMatrix()
    
    # Position at player coordinates but lying on the ground
    glTranslatef(player_pos[0], player_pos[1], 15)  # Lower z position
    glRotatef(player_angle, 0, 0, 1)  # Maintain rotation angle
    glRotatef(90, 1, 0, 0)  # Rotate 90 degrees to lie down
    
    # Base (main body) - Sphere
    glColor3f(0.4, 0.4, 0.7)  # Blue-gray color
    gluSphere(gluNewQuadric(), 25, 16, 16)
    
    # Gun barrel (cylinder)
    glColor3f(0.3, 0.3, 0.3)  # Dark gray
    glRotatef(90, 0, 1, 0)  # Orient cylinder along x-axis
    gluCylinder(gluNewQuadric(), 10, 10, gun_length, 12, 1)
    
    # Gun sight on top of the barrel
    glTranslatef(0, 15, gun_length/2)
    glColor3f(0.7, 0.7, 0.7)  # Light gray
    glutSolidCube(10)
    
    glPopMatrix()


def draw_grid():
    # Draw the grid floor
    cell_size = 50  # Size of each grid cell
    
    glBegin(GL_LINES)
    glColor3f(0.5, 0.5, 0.5)  # Gray color for grid lines
    
    # Draw horizontal lines
    for i in range(-GRID_LENGTH, GRID_LENGTH + 1, cell_size):
        glVertex3f(i, -GRID_LENGTH, 0)
        glVertex3f(i, GRID_LENGTH, 0)
    
    # Draw vertical lines
    for i in range(-GRID_LENGTH, GRID_LENGTH + 1, cell_size):
        glVertex3f(-GRID_LENGTH, i, 0)
        glVertex3f(GRID_LENGTH, i, 0)
    
    glEnd()
    
    # Draw the floor (actual surface)
    glBegin(GL_QUADS)
    glColor3f(0.2, 0.2, 0.2)  # Dark color for the floor
    glVertex3f(-GRID_LENGTH, -GRID_LENGTH, -1)
    glVertex3f(-GRID_LENGTH, GRID_LENGTH, -1)
    glVertex3f(GRID_LENGTH, GRID_LENGTH, -1)
    glVertex3f(GRID_LENGTH, -GRID_LENGTH, -1)
    glEnd()
    
    # Draw boundary walls
    draw_boundaries()


def draw_boundaries():
    wall_height = 100
    
    glBegin(GL_QUADS)
    
    # North wall (positive y)
    glColor3f(0.7, 0.0, 0.0)  # Red
    glVertex3f(-GRID_LENGTH, GRID_LENGTH, 0)
    glVertex3f(GRID_LENGTH, GRID_LENGTH, 0)
    glVertex3f(GRID_LENGTH, GRID_LENGTH, wall_height)
    glVertex3f(-GRID_LENGTH, GRID_LENGTH, wall_height)
    
    # South wall (negative y)
    glColor3f(0.0, 0.7, 0.0)  # Green
    glVertex3f(-GRID_LENGTH, -GRID_LENGTH, 0)
    glVertex3f(GRID_LENGTH, -GRID_LENGTH, 0)
    glVertex3f(GRID_LENGTH, -GRID_LENGTH, wall_height)
    glVertex3f(-GRID_LENGTH, -GRID_LENGTH, wall_height)
    
    # East wall (positive x)
    glColor3f(0.0, 0.0, 0.7)  # Blue
    glVertex3f(GRID_LENGTH, -GRID_LENGTH, 0)
    glVertex3f(GRID_LENGTH, GRID_LENGTH, 0)
    glVertex3f(GRID_LENGTH, GRID_LENGTH, wall_height)
    glVertex3f(GRID_LENGTH, -GRID_LENGTH, wall_height)
    
    # West wall (negative x)
    glColor3f(0.7, 0.7, 0.0)  # Yellow
    glVertex3f(-GRID_LENGTH, -GRID_LENGTH, 0)
    glVertex3f(-GRID_LENGTH, GRID_LENGTH, 0)
    glVertex3f(-GRID_LENGTH, GRID_LENGTH, wall_height)
    glVertex3f(-GRID_LENGTH, -GRID_LENGTH, wall_height)
    
    glEnd()


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


def fire_bullet():
    if not game_over:
        # Create bullet at the end of the gun barrel
        bullet_x = player_pos[0] + math.cos(math.radians(player_angle)) * gun_length
        bullet_y = player_pos[1] + math.sin(math.radians(player_angle)) * gun_length
        bullet_z = player_pos[2]
        new_bullet = Bullet(bullet_x, bullet_y, bullet_z, player_angle)
        bullets.append(new_bullet)


def check_game_over():
    global game_over
    
    if player_lives <= 0 or bullets_missed >= 10:
        game_over = True


def initialize_enemies():
    global enemies
    enemies = []
    for _ in range(num_enemies):
        enemies.append(Enemy())


def reset_game():
    global game_over, score, player_lives, bullets_missed, player_pos, bullets
    game_over = False
    score = 0
    player_lives = 5
    bullets_missed = 0
    player_pos = [0, 0, 30]
    bullets = []
    initialize_enemies()


def cheat_update():
    if cheat_mode and not game_over:
        global player_angle
        player_angle = (player_angle + 5) % 360
        
        # Check if any enemy is in line of sight for auto-firing
        for enemy in enemies:
            dx = enemy.x - player_pos[0]
            dy = enemy.y - player_pos[1]
            enemy_angle = math.degrees(math.atan2(dy, dx))
            if enemy_angle < 0:
                enemy_angle += 360
                
            # If enemy is close to current gun angle, fire a bullet
            angle_diff = abs(player_angle - enemy_angle)
            if angle_diff < 5 or angle_diff > 355:
                fire_bullet()
                break


def keyboardListener(key, x, y):
    """
    Handles keyboard inputs for player movement, gun rotation, camera updates, and cheat mode toggles.
    """
    global player_pos, player_angle, cheat_mode, auto_vision
    
    if not game_over:
        # Move forward (W key)
        if key == b'w':
            player_pos[0] += player_speed * math.cos(math.radians(player_angle))
            player_pos[1] += player_speed * math.sin(math.radians(player_angle))
            
            # Keep player inside boundaries
            player_pos[0] = max(min(player_pos[0], GRID_LENGTH - 50), -GRID_LENGTH + 50)
            player_pos[1] = max(min(player_pos[1], GRID_LENGTH - 50), -GRID_LENGTH + 50)

        # Move backward (S key)
        if key == b's':
            player_pos[0] -= player_speed * math.cos(math.radians(player_angle))
            player_pos[1] -= player_speed * math.sin(math.radians(player_angle))
            
            # Keep player inside boundaries
            player_pos[0] = max(min(player_pos[0], GRID_LENGTH - 50), -GRID_LENGTH + 50)
            player_pos[1] = max(min(player_pos[1], GRID_LENGTH - 50), -GRID_LENGTH + 50)

        # Rotate gun left (A key)
        if key == b'a':
            player_angle = (player_angle + 5) % 360

        # Rotate gun right (D key)
        if key == b'd':
            player_angle = (player_angle - 5) % 360

        # Toggle cheat mode (C key)
        if key == b'c':
            cheat_mode = not cheat_mode
            if not cheat_mode:
                auto_vision = False

        # Toggle cheat vision (V key)
        if key == b'v':
            if cheat_mode:  # Only works when cheat mode is active
                auto_vision = not auto_vision

    # Reset the game if R key is pressed
    if key == b'r':
        reset_game()

    glutPostRedisplay()


def specialKeyListener(key, x, y):
    """
    Handles special key inputs (arrow keys) for adjusting the camera angle and height.
    """
    global camera_angle, camera_height
    
    # Move camera up (UP arrow key)
    if key == GLUT_KEY_UP:
        camera_height = min(camera_height + 10, 1000)  # Limit max height

    # Move camera down (DOWN arrow key)
    if key == GLUT_KEY_DOWN:
        camera_height = max(camera_height - 10, 100)  # Limit min height

    # moving camera left (LEFT arrow key)
    if key == GLUT_KEY_LEFT:
        camera_angle = (camera_angle + 5) % 360  # Rotate counterclockwise

    # moving camera right (RIGHT arrow key)
    if key == GLUT_KEY_RIGHT:
        camera_angle = (camera_angle - 5) % 360  # Rotate clockwise

    glutPostRedisplay()


def mouseListener(button, state, x, y):
    """
    Handles mouse inputs for firing bullets (left click) and toggling camera mode (right click).
    """
    global first_person_mode
    
    # Left mouse button fires a bullet
    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        fire_bullet()

    # Right mouse button toggles camera tracking mode
    if button == GLUT_RIGHT_BUTTON and state == GLUT_DOWN:
        first_person_mode = not first_person_mode

    glutPostRedisplay()


def setupCamera():
    """
    Configures the camera's projection and view settings.
    Uses a perspective projection and positions the camera to look at the target.
    """
    glMatrixMode(GL_PROJECTION)  # Switch to projection matrix mode
    glLoadIdentity()  # Reset the projection matrix
    # Set up a perspective projection (field of view, aspect ratio, near clip, far clip)
    gluPerspective(fovY, 1.25, 0.1, 1500)  # Aspect ratio 1.25 (1000/800)
    glMatrixMode(GL_MODELVIEW)  # Switch to model-view matrix mode
    glLoadIdentity()  # Reset the model-view matrix

    if first_person_mode:
        # First-person view (from gun position)
        eye_x = player_pos[0] - 50 * math.cos(math.radians(player_angle))
        eye_y = player_pos[1] - 50 * math.sin(math.radians(player_angle))
        eye_z = player_pos[2] + 20
        
        look_x = player_pos[0] + 100 * math.cos(math.radians(player_angle))
        look_y = player_pos[1] + 100 * math.sin(math.radians(player_angle))
        look_z = player_pos[2] + 10
        
        gluLookAt(eye_x, eye_y, eye_z,  # Camera position
                  look_x, look_y, look_z,  # Look-at target
                  0, 0, 1)  # Up vector (z-axis)
    else:
        # Third-person view (orbiting camera)
        rad = camera_height  # Distance from center
        
        eye_x = rad * math.cos(math.radians(camera_angle))
        eye_y = rad * math.sin(math.radians(camera_angle))
        eye_z = camera_height
        
        # If auto_vision is enabled and in cheat mode, look at player, otherwise look at origin
        if auto_vision and cheat_mode:
            gluLookAt(eye_x + player_pos[0], eye_y + player_pos[1], eye_z,  # Camera position
                      player_pos[0], player_pos[1], player_pos[2],  # Look-at target
                      0, 0, 1)  # Up vector (z-axis)
        else:
            gluLookAt(eye_x, eye_y, eye_z,  # Camera position
                      0, 0, 0,  # Look-at target
                      0, 0, 1)  # Up vector (z-axis)


def update_game():
    """
    Updates all game objects and states.
    """
    if not game_over:
        # Update enemies
        for enemy in enemies:
            enemy.update()
            
        # Update bullets
        for bullet in bullets[:]:
            bullet.update()
            if not bullet.active:
                bullets.remove(bullet)
                
        # Update enemy pulsation
        global enemy_pulse
        enemy_pulse += enemy_pulse_rate
        
        # Check if game should end
        check_game_over()
        
        # Apply cheat mode updates
        if cheat_mode:
            cheat_update()


def idle():
    """
    Idle function that runs continuously to update game state.
    """
    update_game()
    glutPostRedisplay()


def showScreen():
    """
    Display function to render the game scene.
    """
    # Clear color and depth buffers
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()  # Reset modelview matrix
    glViewport(0, 0, 1000, 800)  # Set viewport size

    setupCamera()  # Configure camera perspective
    
    # Enable depth testing for proper 3D rendering
    glEnable(GL_DEPTH_TEST)
    
    # Draw the grid and boundaries
    draw_grid()
    
    # Draw the player
    draw_player()
    
    # Draw all active bullets
    for bullet in bullets:
        bullet.draw()
    
    # Draw all enemies
    for enemy in enemies:
        enemy.draw()
    
    # Display game information
    draw_text(10, 770, f"Lives: {player_lives}")
    draw_text(10, 740, f"Score: {score}")
    draw_text(10, 710, f"Bullets Missed: {bullets_missed}")
    
    if cheat_mode:
        draw_text(800, 770, "CHEAT MODE ON")
        if auto_vision:
            draw_text(800, 740, "AUTO-VISION ON")
    
    if game_over:
        draw_text(400, 400, "GAME OVER!")
        draw_text(380, 370, "Press 'R' to restart")
    
    # Swap buffers for smooth rendering (double buffering)
    glutSwapBuffers()


# Main function to set up OpenGL window and loop
def main():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)  # Double buffering, RGB color, depth test
    glutInitWindowSize(1000, 800)  # Window size
    glutInitWindowPosition(0, 0)  # Window position
    wind = glutCreateWindow(b"Bullet Frenzy")  # Create the window

    # Initialize game
    initialize_enemies()
    
    glutDisplayFunc(showScreen)  # Register display function
    glutKeyboardFunc(keyboardListener)  # Register keyboard listener
    glutSpecialFunc(specialKeyListener)
    glutMouseFunc(mouseListener)
    glutIdleFunc(idle)  # Register the idle function for game updates
    
    # Enable lighting and set material properties
    glEnable(GL_DEPTH_TEST)

    glutMainLoop()  # Enter the GLUT main loop

if __name__ == "__main__":
    main()