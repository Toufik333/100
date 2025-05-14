from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLUT.fonts import GLUT_BITMAP_HELVETICA_18
from OpenGL.GLU import *
import math
import random
import time

game_state = "MENU"
score = 0
lives = 3
start_time = 0
pause_time = 0
total_pause_time = 0
game_speed = 1.0
distance_traveled = 0
jump_state = False
jump_height = 0
crouch_state = False

coins = []
max_coins = 16
coin_spawn_distance = 1200
coin_min_distance = 200
coin_size = 15
coin_spin_speed = 5
coin_count = 0
coin_spin_angle = 0
last_coin_spawn_time = 0
coin_spawn_interval = 1.0

butterflies = []
max_butterflies = 24
butterfly_spawn_distance = 1800
butterfly_spawn_rate = 0.025
butterfly_min_distance = 400
wing_flap_angle = 0
wing_flap_speed = 3
last_butterfly_spawn_time = 0
butterfly_spawn_interval = 0.9

camera_pos = (0, -500, 200)
is_first_person = False
fovY = 90
ROAD_LENGTH = 40000
ROAD_WIDTH = 300

human_x = 0
human_y = -ROAD_LENGTH/2 + 200
human_z = 0
human_rotation = 0
lane_positions = [-ROAD_WIDTH/3, 0, ROAD_WIDTH/3]
current_lane = 1
lane_transition = 0
jump_time = 0
crouch_time = 0
player_height = 150 * 0.7
crouch_height = player_height * 0.5
jump_max_height = 180

butterfly_height_types = [
    "low",
    "middle",
    "high"
]

is_flying = False
fly_start_time = 0
fly_duration = 6.0
fly_height = 250
coins_for_fly = 10
fly_coins_counter = 0
fly_activated_once = False

trees = []
buildings = []

def init_environment():
    global trees, buildings
    for i in range(-ROAD_LENGTH//2, ROAD_LENGTH//2, 200):
        trees.append({
            'pos': [-ROAD_WIDTH/2 - 100, i, 0],
            'height': random.randint(100, 150),
            'trunk_radius': random.randint(5, 10),
            'crown_radius': random.randint(30, 50)
        })
        trees.append({
            'pos': [ROAD_WIDTH/2 + 100, i, 0],
            'height': random.randint(100, 150),
            'trunk_radius': random.randint(5, 10),
            'crown_radius': random.randint(30, 50)
        })
    for i in range(-ROAD_LENGTH//2, ROAD_LENGTH//2, 400):
        buildings.append({
            'pos': [-ROAD_WIDTH/2 - 250, i, 0],
            'width': random.randint(100, 150),
            'depth': random.randint(100, 150),
            'height': random.randint(150, 300),
            'color': [random.uniform(0.5, 0.9), random.uniform(0.5, 0.9), random.uniform(0.5, 0.9)]
        })
        buildings.append({
            'pos': [ROAD_WIDTH/2 + 250, i, 0],
            'width': random.randint(100, 150),
            'depth': random.randint(100, 150),
            'height': random.randint(150, 300),
            'color': [random.uniform(0.5, 0.9), random.uniform(0.5, 0.9), random.uniform(0.5, 0.9)]
        })

def draw_disk(radius, slices=24):
    glBegin(GL_TRIANGLE_FAN)
    glVertex3f(0, 0, 0)
    for i in range(slices + 1):
        angle = 2 * math.pi * i / slices
        x = radius * math.cos(angle)
        y = radius * math.sin(angle)
        glVertex3f(x, y, 0)
    glEnd()

def draw_butterfly(x, y, z, body_size, head_size, color, wing_angle):
    glPushMatrix()
    glTranslatef(x, y, z)
    glRotatef(90, 0, 0, 1)
    glColor3f(*color)
    gluSphere(gluNewQuadric(), body_size * 1.0, 10, 10)
    glPushMatrix()
    glTranslatef(body_size * 1.2, 0, 0)
    gluSphere(gluNewQuadric(), head_size * 1.2, 10, 10)
    glPopMatrix()
    glPushMatrix()
    glColor3f(0.0, 0.0, 0.0)
    glTranslatef(-body_size * 1.5, 0, 0)
    gluSphere(gluNewQuadric(), body_size * 0.5, 8, 8)
    glPopMatrix()
    glColor3f(color[0] + 0.2, color[1] + 0.2, color[2] + 0.2)
    glPushMatrix()
    glRotatef(wing_angle, 0, 0, 1)
    glBegin(GL_TRIANGLES)
    glVertex3f(-body_size * 0.4, 0, 0)
    glVertex3f(-body_size * 1.6, body_size * 1.2, 0)
    glVertex3f(-body_size * 1.6, -body_size * 1.2, 0)
    glEnd()
    glPopMatrix()
    glPushMatrix()
    glRotatef(-wing_angle, 0, 0, 1)
    glBegin(GL_TRIANGLES)
    glVertex3f(-body_size * 0.4, 0, 0)
    glVertex3f(-body_size * 1.6, body_size * 1.2, 0)
    glVertex3f(-body_size * 1.6, -body_size * 1.2, 0)
    glEnd()
    glPopMatrix()
    glPopMatrix()

def draw_butterflies():
    global wing_flap_angle, butterflies
    wing_flap_angle = (wing_flap_angle + wing_flap_speed) % 60
    flap_angle = 30 + 30 * math.sin(wing_flap_angle * math.pi / 30)
    for butterfly in butterflies:
        x, y, z, body_size, head_size, color, height_type = butterfly
        draw_butterfly(x, y, z, body_size, head_size, color, flap_angle)

def spawn_butterfly():
    global butterflies, last_butterfly_spawn_time
    current_time = time.time()
    if len(butterflies) < max_butterflies and (current_time - last_butterfly_spawn_time) >= butterfly_spawn_interval:
        lane = random.randint(0, 2)
        lane_x = lane_positions[lane]
        height_type = random.choice(butterfly_height_types)
        body_size = random.uniform(15, 22)
        head_size = body_size * 0.5
        scale_factor = 0.7
        head_center_z = 325/3 * scale_factor
        if height_type == "low":
            z = random.uniform(5, 20)
        elif height_type == "middle":
            z = random.uniform(player_height * 0.5, player_height * 0.6)
        else:
            z = random.uniform(player_height * 0.8, head_center_z)
        patriotic_colors = [
            (1.0, 0.0, 0.0),
            (1.0, 1.0, 1.0),
            (0.0, 0.0, 1.0)
        ]
        color = random.choice(patriotic_colors)
        y = human_y + butterfly_spawn_distance
        butterflies.append([lane_x, y, z, body_size, head_size, color, height_type])
        last_butterfly_spawn_time = current_time

def update_butterflies():
    global butterflies, score, lives, game_state
    butterflies_to_remove = []
    for i, butterfly in enumerate(butterflies):
        x, y, z, body_size, head_size, color, height_type = butterfly
        butterfly[1] -= 10 * game_speed
        if butterfly[1] < human_y - 200:
            butterflies_to_remove.append(i)
            score += 2
            continue
        scale_factor = 0.7
        head_center_z = human_z + 325/3 * scale_factor
        head_radius = 50/3 * scale_factor
        collision = False
        if (
            abs(human_x - butterfly[0]) < 30 and
            abs(human_y - butterfly[1]) < 30
        ):
            if height_type == "high":
                dz = abs(z - head_center_z)
                if dz < head_radius + body_size * 0.5:
                    collision = True
            else:
                if abs(human_z - z) < 50:
                    collision = True
        if collision:
            lives -= 1
            butterflies_to_remove.append(i)
            if lives <= 0:
                game_state = "GAME_OVER"
            break
    for i in sorted(butterflies_to_remove, reverse=True):
        if i < len(butterflies):
            butterflies.pop(i)

def draw_coin(x, y, z, rotation, wobble):
    glPushMatrix()
    glTranslatef(x, y, z)
    glRotatef(90, 1, 0, 0)
    glRotatef(90, 0, 1, 0)
    glRotatef(rotation, 0, 0, 1)
    glRotatef(wobble * 0.2, 1, 0, 0)
    gold_color = (1.0, 0.84, 0.0)
    glColor3f(*gold_color)
    coin_thickness = 3.5
    draw_disk(coin_size, 24)
    gluCylinder(gluNewQuadric(), coin_size, coin_size * 0.9, coin_thickness * 0.2, 24, 1)
    glTranslatef(0, 0, coin_thickness * 0.2)
    gluCylinder(gluNewQuadric(), coin_size * 0.9, coin_size * 0.9, coin_thickness * 0.6, 24, 1)
    glTranslatef(0, 0, coin_thickness * 0.6)
    gluCylinder(gluNewQuadric(), coin_size * 0.9, coin_size, coin_thickness * 0.2, 24, 1)
    glTranslatef(0, 0, coin_thickness * 0.2)
    draw_disk(coin_size, 24)
    glPopMatrix()

def draw_coins():
    global coin_spin_angle, coins
    coin_spin_angle = (coin_spin_angle + coin_spin_speed) % 360
    for coin in coins:
        x, y, z, rotation, wobble = coin
        draw_coin(x, y, z, rotation + coin_spin_angle, wobble)

def spawn_coin():
    global coins, last_coin_spawn_time
    current_time = time.time()
    if is_flying:
        flying_coin_spawn_interval = 0.25
        flying_max_coins = max_coins * 2
        spawn_interval = flying_coin_spawn_interval
        max_spawn = flying_max_coins
    else:
        spawn_interval = coin_spawn_interval
        max_spawn = max_coins
    if len(coins) < max_spawn and (current_time - last_coin_spawn_time) >= spawn_interval:
        lane = random.randint(0, 2)
        lane_x = lane_positions[lane]
        scale_factor = 0.7
        cuboid_center = 200/3 * scale_factor
        if is_flying:
            z = fly_height
        else:
            if random.random() < 0.2:
                z = fly_height
            else:
                z = cuboid_center
        rotation = random.uniform(0, 360)
        wobble = random.uniform(0, 360)
        y = human_y + coin_spawn_distance
        coins.append([lane_x, y, z, rotation, wobble])
        last_coin_spawn_time = current_time

def update_coins():
    global coins, score, coin_count, fly_coins_counter, is_flying, fly_start_time
    global coins_for_fly, fly_activated_once
    coins_to_remove = []
    for i, coin in enumerate(coins):
        x, y, z, rotation, wobble = coin
        coin[1] -= 10 * game_speed
        coin[3] = (coin[3] + coin_spin_speed) % 360
        if coin[1] < human_y - 200:
            coins_to_remove.append(i)
            continue
        distance_x = abs(human_x - coin[0])
        distance_y = abs(human_y - coin[1])
        distance_z = abs(human_z - coin[2])
        if distance_x < 50 and distance_y < 50 and distance_z < 60:
            print(f"Coin collected! Count: {coin_count} -> {coin_count + 1}")
            coin_count += 1
            score += 5
            fly_coins_counter += 1
            if fly_coins_counter >= coins_for_fly and not is_flying:
                is_flying = True
                fly_start_time = time.time()
                fly_coins_counter = 0
                if not fly_activated_once:
                    fly_activated_once = True
                    coins_for_fly = 15
            coins_to_remove.append(i)
            glutPostRedisplay()
    for i in sorted(coins_to_remove, reverse=True):
        if i < len(coins):
            coins.pop(i)

def draw_tree(x, y, z, trunk_height, trunk_radius, crown_radius):
    glPushMatrix()
    glColor3f(0.55, 0.27, 0.07)
    glTranslatef(x, y, z)
    glRotatef(0, 1, 0, 0)
    gluCylinder(gluNewQuadric(), trunk_radius, trunk_radius, trunk_height, 10, 10)
    glPopMatrix()
    glPushMatrix()
    glColor3f(0.0, 0.5, 0.0)
    glTranslatef(x, y, z + trunk_height)
    gluSphere(gluNewQuadric(), crown_radius, 10, 10)
    glPopMatrix()

def draw_building(x, y, z, width, depth, height, color):
    glPushMatrix()
    glColor3f(color[0], color[1], color[2])
    glTranslatef(x, y, z + height/2)
    draw_rectangular_cuboid(width, depth, height)
    glPopMatrix()

def draw_text(x, y, text, font=GLUT_BITMAP_HELVETICA_18):
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    gluOrtho2D(0, 1000, 0, 800)
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()
    glColor3f(1.0, 1.0, 1.0)
    glRasterPos2f(x, y)
    for ch in text:
        glutBitmapCharacter(font, ord(ch))
    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)

def draw_human(x=0, y=0, z=0, rotation=90):
    glPushMatrix()
    glTranslatef(x, y, z)
    glRotatef(rotation, 0, 0, 1)
    if is_flying:
        glPushMatrix()
        glColor3f(0, 0, 0)
        glTranslatef(0, 0, -z)
        draw_disk(40, 20)
        glPopMatrix()
        glRotatef(90, 1, 0, 0)
        scale_factor = 0.7
        glPushMatrix()
        glColor3f(1, 0, 0)
        glTranslatef(0, -90/3 * scale_factor, 0)
        glPushMatrix()
        glTranslatef(-15/3 * scale_factor, 0, 0)
        gluCylinder(gluNewQuadric(), 25/3 * scale_factor, 15/3 * scale_factor, 200/3 * scale_factor, 10, 10)
        glPopMatrix()
        glPushMatrix()
        glTranslatef(15/3 * scale_factor, 0, 0)
        gluCylinder(gluNewQuadric(), 25/3 * scale_factor, 15/3 * scale_factor, 200/3 * scale_factor, 10, 10)
        glPopMatrix()
        glPopMatrix()
        glPushMatrix()
        glColor3f(0, 1, 0)
        draw_rectangular_cuboid(200/3 * scale_factor * 0.8, 180/3 * scale_factor, 50/3 * scale_factor)
        glPopMatrix()
        glPushMatrix()
        glColor3f(0, 0, 1)
        glTranslatef(0, 140/3 * scale_factor, 30/3 * scale_factor)
        gluSphere(gluNewQuadric(), 50/3 * scale_factor, 10, 10)
        glPopMatrix()
        glPushMatrix()
        glColor3f(1, 0.5, 0)
        glTranslatef(-60/3 * scale_factor, 200/3 * scale_factor, 0)
        glRotatef(90, 1, 0, 0)
        gluCylinder(gluNewQuadric(), 12/3 * scale_factor, 12/3 * scale_factor, 130/3 * scale_factor, 12, 12)
        glPopMatrix()
        glPushMatrix()
        glColor3f(1, 0.5, 0)
        glTranslatef(60/3 * scale_factor, 200/3 * scale_factor, 0)
        glRotatef(90, 1, 0, 0)
        gluCylinder(gluNewQuadric(), 12/3 * scale_factor, 12/3 * scale_factor, 130/3 * scale_factor, 12, 12)
        glPopMatrix()
    else:
        crouch_factor = 0.5 if crouch_state else 1.0
        scale_factor = 0.7
        glPushMatrix()
        glColor3f(1, 0, 0)
        glTranslatef(50/3 * scale_factor, 0, 0)
        gluCylinder(gluNewQuadric(), 15/3 * scale_factor, 40/3 * scale_factor, 150/3 * crouch_factor * scale_factor, 10, 10)
        glPopMatrix()
        glPushMatrix()
        glColor3f(1, 0, 0)
        glTranslatef(-50/3 * scale_factor, 0, 0)
        gluCylinder(gluNewQuadric(), 15/3 * scale_factor, 40/3 * scale_factor, 150/3 * crouch_factor * scale_factor, 10, 10)
        glPopMatrix()
        glPushMatrix()
        glColor3f(0, 1, 0)
        glTranslatef(0, 0, 200/3 * crouch_factor * scale_factor)
        draw_rectangular_cuboid(200/3 * scale_factor * 0.8, 50/3 * scale_factor, 180/3 * crouch_factor * scale_factor)
        glPopMatrix()
        glPushMatrix()
        glColor3f(0, 0, 1)
        glTranslatef(0, 0, 325/3 * crouch_factor * scale_factor)
        gluSphere(gluNewQuadric(), 50/3 * scale_factor, 10, 10)
        glPopMatrix()
        glPushMatrix()
        glColor3f(1, 0.5, 0)
        glTranslatef(120/3 * scale_factor * 0.8, 0, 250/3 * crouch_factor * scale_factor)
        glRotatef(-90, 1, 0, 0)
        gluCylinder(gluNewQuadric(), 5/3 * scale_factor, 20/3 * scale_factor, 120/3 * scale_factor, 10, 10)
        glPopMatrix()
        glPushMatrix()
        glColor3f(1, 0.5, 0)
        glTranslatef(-120/3 * scale_factor * 0.8, 0, 250/3 * crouch_factor * scale_factor)
        glRotatef(-90, 1, 0, 0)
        gluCylinder(gluNewQuadric(), 5/3 * scale_factor, 20/3 * scale_factor, 120/3 * scale_factor, 10, 10)
        glPopMatrix()
    glPopMatrix()

def draw_rectangular_cuboid(width, height, depth):
    half_width = width / 2
    half_height = height / 2
    half_depth = depth / 2
    glBegin(GL_QUADS)
    glVertex3f(-half_width, -half_height, half_depth)
    glVertex3f(half_width, -half_height, half_depth)
    glVertex3f(half_width, half_height, half_depth)
    glVertex3f(-half_width, half_height, half_depth)
    glEnd()
    glBegin(GL_QUADS)
    glVertex3f(-half_width, -half_height, -half_depth)
    glVertex3f(half_width, -half_height, -half_depth)
    glVertex3f(half_width, half_height, -half_depth)
    glVertex3f(-half_width, half_height, -half_depth)
    glEnd()
    glBegin(GL_QUADS)
    glVertex3f(-half_width, half_height, half_depth)
    glVertex3f(half_width, half_height, half_depth)
    glVertex3f(half_width, half_height, -half_depth)
    glVertex3f(-half_width, half_height, -half_depth)
    glEnd()
    glBegin(GL_QUADS)
    glVertex3f(-half_width, -half_height, half_depth)
    glVertex3f(half_width, -half_height, half_depth)
    glVertex3f(half_width, -half_height, -half_depth)
    glVertex3f(-half_width, -half_height, -half_depth)
    glEnd()
    glBegin(GL_QUADS)
    glVertex3f(half_width, -half_height, half_depth)
    glVertex3f(half_width, -half_height, -half_depth)
    glVertex3f(half_width, half_height, -half_depth)
    glVertex3f(half_width, half_height, half_depth)
    glEnd()
    glBegin(GL_QUADS)
    glVertex3f(-half_width, -half_height, half_depth)
    glVertex3f(-half_width, -half_height, -half_depth)
    glVertex3f(-half_width, half_height, -half_depth)
    glVertex3f(-half_width, half_height, half_depth)
    glEnd()

def keyboardListener(key, x, y):
    global human_x, human_y, current_lane, jump_state, jump_time, crouch_state, crouch_time
    global game_state, score, lives, start_time, game_speed, distance_traveled
    global pause_time, total_pause_time, butterflies
    global is_flying
    global is_first_person

    if key == b' ' and game_state == "MENU":
        game_state = "PLAYING"
        score = 0
        lives = 3
        start_time = time.time()
        total_pause_time = 0
        game_speed = 1.0
        distance_traveled = 0
        human_y = -ROAD_LENGTH/2 + 200
        current_lane = 1
        butterflies = []
        return

    if (key == b'p' or key == b'\b') and (game_state == "PLAYING" or game_state == "PAUSED"):
        if game_state == "PLAYING":
            game_state = "PAUSED"
            pause_time = time.time()
        else:
            game_state = "PLAYING"
            total_pause_time += time.time() - pause_time
        return

    if key == b'r' and (game_state == "GAME_OVER" or game_state == "WIN"):
        game_state = "MENU"
        return

    if key == b'\x1b':
        exit(0)
        return

    if game_state != "PLAYING":
        return

    if key == b'a' and current_lane > 0:
        current_lane -= 1

    if key == b'd' and current_lane < 2:
        current_lane += 1

    if not is_flying:
        if key == b'w' and not jump_state and not crouch_state:
            jump_state = True
            jump_time = time.time()
        if key == b's' and not jump_state and not crouch_state:
            crouch_state = True
            crouch_time = time.time()

    if key == b'c':
        is_first_person = not is_first_person

def specialKeyListener(key, x, y):
    global camera_pos, game_state
    x_pos, y_pos, z_pos = camera_pos

    if key == GLUT_KEY_UP:
        z_pos += 10
    if key == GLUT_KEY_DOWN:
        z_pos -= 10
    if key == GLUT_KEY_LEFT:
        x_pos -= 10
    if key == GLUT_KEY_RIGHT:
        x_pos += 10

    camera_pos = (x_pos, y_pos, z_pos)

def mouseListener(button, state, x, y):
    pass

def setupCamera():
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    if is_first_person:
        gluPerspective(fovY, 1.25, 5.0, 5000)
    else:
        gluPerspective(fovY, 1.25, 0.1, 5000)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    if is_first_person:
        scale_factor = 0.7
        camera_offset = -15
        if is_flying:
            camera_x = human_x
            camera_y = human_y + 140/3 * scale_factor + camera_offset
            camera_z = human_z + 30/3 * scale_factor - 10
            look_x = human_x
            look_y = human_y + 500
            look_z = camera_z - 10
        else:
            camera_x = human_x
            camera_y = human_y + camera_offset
            head_height = 325/4 * (0.5 if crouch_state else 1.0) * scale_factor
            camera_z = human_z + head_height + 50
            look_x = human_x
            look_y = human_y + 500
            look_z = camera_z
        gluLookAt(
            camera_x, camera_y, camera_z,
            look_x, look_y, look_z,
            0, 0, 1
        )
    else:
        gluLookAt(
            human_x + camera_pos[0], human_y + camera_pos[1], human_z + camera_pos[2],
            human_x, human_y + 300, human_z + 50,
            0, 0, 1
        )

def update_game():
    global human_x, human_y, human_z, jump_state, jump_height, crouch_state, game_speed, score, distance_traveled
    global is_flying, fly_start_time

    if game_state != "PLAYING":
        return

    target_x = lane_positions[current_lane]
    human_x += (target_x - human_x) * 0.2

    if is_flying:
        human_z = fly_height
        if time.time() - fly_start_time >= fly_duration:
            is_flying = False
            human_z = 0
    else:
        if jump_state:
            jump_duration = time.time() - jump_time
            if jump_duration < 1.0:
                jump_height = jump_max_height * math.sin(jump_duration * math.pi)
                human_z = jump_height
            else:
                jump_state = False
                human_z = 0
        if crouch_state:
            crouch_duration = time.time() - crouch_time
            if crouch_duration >= 0.5:
                crouch_state = False

    forward_speed = 10 * game_speed
    human_y += forward_speed
    distance_traveled += forward_speed

    if human_y >= ROAD_LENGTH/2 - 500:
        human_y = -ROAD_LENGTH/2 + 500


    elapsed_time = time.time() - start_time - total_pause_time
    game_speed = min(2.0, 1.0 + elapsed_time / 45.0)

    update_butterflies()
    spawn_butterfly()
    update_coins()
    spawn_coin()

def idle():
    update_game()
    glutPostRedisplay()

def draw_road():
    glColor3f(0.2, 0.2, 0.2)
    glBegin(GL_QUADS)
    glVertex3f(-ROAD_WIDTH/2, -ROAD_LENGTH/2, 0)
    glVertex3f(ROAD_WIDTH/2, -ROAD_LENGTH/2, 0)
    glVertex3f(ROAD_WIDTH/2, ROAD_LENGTH/2, 0)
    glVertex3f(-ROAD_WIDTH/2, ROAD_LENGTH/2, 0)
    glEnd()

    glColor3f(1, 1, 1)
    num_lines = int(ROAD_LENGTH / 50)

    for i in range(num_lines):
        line_pos = -ROAD_LENGTH/2 + i * 50
        if i % 2 == 0:
            glBegin(GL_QUADS)
            glVertex3f(-5, line_pos, 1)
            glVertex3f(5, line_pos, 1)
            glVertex3f(5, line_pos + 30, 1)
            glVertex3f(-5, line_pos + 30, 1)
            glEnd()

    glBegin(GL_QUADS)
    glVertex3f(-ROAD_WIDTH/2, -ROAD_LENGTH/2, 1)
    glVertex3f(-ROAD_WIDTH/2 + 5, -ROAD_LENGTH/2, 1)
    glVertex3f(-ROAD_WIDTH/2 + 5, ROAD_LENGTH/2, 1)
    glVertex3f(-ROAD_WIDTH/2, ROAD_LENGTH/2, 1)
    glVertex3f(ROAD_WIDTH/2 - 5, -ROAD_LENGTH/2, 1)
    glVertex3f(ROAD_WIDTH/2, -ROAD_LENGTH/2, 1)
    glVertex3f(ROAD_WIDTH/2, ROAD_LENGTH/2, 1)
    glVertex3f(ROAD_WIDTH/2 - 5, ROAD_LENGTH/2, 1)
    glEnd()

    lane_width = ROAD_WIDTH / 3

    for i in range(num_lines):
        line_pos = -ROAD_LENGTH/2 + i * 50
        if i % 2 == 0:
            glBegin(GL_QUADS)
            glVertex3f(-lane_width/2 - 2.5, line_pos, 1)
            glVertex3f(-lane_width/2 + 2.5, line_pos, 1)
            glVertex3f(-lane_width/2 + 2.5, line_pos + 30, 1)
            glVertex3f(-lane_width/2 - 2.5, line_pos + 30, 1)
            glEnd()

    for i in range(num_lines):
        line_pos = -ROAD_LENGTH/2 + i * 50
        if i % 2 == 0:
            glBegin(GL_QUADS)
            glVertex3f(lane_width/2 - 2.5, line_pos, 1)
            glVertex3f(lane_width/2 + 2.5, line_pos, 1)
            glVertex3f(lane_width/2 + 2.5, line_pos + 30, 1)
            glVertex3f(lane_width/2 - 2.5, line_pos + 30, 1)
            glEnd()

    glColor3f(1, 1, 0)
    glBegin(GL_QUADS)
    glVertex3f(-ROAD_WIDTH/2, -ROAD_LENGTH/2 + 100, 1)
    glVertex3f(ROAD_WIDTH/2, -ROAD_LENGTH/2 + 100, 1)
    glVertex3f(ROAD_WIDTH/2, -ROAD_LENGTH/2 + 110, 1)
    glVertex3f(-ROAD_WIDTH/2, -ROAD_LENGTH/2 + 110, 1)
    glEnd()

    glColor3f(1, 0, 0)
    glBegin(GL_QUADS)
    glVertex3f(-ROAD_WIDTH/2, ROAD_LENGTH/2 - 100, 1)
    glVertex3f(ROAD_WIDTH/2, ROAD_LENGTH/2 - 100, 1)
    glVertex3f(ROAD_WIDTH/2, ROAD_LENGTH/2 - 90, 1)
    glVertex3f(-ROAD_WIDTH/2, ROAD_LENGTH/2 - 90, 1)
    glEnd()

def draw_environment():
    global trees, buildings

    for tree in trees:
        draw_tree(tree['pos'][0], tree['pos'][1], tree['pos'][2],
                 tree['height'], tree['trunk_radius'], tree['crown_radius'])

    for building in buildings:
        draw_building(building['pos'][0], building['pos'][1], building['pos'][2],
                     building['width'], building['depth'], building['height'],
                     building['color'])

def draw_game_info():
    global coin_count
    if game_state == "MENU":
        coin_count = 0
        glMatrixMode(GL_PROJECTION)
        glPushMatrix()
        glLoadIdentity()
        gluOrtho2D(0, 1000, 0, 800)

        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glLoadIdentity()

        glColor3f(0.0, 0.0, 0.0)
        glBegin(GL_QUADS)
        glVertex3f(300, 420, 0)
        glVertex3f(700, 420, 0)
        glVertex3f(700, 100, 0)
        glVertex3f(300, 100, 0)
        glEnd()

        glPopMatrix()
        glMatrixMode(GL_PROJECTION)
        glPopMatrix()
        glMatrixMode(GL_MODELVIEW)

        draw_text(350, 400, "Dodge the obstacles", GLUT_BITMAP_HELVETICA_18)
        draw_text(380, 350, "Press SPACE to start", GLUT_BITMAP_HELVETICA_18)
        draw_text(320, 300, "CONTROLS:", GLUT_BITMAP_HELVETICA_18)
        draw_text(320, 270, "W - Jump", GLUT_BITMAP_HELVETICA_18)
        draw_text(320, 240, "S - Crouch", GLUT_BITMAP_HELVETICA_18)
        draw_text(320, 210, "A - Move Left", GLUT_BITMAP_HELVETICA_18)
        draw_text(320, 180, "D - Move Right", GLUT_BITMAP_HELVETICA_18)
        draw_text(320, 150, "P- Pause/Resume", GLUT_BITMAP_HELVETICA_18)
        draw_text(320, 120, "C - Toggle First-Person View", GLUT_BITMAP_HELVETICA_18)
        return

    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    gluOrtho2D(0, 1000, 0, 800)

    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()

    glColor3f(0.0, 0.0, 0.0)
    glBegin(GL_QUADS)
    glVertex3f(5, 685, 0)
    glVertex3f(305, 685, 0)
    glVertex3f(305, 555, 0)
    glVertex3f(5, 555, 0)
    glEnd()

    glColor3f(0.2, 0.2, 0.7)
    glBegin(GL_QUADS)
    glVertex3f(10, 680, 0)
    glVertex3f(300, 680, 0)
    glVertex3f(300, 560, 0)
    glVertex3f(10, 560, 0)
    glEnd()

    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)

    draw_text(20, 660, f"SCORE: {score}", GLUT_BITMAP_HELVETICA_18)
    draw_text(20, 630, f"LIVES: {lives}", GLUT_BITMAP_HELVETICA_18)
    draw_text(20, 600, f"SPEED: {game_speed:.1f}x", GLUT_BITMAP_HELVETICA_18)
    draw_text(20, 570, f"COINS: {coin_count}", GLUT_BITMAP_HELVETICA_18)

    if game_state == "PAUSED":
        glMatrixMode(GL_PROJECTION)
        glPushMatrix()
        glLoadIdentity()
        gluOrtho2D(0, 1000, 0, 800)

        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glLoadIdentity()

        glColor3f(0.0, 0.0, 0.0)
        glBegin(GL_QUADS)
        glVertex3f(0, 0, 0)
        glVertex3f(1000, 0, 0)
        glVertex3f(1000, 800, 0)
        glVertex3f(0, 800, 0)
        glEnd()

        glPopMatrix()
        glMatrixMode(GL_PROJECTION)
        glPopMatrix()
        glMatrixMode(GL_MODELVIEW)

        draw_text(400, 400, "GAME PAUSED", GLUT_BITMAP_HELVETICA_18)
        draw_text(350, 350, "Press P or Backspace to resume", GLUT_BITMAP_HELVETICA_18)

    if game_state == "GAME_OVER":
        glMatrixMode(GL_PROJECTION)
        glPushMatrix()
        glLoadIdentity()
        gluOrtho2D(0, 1000, 0, 800)

        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glLoadIdentity()

        glColor3f(0.0, 0.0, 0.0)
        glBegin(GL_QUADS)
        glVertex3f(300, 420, 0)
        glVertex3f(700, 420, 0)
        glVertex3f(700, 280, 0)
        glVertex3f(300, 280, 0)
        glEnd()

        glPopMatrix()
        glMatrixMode(GL_PROJECTION)
        glPopMatrix()
        glMatrixMode(GL_MODELVIEW)

        draw_text(400, 400, "GAME OVER", font=GLUT_BITMAP_HELVETICA_18)
        draw_text(380, 350, f"Final Score: {score}", GLUT_BITMAP_HELVETICA_18)
        draw_text(390, 300, "Press R to restart", GLUT_BITMAP_HELVETICA_18)

def showScreen():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    glViewport(0, 0, 1000, 800)

    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    gluOrtho2D(0, 1, 0, 1)

    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()

    if game_state == "PLAYING" or game_state == "MENU" or game_state == "PAUSED":
        glColor3f(0, 1.0, 1.0)
    elif game_state == "GAME_OVER":
        glColor3f(0.5, 0.0, 0.0)

    glBegin(GL_QUADS)
    glVertex3f(0, 0, 0)
    glVertex3f(1, 0, 0)
    glVertex3f(1, 1, 0)
    glVertex3f(0, 1, 0)
    glEnd()

    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)

    setupCamera()

    draw_road()
    draw_environment()
    draw_butterflies()
    draw_coins()
    draw_human(human_x, human_y, human_z, human_rotation)
    draw_game_info()

    glutSwapBuffers()

def main():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(1000, 800)
    glutInitWindowPosition(0, 0)
    wind = glutCreateWindow(b"Dodge the obstacles")

    init_environment()

    glutDisplayFunc(showScreen)
    glutKeyboardFunc(keyboardListener)
    glutSpecialFunc(specialKeyListener)
    glutMouseFunc(mouseListener)
    glutIdleFunc(idle)

    glutMainLoop()

if __name__ == "__main__":
    main()