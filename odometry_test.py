import math

L = 26.0
B = 23.0
R = 4.95/2
N = 4000.0
cm_per_tick = 2.0 * math.pi * R / N

pos_x = 0
pos_y = 0
pos_h = 0
theta = 0
angle_turn = 0

old_A = 0
old_L = 0
old_R = 0

current_A = 0
current_L = 0
current_R = 0


def odometry(Aux, Right, Left):
    global old_A, old_L, old_R, \
        current_A, current_L, current_R, \
        pos_h, pos_x, pos_y, angle_turn

    old_A = current_A
    old_L = current_L
    old_R = current_R

    current_A = -Aux
    current_L = -Left
    current_R = Right

    dn1 = current_L - old_L
    dn2 = current_R - old_R
    dn3 = current_A - old_A

    dtheta = cm_per_tick * (dn2 - dn1) / L
    dx = cm_per_tick * (dn1 + dn2) / 2
    dy = cm_per_tick * (dn3 - (dn2 - dn1) * B / L)

    theta = pos_h * (dtheta/2)
    pos_x += dx * math.cos(theta) - dy * math.sin(theta)
    pos_y += dx * math.sin(theta) + dy * math.cos(theta)

    pos_h += dtheta
    angle_turn = pos_h * 180 / math.pi

    return pos_x, pos_y, angle_turn
