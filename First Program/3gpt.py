from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import math
import random

# Global Variables
camera_pos = (0, 500, 500)
fovY = 120
GRID_LENGTH = 600
player_pos = [0, 0, 0]
player_angle = 0  # In degrees
bullets = []
enemies = []
cheat_mode = False
first_person = False
life = 5
score = 0
missed_bullets = 0
max_missed = 10
rand_var = 423

# Bullet Class
class Bullet:
    def __init__(self, x, y, z, angle):
        self.x = x
        self.y = y
        self.z = z
        self.angle = angle

    def move(self):
        speed = 10
        rad = math.radians(self.angle)
        self.x += speed * math.cos(rad)
        self.y += speed * math.sin(rad)

# Enemy Class
class Enemy:
    def __init__(self):
        self.respawn()

    def respawn(self):
        self.x = random.randint(-500, 500)
        self.y = random.randint(-500, 500)
        self.z = 0
        self.scale = 1
        self.scale_dir = 1

    def move_towards_player(self):
        dx = player_pos[0] - self.x
        dy = player_pos[1] - self.y
        dist = math.hypot(dx, dy)
        if dist > 0:
            self.x += (dx / dist) * 2
            self.y += (dy / dist) * 2

    def animate(self):
        self.scale += 0.01 * self.scale_dir
        if self.scale >= 1.2 or self.scale <= 0.8:
            self.scale_dir *= -1

# Initialize enemies
def init_enemies():
    for _ in range(5):
        enemies.append(Enemy())

def draw_text(x, y, text, font=GLUT_BITMAP_HELVETICA_18):
    glColor3f(1,1,1)
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

def draw_player():
    glPushMatrix()
    glTranslatef(player_pos[0], player_pos[1], player_pos[2])
    glRotatef(player_angle, 0, 0, 1)

    glColor3f(1, 0, 0)
    glutSolidCube(30)

    glTranslatef(0, 30, 0)
    glColor3f(0, 1, 0)
    gluCylinder(gluNewQuadric(), 10, 5, 40, 10, 10)

    glTranslatef(0, 40, 0)
    glColor3f(0, 0, 1)
    gluSphere(gluNewQuadric(), 15, 10, 10)

    glPopMatrix()

def draw_bullets():
    global bullets
    for bullet in bullets:
        glPushMatrix()
        glTranslatef(bullet.x, bullet.y, bullet.z)
        glColor3f(1,1,0)
        glutSolidCube(5)
        glPopMatrix()

def draw_enemies():
    for enemy in enemies:
        glPushMatrix()
        glTranslatef(enemy.x, enemy.y, enemy.z)
        glScalef(enemy.scale, enemy.scale, enemy.scale)
        glColor3f(0,1,1)
        gluSphere(gluNewQuadric(), 20, 10, 10)
        glTranslatef(0, 0, 30)
        gluSphere(gluNewQuadric(), 10, 10, 10)
        glPopMatrix()

def draw_grid():
    glBegin(GL_QUADS)
    glColor3f(1, 1, 1)
    glVertex3f(-GRID_LENGTH, GRID_LENGTH, 0)
    glVertex3f(GRID_LENGTH, GRID_LENGTH, 0)
    glVertex3f(GRID_LENGTH, -GRID_LENGTH, 0)
    glVertex3f(-GRID_LENGTH, -GRID_LENGTH, 0)
    glEnd()

def keyboardListener(key, x, y):
    global player_pos, player_angle, cheat_mode, first_person, life, score, missed_bullets, bullets, enemies

    if key == b'w':
        rad = math.radians(player_angle)
        player_pos[0] += 10 * math.cos(rad)
        player_pos[1] += 10 * math.sin(rad)
    if key == b's':
        rad = math.radians(player_angle)
        player_pos[0] -= 10 * math.cos(rad)
        player_pos[1] -= 10 * math.sin(rad)
    if key == b'a':
        player_angle += 5
    if key == b'd':
        player_angle -= 5
    if key == b'c':
        global cheat_mode
        cheat_mode = not cheat_mode
    if key == b'r':
        life = 5
        score = 0
        missed_bullets = 0
        player_pos[0] = player_pos[1] = 0
        bullets.clear()
        enemies.clear()
        init_enemies()

def mouseListener(button, state, x, y):
    global first_person
    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        fire_bullet()
    if button == GLUT_RIGHT_BUTTON and state == GLUT_DOWN:
        first_person = not first_person

def fire_bullet():
    global bullets
    bullets.append(Bullet(player_pos[0], player_pos[1], player_pos[2], player_angle))

def update_game():
    global bullets, enemies, score, life, missed_bullets

    for bullet in bullets:
        bullet.move()

    for enemy in enemies:
        enemy.move_towards_player()
        enemy.animate()

    new_bullets = []
    for bullet in bullets:
        hit = False
        for enemy in enemies:
            dist = math.hypot(bullet.x - enemy.x, bullet.y - enemy.y)
            if dist < 25:
                enemy.respawn()
                score += 1
                hit = True
                break
        if not hit and -GRID_LENGTH < bullet.x < GRID_LENGTH and -GRID_LENGTH < bullet.y < GRID_LENGTH:
            new_bullets.append(bullet)
        elif not hit:
            missed_bullets += 1
    bullets = new_bullets

    for enemy in enemies:
        dist = math.hypot(player_pos[0] - enemy.x, player_pos[1] - enemy.y)
        if dist < 30:
            life -= 1
            enemy.respawn()

    if cheat_mode:
        player_angle += 2
        fire_bullet()

def setupCamera():
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(fovY, 1.25, 0.1, 1500)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    x, y, z = camera_pos
    if first_person:
        gluLookAt(player_pos[0]-100*math.cos(math.radians(player_angle)),
                  player_pos[1]-100*math.sin(math.radians(player_angle)),
                  100,
                  player_pos[0], player_pos[1], 50,
                  0, 0, 1)
    else:
        gluLookAt(x, y, z, 0, 0, 0, 0, 0, 1)

def showScreen():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    glViewport(0, 0, 1000, 800)

    setupCamera()

    draw_grid()
    draw_player()
    draw_bullets()
    draw_enemies()

    draw_text(10, 770, f"Life: {life}  Score: {score}  Missed: {missed_bullets}")

    glutSwapBuffers()

def idle():
    update_game()
    glutPostRedisplay()

def main():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(1000, 800)
    glutInitWindowPosition(0, 0)
    glutCreateWindow(b"3D Bullet Frenzy")

    glEnable(GL_DEPTH_TEST)

    init_enemies()

    glutDisplayFunc(showScreen)
    glutKeyboardFunc(keyboardListener)
    glutMouseFunc(mouseListener)
    glutIdleFunc(idle)

    glutMainLoop()

if __name__ == "__main__":
    main()
