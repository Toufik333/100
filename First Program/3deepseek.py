from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random
import math

# Game state variables
player_pos = [0, 0, 0]  # Player position (x, y, z)
player_angle = 0  # Player rotation angle
player_lives = 5
game_score = 0
bullets_missed = 0
game_over = False

# Cheat mode flags
cheat_mode = False
cheat_vision = False

# Camera settings
camera_pos = [0, 500, 500]
camera_angle = 0
camera_height = 500
camera_distance = 500
first_person = False

# Enemy settings
enemies = []
ENEMY_COUNT = 5
enemy_size = 30
enemy_pulse_dir = 1

# Bullet settings
bullets = []
BULLET_SPEED = 10
bullet_size = 10

# Game settings
GRID_LENGTH = 600
fovY = 120
PLAYER_SPEED = 5
ENEMY_SPEED = 1

def init_game():
    global player_pos, player_angle, player_lives, game_score, bullets_missed, game_over
    global enemies, bullets, cheat_mode, cheat_vision
    
    player_pos = [0, 0, 0]
    player_angle = 0
    player_lives = 5
    game_score = 0
    bullets_missed = 0
    game_over = False
    cheat_mode = False
    cheat_vision = False
    bullets = []
    
    # Initialize enemies at random positions
    enemies = []
    for _ in range(ENEMY_COUNT):
        x = random.randint(-GRID_LENGTH//2, GRID_LENGTH//2)
        y = random.randint(-GRID_LENGTH//2, GRID_LENGTH//2)
        z = 0
        enemies.append([x, y, z, enemy_size])  # x, y, z, size

def draw_player():
    glPushMatrix()
    
    if game_over:
        # Player lies down when game is over
        glTranslatef(player_pos[0], player_pos[1], player_pos[2])
        glRotatef(90, 1, 0, 0)  # Rotate to lying position
    else:
        # Normal player position
        glTranslatef(player_pos[0], player_pos[1], player_pos[2])
        glRotatef(player_angle, 0, 0, 1)
    
    # Player body (cube)
    glColor3f(0.2, 0.2, 0.8)
    glPushMatrix()
    glTranslatef(0, 0, 30)
    glScalef(30, 30, 60)
    glutSolidCube(1)
    glPopMatrix()
    
    # Player head (sphere)
    glColor3f(0.9, 0.7, 0.5)
    glPushMatrix()
    glTranslatef(0, 0, 70)
    glutSolidSphere(20, 20, 20)
    glPopMatrix()
    
    # Gun (cylinder + cube)
    glColor3f(0.3, 0.3, 0.3)
    glPushMatrix()
    glTranslatef(20, 0, 40)
    glRotatef(90, 0, 1, 0)
    gluCylinder(gluNewQuadric(), 5, 5, 60, 10, 10)
    glTranslatef(0, 0, 60)
    glutSolidSphere(8, 10, 10)
    glPopMatrix()
    
    glPopMatrix()

def draw_enemies():
    global enemy_size, enemy_pulse_dir
    
    # Pulse enemy size for animation
    enemy_size += enemy_pulse_dir * 0.5
    if enemy_size > 35 or enemy_size < 25:
        enemy_pulse_dir *= -1
    
    for enemy in enemies:
        glPushMatrix()
        glTranslatef(enemy[0], enemy[1], enemy[2])
        
        # Main enemy body
        glColor3f(0.8, 0.2, 0.2)
        glutSolidSphere(enemy_size, 20, 20)
        
        # Enemy head
        glColor3f(0.9, 0.1, 0.1)
        glTranslatef(0, 0, enemy_size)
        glutSolidSphere(enemy_size * 0.6, 20, 20)
        
        glPopMatrix()

def draw_bullets():
    for bullet in bullets:
        glPushMatrix()
        glTranslatef(bullet[0], bullet[1], bullet[2])
        glColor3f(1, 1, 0)
        glutSolidCube(bullet_size)
        glPopMatrix()

def draw_grid():
    # Draw the grid floor
    glBegin(GL_QUADS)
    for i in range(-GRID_LENGTH, GRID_LENGTH, 100):
        for j in range(-GRID_LENGTH, GRID_LENGTH, 100):
            # Alternate colors for checkered pattern
            if (i + j) % 200 == 0:
                glColor3f(0.7, 0.5, 0.95)
            else:
                glColor3f(1, 1, 1)
            
            glVertex3f(i, j, 0)
            glVertex3f(i + 100, j, 0)
            glVertex3f(i + 100, j + 100, 0)
            glVertex3f(i, j + 100, 0)
    glEnd()
    
    # Draw boundaries
    glColor3f(0.5, 0.5, 0.5)
    glBegin(GL_LINES)
    for i in range(-GRID_LENGTH, GRID_LENGTH + 1, 100):
        # Vertical boundaries
        glVertex3f(i, -GRID_LENGTH, 0)
        glVertex3f(i, -GRID_LENGTH, 100)
        glVertex3f(i, GRID_LENGTH, 0)
        glVertex3f(i, GRID_LENGTH, 100)
        glVertex3f(-GRID_LENGTH, i, 0)
        glVertex3f(-GRID_LENGTH, i, 100)
        glVertex3f(GRID_LENGTH, i, 0)
        glVertex3f(GRID_LENGTH, i, 100)
    glEnd()

def draw_text(x, y, text, font=GLUT_BITMAP_HELVETICA_18):
    glColor3f(1, 1, 1)
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    gluOrtho2D(0, 1000, 0, 800)
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()
    glRasterPos2f(x, y)
    for ch in text:
        glutBitmapCharacter(font, ord(ch))
    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)

def keyboardListener(key, x, y):
    global player_pos, player_angle, cheat_mode, cheat_vision, game_over
    
    if game_over and key == b'r':
        init_game()
        return
    
    key = key.decode('utf-8').lower()
    
    # Player movement
    if not game_over:
        if key == 'w':  # Move forward
            player_pos[0] += PLAYER_SPEED * math.sin(math.radians(player_angle))
            player_pos[1] += PLAYER_SPEED * math.cos(math.radians(player_angle))
        elif key == 's':  # Move backward
            player_pos[0] -= PLAYER_SPEED * math.sin(math.radians(player_angle))
            player_pos[1] -= PLAYER_SPEED * math.cos(math.radians(player_angle))
        elif key == 'a':  # Rotate left
            player_angle += 5
        elif key == 'd':  # Rotate right
            player_angle -= 5
    
    # Cheat modes
    if key == 'c':
        cheat_mode = not cheat_mode
    elif key == 'v' and cheat_mode:
        cheat_vision = not cheat_vision

def specialKeyListener(key, x, y):
    global camera_angle, camera_height, first_person
    
    if key == GLUT_KEY_UP:
        camera_height += 10
    elif key == GLUT_KEY_DOWN:
        camera_height -= 10
    elif key == GLUT_KEY_LEFT:
        camera_angle += 5
    elif key == GLUT_KEY_RIGHT:
        camera_angle -= 5
    
    # Keep camera height within reasonable bounds
    camera_height = max(100, min(1000, camera_height))

def mouseListener(button, state, x, y):
    global bullets
    
    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN and not game_over:
        # Create a new bullet at player position with player angle
        bullet_x = player_pos[0]
        bullet_y = player_pos[1]
        bullet_z = 40  # Gun height
        bullets.append([bullet_x, bullet_y, bullet_z, player_angle])
    
    elif button == GLUT_RIGHT_BUTTON and state == GLUT_DOWN:
        # Toggle camera mode
        global first_person
        first_person = not first_person

def update_game():
    global bullets, enemies, game_score, bullets_missed, player_lives, game_over
    
    if game_over:
        return
    
    # Update bullet positions
    for bullet in bullets[:]:
        angle_rad = math.radians(bullet[3])
        bullet[0] += BULLET_SPEED * math.sin(angle_rad)
        bullet[1] += BULLET_SPEED * math.cos(angle_rad)
        
        # Remove bullets that go out of bounds
        if (abs(bullet[0]) > GRID_LENGTH or abs(bullet[1]) > GRID_LENGTH):
            bullets.remove(bullet)
            bullets_missed += 1
            if bullets_missed >= 10:
                game_over = True
    
    # Update enemy positions (move toward player)
    for enemy in enemies:
        dx = player_pos[0] - enemy[0]
        dy = player_pos[1] - enemy[1]
        dist = math.sqrt(dx*dx + dy*dy)
        
        if dist > 0:
            enemy[0] += ENEMY_SPEED * dx / dist
            enemy[1] += ENEMY_SPEED * dy / dist
        
        # Check collision with player
        player_dist = math.sqrt((player_pos[0]-enemy[0])**2 + (player_pos[1]-enemy[1])**2)
        if player_dist < 40:  # Collision detection
            player_lives -= 1
            if player_lives <= 0:
                game_over = True
            # Respawn enemy
            enemy[0] = random.randint(-GRID_LENGTH//2, GRID_LENGTH//2)
            enemy[1] = random.randint(-GRID_LENGTH//2, GRID_LENGTH//2)
    
    # Check bullet-enemy collisions
    for bullet in bullets[:]:
        for enemy in enemies[:]:
            dist = math.sqrt((bullet[0]-enemy[0])**2 + (bullet[1]-enemy[1])**2)
            if dist < enemy_size + bullet_size/2:
                bullets.remove(bullet)
                enemies.remove(enemy)
                game_score += 10
                # Respawn enemy
                x = random.randint(-GRID_LENGTH//2, GRID_LENGTH//2)
                y = random.randint(-GRID_LENGTH//2, GRID_LENGTH//2)
                enemies.append([x, y, 0, enemy_size])
                break
    
    # Cheat mode: auto-rotate and fire
    if cheat_mode and not game_over:
        player_angle += 5  # Auto-rotate
        
        # Check if enemy is in line of sight and fire
        for enemy in enemies:
            angle_to_enemy = math.degrees(math.atan2(enemy[0]-player_pos[0], enemy[1]-player_pos[1]))
            if abs(angle_to_enemy - player_angle) < 15:  # If enemy is in sight
                bullets.append([player_pos[0], player_pos[1], 40, player_angle])
                break

def setupCamera():
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(fovY, 1.25, 0.1, 1500)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    
    if first_person:
        # First-person view (from player's perspective)
        eye_x = player_pos[0]
        eye_y = player_pos[1]
        eye_z = 50  # Eye level
        
        # Calculate look-at point based on player angle
        look_x = eye_x + math.sin(math.radians(player_angle))
        look_y = eye_y + math.cos(math.radians(player_angle))
        look_z = eye_z
        
        gluLookAt(eye_x, eye_y, eye_z,
                  look_x, look_y, look_z,
                  0, 0, 1)
    else:
        # Third-person view (orbiting camera)
        eye_x = player_pos[0] + camera_distance * math.sin(math.radians(camera_angle))
        eye_y = player_pos[1] + camera_distance * math.cos(math.radians(camera_angle))
        eye_z = camera_height
        
        gluLookAt(eye_x, eye_y, eye_z,
                  player_pos[0], player_pos[1], 0,
                  0, 0, 1)

def showScreen():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    glViewport(0, 0, 1000, 800)
    
    setupCamera()
    
    # Draw game elements
    draw_grid()
    draw_player()
    draw_enemies()
    draw_bullets()
    
    # Display game info
    draw_text(10, 770, f"Player Life Remaining: {player_lives}")
    draw_text(10, 740, f"Game Score: {game_score}")
    draw_text(10, 710, f"Player Bullet Missed: {bullets_missed}")
    
    if cheat_mode:
        draw_text(10, 680, "CHEAT MODE: ON", GLUT_BITMAP_HELVETICA_12)
    if cheat_vision and cheat_mode:
        draw_text(10, 660, "CHEAT VISION: ON", GLUT_BITMAP_HELVETICA_12)
    if game_over:
        draw_text(400, 400, "GAME OVER! Press R to restart", GLUT_BITMAP_TIMES_ROMAN_24)
    
    glutSwapBuffers()

def main():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(1000, 800)
    glutInitWindowPosition(0, 0)
    glutCreateWindow(b"Bullet Frenzy - 3D Game")
    
    glEnable(GL_DEPTH_TEST)
    init_game()
    
    glutDisplayFunc(showScreen)
    glutKeyboardFunc(keyboardListener)
    glutSpecialFunc(specialKeyListener)
    glutMouseFunc(mouseListener)
    glutIdleFunc(lambda: [update_game(), glutPostRedisplay()])
    
    glutMainLoop()

if __name__ == "__main__":
    main()