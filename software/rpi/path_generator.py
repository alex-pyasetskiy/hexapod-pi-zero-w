from lib import semicircle_generator, semicircle2_generator
from lib import path_rotate_z
from lib import get_rotate_x_matrix, get_rotate_y_matrix, get_rotate_z_matrix
import numpy as np
from collections import deque


def gen_forward_path(standby_coordinate, g_steps=20, g_radius=25):
    assert (g_steps % 4) == 0

    halfsteps = int(g_steps/2)

    path = np.zeros((g_steps, 6, 3))

    semi_circle = semicircle_generator(g_radius, g_steps)

    path[:, [0, 2, 4], :] = np.tile(semi_circle[:, np.newaxis, :], (1, 3, 1))
    path[:, [1, 3, 5], :] = np.tile(
        np.roll(semi_circle[:, np.newaxis, :], halfsteps, axis=0), (1, 3, 1))

    return path+np.tile(standby_coordinate, (g_steps, 1, 1))


def gen_backward_path(standby_coordinate, g_steps=20, g_radius=25):
    assert (g_steps % 4) == 0

    halfsteps = int(g_steps/2)

    path = np.zeros((g_steps, 6, 3))

    semi_circle = semicircle_generator(g_radius, g_steps, reverse=True)

    path[:, [0, 2, 4], :] = np.tile(semi_circle[:, np.newaxis, :], (1, 3, 1))
    path[:, [1, 3, 5], :] = np.tile(
        np.roll(semi_circle[:, np.newaxis, :], halfsteps, axis=0), (1, 3, 1))

    return path+np.tile(standby_coordinate, (g_steps, 1, 1))


def gen_fastforward_path(standby_coordinate,g_steps = 20, y_radius = 50, z_radius = 30, x_radius = 10):
    assert (g_steps % 2) == 0

    halfsteps = int(g_steps/2)

    path = np.zeros((g_steps, 6, 3))
    semi_circle_r = semicircle2_generator(
        g_steps, y_radius, z_radius, x_radius)
    semi_circle_l = semicircle2_generator(
        g_steps, y_radius, z_radius, -x_radius)

    path[:, [0,2], :] = np.tile(semi_circle_r[:, np.newaxis, :], (1, 2, 1))
    path[:, 1, :] = np.roll(semi_circle_r, halfsteps, axis=0)
    path[:, 4, :] = semi_circle_l
    path[:, [3,5], :] = np.tile(
        np.roll(semi_circle_l[:, np.newaxis, :], halfsteps, axis=0), (1, 2, 1))

    return path+np.tile(standby_coordinate, (g_steps, 1, 1))


def gen_fastbackward_path(standby_coordinate):
    g_steps = 20
    y_radius = 50
    z_radius = 30
    x_radius = 10

    halfsteps = int(g_steps/2)

    path = np.zeros((g_steps, 6, 3))
    path[:, 0, :] = semicircle2_generator(
        g_steps, y_radius, z_radius, x_radius, reverse=True)
    path[:, 4, :] = semicircle2_generator(
        g_steps, y_radius, z_radius, -x_radius, reverse=True)

    mir_rpath = np.roll(path[:, 0, :], halfsteps, axis=0)
    path[:, 1, :] = mir_rpath
    path[:, 2, :] = path[:, 0, :]

    mir_lpath = np.roll(path[:, 4, :], halfsteps, axis=0)
    path[:, 3, :] = mir_lpath
    path[:, 5, :] = mir_lpath

    return path+np.tile(standby_coordinate, (g_steps, 1, 1))


def gen_leftturn_path(standby_coordinate):
    g_steps = 20
    g_radius = 25
    assert (g_steps % 4) == 0
    halfsteps = int(g_steps/2)

    path = semicircle_generator(g_radius, g_steps)
    mir_path = np.roll(path, halfsteps, axis=0)

    leftturn = np.zeros((g_steps, 6, 3))
    leftturn[:, 0, :] = np.array(path_rotate_z(path, 45))
    leftturn[:, 1, :] = np.array(path_rotate_z(mir_path, 0))
    leftturn[:, 2, :] = np.array(path_rotate_z(path, 315))
    leftturn[:, 3, :] = np.array(path_rotate_z(mir_path, 225))
    leftturn[:, 4, :] = np.array(path_rotate_z(path, 180))
    leftturn[:, 5, :] = np.array(path_rotate_z(mir_path, 135))

    return leftturn+np.tile(standby_coordinate, (g_steps, 1, 1))


def gen_rightturn_path(standby_coordinate):
    g_steps = 20
    g_radius = 25
    assert (g_steps % 4) == 0
    halfsteps = int(g_steps/2)

    path = semicircle_generator(g_radius, g_steps)
    mir_path = np.roll(path, halfsteps, axis=0)

    rightturn = np.zeros((g_steps, 6, 3))
    rightturn[:, 0, :] = np.array(path_rotate_z(path, 45+180))
    rightturn[:, 1, :] = np.array(path_rotate_z(mir_path, 0+180))
    rightturn[:, 2, :] = np.array(path_rotate_z(path, 315+180))
    rightturn[:, 3, :] = np.array(path_rotate_z(mir_path, 225+180))
    rightturn[:, 4, :] = np.array(path_rotate_z(path, 180+180))
    rightturn[:, 5, :] = np.array(path_rotate_z(mir_path, 135+180))

    return rightturn+np.tile(standby_coordinate, (g_steps, 1, 1))


def gen_shiftleft_path(standby_coordinate):
    g_steps = 20
    g_radius = 25
    assert (g_steps % 4) == 0
    halfsteps = int(g_steps/2)

    path = semicircle_generator(g_radius, g_steps)
    # shift 90 degree to make the path "left" shift
    path = path_rotate_z(path, 90)
    mir_path = np.roll(path, halfsteps, axis=0)

    shiftleft = np.zeros((g_steps, 6, 3))
    shiftleft[:, 0, :] = path
    shiftleft[:, 1, :] = mir_path
    shiftleft[:, 2, :] = path
    shiftleft[:, 3, :] = mir_path
    shiftleft[:, 4, :] = path
    shiftleft[:, 5, :] = mir_path

    return shiftleft+np.tile(standby_coordinate, (g_steps, 1, 1))


def gen_shiftright_path(standby_coordinate):
    g_steps = 20
    g_radius = 25
    assert (g_steps % 4) == 0
    halfsteps = int(g_steps/2)

    path = semicircle_generator(g_radius, g_steps)
    # shift 90 degree to make the path "left" shift
    path = path_rotate_z(path, 270)
    mir_path = np.roll(path, halfsteps, axis=0)

    shiftright = np.zeros((g_steps, 6, 3))
    shiftright[:, 0, :] = path
    shiftright[:, 1, :] = mir_path
    shiftright[:, 2, :] = path
    shiftright[:, 3, :] = mir_path
    shiftright[:, 4, :] = path
    shiftright[:, 5, :] = mir_path

    return shiftright+np.tile(standby_coordinate, (g_steps, 1, 1))


def gen_climb_path(standby_coordinate):
    g_steps = 20
    y_radius = 20
    z_radius = 80
    x_radius = 30

    z_shift = -30

    assert (g_steps % 4) == 0
    halfsteps = int(g_steps/2)

    rpath = semicircle2_generator(g_steps, y_radius, z_radius, x_radius)
    rpath[:, 2] = rpath[:, 2]+z_shift
    # rpath = [(x, y, z + z_shift) for x, y,
    #          z in semicircle2_generator(g_steps, y_radius, z_radius, x_radius)]
    lpath = semicircle2_generator(g_steps, y_radius, z_radius, -x_radius)
    lpath[:, 2] = lpath[:, 2]+z_shift
    # lpath = [(x, y, z + z_shift) for x, y,
    #          z in semicircle2_generator(g_steps, y_radius, z_radius, -x_radius)]

    mir_rpath = np.roll(rpath, halfsteps, axis=0)
    mir_lpath = np.roll(lpath, halfsteps, axis=0)

    climbpath = np.zeros((g_steps, 6, 3))
    climbpath[:, 0, :] = rpath
    climbpath[:, 1, :] = mir_rpath
    climbpath[:, 2, :] = rpath
    climbpath[:, 3, :] = mir_lpath
    climbpath[:, 4, :] = lpath
    climbpath[:, 5, :] = mir_lpath

    return climbpath+np.tile(standby_coordinate, (g_steps, 1, 1))


def gen_rotatex_path(standby_coordinate):
    # standby_coordinate = np.ones((6,3))
    g_steps = 20

    swing_angle = 15
    y_radius = 15

    assert (g_steps % 4) == 0
    quarter = int(g_steps/4)

    path = np.zeros((g_steps, 6, 3))

    result = []
    step_angle = swing_angle / quarter
    step_offset = y_radius / quarter

    for i in range(quarter):
        m = get_rotate_x_matrix(swing_angle - i*step_angle)
        m[1, 3] = -i * step_offset
        path[i, 0, 0] = standby_coordinate[0, 0]*m[0, 0]+standby_coordinate[0,
                                                                            1]*m[0, 1]+standby_coordinate[0, 2]*m[0, 2]+m[0, 3]
        path[i, 0, 1] = standby_coordinate[0, 0]*m[1, 0]+standby_coordinate[0,
                                                                            1]*m[1, 1]+standby_coordinate[0, 2]*m[1, 2]+m[1, 3]
        path[i, 0, 2] = standby_coordinate[0, 0]*m[2, 0]+standby_coordinate[0,
                                                                            1]*m[2, 1]+standby_coordinate[0, 2]*m[2, 2]+m[2, 3]

        path[i, 1, 0] = standby_coordinate[1, 0]*m[0, 0]+standby_coordinate[1,
                                                                            1]*m[0, 1]+standby_coordinate[1, 2]*m[0, 2]+m[0, 3]
        path[i, 1, 1] = standby_coordinate[1, 0]*m[1, 0]+standby_coordinate[1,
                                                                            1]*m[1, 1]+standby_coordinate[1, 2]*m[1, 2]+m[1, 3]
        path[i, 1, 2] = standby_coordinate[1, 0]*m[2, 0]+standby_coordinate[1,
                                                                            1]*m[2, 1]+standby_coordinate[1, 2]*m[2, 2]+m[2, 3]

        path[i, 2, 0] = standby_coordinate[2, 0]*m[0, 0]+standby_coordinate[2,
                                                                            1]*m[0, 1]+standby_coordinate[2, 2]*m[0, 2]+m[0, 3]
        path[i, 2, 1] = standby_coordinate[2, 0]*m[1, 0]+standby_coordinate[2,
                                                                            1]*m[1, 1]+standby_coordinate[2, 2]*m[1, 2]+m[1, 3]
        path[i, 2, 2] = standby_coordinate[2, 0]*m[2, 0]+standby_coordinate[2,
                                                                            1]*m[2, 1]+standby_coordinate[2, 2]*m[2, 2]+m[2, 3]

        path[i, 3, 0] = standby_coordinate[3, 0]*m[0, 0]+standby_coordinate[3,
                                                                            1]*m[0, 1]+standby_coordinate[3, 2]*m[0, 2]+m[0, 3]
        path[i, 3, 1] = standby_coordinate[3, 0]*m[1, 0]+standby_coordinate[3,
                                                                            1]*m[1, 1]+standby_coordinate[3, 2]*m[1, 2]+m[1, 3]
        path[i, 3, 2] = standby_coordinate[3, 0]*m[2, 0]+standby_coordinate[3,
                                                                            1]*m[2, 1]+standby_coordinate[3, 2]*m[2, 2]+m[2, 3]

        path[i, 4, 0] = standby_coordinate[4, 0]*m[0, 0]+standby_coordinate[4,
                                                                            1]*m[0, 1]+standby_coordinate[4, 2]*m[0, 2]+m[0, 3]
        path[i, 4, 1] = standby_coordinate[4, 0]*m[1, 0]+standby_coordinate[4,
                                                                            1]*m[1, 1]+standby_coordinate[4, 2]*m[1, 2]+m[1, 3]
        path[i, 4, 2] = standby_coordinate[4, 0]*m[2, 0]+standby_coordinate[4,
                                                                            1]*m[2, 1]+standby_coordinate[4, 2]*m[2, 2]+m[2, 3]

        path[i, 5, 0] = standby_coordinate[5, 0]*m[0, 0]+standby_coordinate[5,
                                                                            1]*m[0, 1]+standby_coordinate[5, 2]*m[0, 2]+m[0, 3]
        path[i, 5, 1] = standby_coordinate[5, 0]*m[1, 0]+standby_coordinate[5,
                                                                            1]*m[1, 1]+standby_coordinate[5, 2]*m[1, 2]+m[1, 3]
        path[i, 5, 2] = standby_coordinate[5, 0]*m[2, 0]+standby_coordinate[5,
                                                                            1]*m[2, 1]+standby_coordinate[5, 2]*m[2, 2]+m[2, 3]

        result.append(m)

    for i in range(quarter):
        m = get_rotate_x_matrix(-i*step_angle)
        m[1, 3] = -y_radius + i * step_offset

        idx = i+quarter

        path[idx, 0, 0] = standby_coordinate[0, 0]*m[0, 0]+standby_coordinate[0,
                                                                              1]*m[0, 1]+standby_coordinate[0, 2]*m[0, 2]+m[0, 3]
        path[idx, 0, 1] = standby_coordinate[0, 0]*m[1, 0]+standby_coordinate[0,
                                                                              1]*m[1, 1]+standby_coordinate[0, 2]*m[1, 2]+m[1, 3]
        path[idx, 0, 2] = standby_coordinate[0, 0]*m[2, 0]+standby_coordinate[0,
                                                                              1]*m[2, 1]+standby_coordinate[0, 2]*m[2, 2]+m[2, 3]

        path[idx, 1, 0] = standby_coordinate[1, 0]*m[0, 0]+standby_coordinate[1,
                                                                              1]*m[0, 1]+standby_coordinate[1, 2]*m[0, 2]+m[0, 3]
        path[idx, 1, 1] = standby_coordinate[1, 0]*m[1, 0]+standby_coordinate[1,
                                                                              1]*m[1, 1]+standby_coordinate[1, 2]*m[1, 2]+m[1, 3]
        path[idx, 1, 2] = standby_coordinate[1, 0]*m[2, 0]+standby_coordinate[1,
                                                                              1]*m[2, 1]+standby_coordinate[1, 2]*m[2, 2]+m[2, 3]

        path[idx, 2, 0] = standby_coordinate[2, 0]*m[0, 0]+standby_coordinate[2,
                                                                              1]*m[0, 1]+standby_coordinate[2, 2]*m[0, 2]+m[0, 3]
        path[idx, 2, 1] = standby_coordinate[2, 0]*m[1, 0]+standby_coordinate[2,
                                                                              1]*m[1, 1]+standby_coordinate[2, 2]*m[1, 2]+m[1, 3]
        path[idx, 2, 2] = standby_coordinate[2, 0]*m[2, 0]+standby_coordinate[2,
                                                                              1]*m[2, 1]+standby_coordinate[2, 2]*m[2, 2]+m[2, 3]

        path[idx, 3, 0] = standby_coordinate[3, 0]*m[0, 0]+standby_coordinate[3,
                                                                              1]*m[0, 1]+standby_coordinate[3, 2]*m[0, 2]+m[0, 3]
        path[idx, 3, 1] = standby_coordinate[3, 0]*m[1, 0]+standby_coordinate[3,
                                                                              1]*m[1, 1]+standby_coordinate[3, 2]*m[1, 2]+m[1, 3]
        path[idx, 3, 2] = standby_coordinate[3, 0]*m[2, 0]+standby_coordinate[3,
                                                                              1]*m[2, 1]+standby_coordinate[3, 2]*m[2, 2]+m[2, 3]

        path[idx, 4, 0] = standby_coordinate[4, 0]*m[0, 0]+standby_coordinate[4,
                                                                              1]*m[0, 1]+standby_coordinate[4, 2]*m[0, 2]+m[0, 3]
        path[idx, 4, 1] = standby_coordinate[4, 0]*m[1, 0]+standby_coordinate[4,
                                                                              1]*m[1, 1]+standby_coordinate[4, 2]*m[1, 2]+m[1, 3]
        path[idx, 4, 2] = standby_coordinate[4, 0]*m[2, 0]+standby_coordinate[4,
                                                                              1]*m[2, 1]+standby_coordinate[4, 2]*m[2, 2]+m[2, 3]

        path[idx, 5, 0] = standby_coordinate[5, 0]*m[0, 0]+standby_coordinate[5,
                                                                              1]*m[0, 1]+standby_coordinate[5, 2]*m[0, 2]+m[0, 3]
        path[idx, 5, 1] = standby_coordinate[5, 0]*m[1, 0]+standby_coordinate[5,
                                                                              1]*m[1, 1]+standby_coordinate[5, 2]*m[1, 2]+m[1, 3]
        path[idx, 5, 2] = standby_coordinate[5, 0]*m[2, 0]+standby_coordinate[5,
                                                                              1]*m[2, 1]+standby_coordinate[5, 2]*m[2, 2]+m[2, 3]
        result.append(m)

    for i in range(quarter):
        m = get_rotate_x_matrix(i*step_angle-swing_angle)
        m[1, 3] = i * step_offset
        idx = i+quarter*2

        path[idx, 0, 0] = standby_coordinate[0, 0]*m[0, 0]+standby_coordinate[0,
                                                                              1]*m[0, 1]+standby_coordinate[0, 2]*m[0, 2]+m[0, 3]
        path[idx, 0, 1] = standby_coordinate[0, 0]*m[1, 0]+standby_coordinate[0,
                                                                              1]*m[1, 1]+standby_coordinate[0, 2]*m[1, 2]+m[1, 3]
        path[idx, 0, 2] = standby_coordinate[0, 0]*m[2, 0]+standby_coordinate[0,
                                                                              1]*m[2, 1]+standby_coordinate[0, 2]*m[2, 2]+m[2, 3]

        path[idx, 1, 0] = standby_coordinate[1, 0]*m[0, 0]+standby_coordinate[1,
                                                                              1]*m[0, 1]+standby_coordinate[1, 2]*m[0, 2]+m[0, 3]
        path[idx, 1, 1] = standby_coordinate[1, 0]*m[1, 0]+standby_coordinate[1,
                                                                              1]*m[1, 1]+standby_coordinate[1, 2]*m[1, 2]+m[1, 3]
        path[idx, 1, 2] = standby_coordinate[1, 0]*m[2, 0]+standby_coordinate[1,
                                                                              1]*m[2, 1]+standby_coordinate[1, 2]*m[2, 2]+m[2, 3]

        path[idx, 2, 0] = standby_coordinate[2, 0]*m[0, 0]+standby_coordinate[2,
                                                                              1]*m[0, 1]+standby_coordinate[2, 2]*m[0, 2]+m[0, 3]
        path[idx, 2, 1] = standby_coordinate[2, 0]*m[1, 0]+standby_coordinate[2,
                                                                              1]*m[1, 1]+standby_coordinate[2, 2]*m[1, 2]+m[1, 3]
        path[idx, 2, 2] = standby_coordinate[2, 0]*m[2, 0]+standby_coordinate[2,
                                                                              1]*m[2, 1]+standby_coordinate[2, 2]*m[2, 2]+m[2, 3]

        path[idx, 3, 0] = standby_coordinate[3, 0]*m[0, 0]+standby_coordinate[3,
                                                                              1]*m[0, 1]+standby_coordinate[3, 2]*m[0, 2]+m[0, 3]
        path[idx, 3, 1] = standby_coordinate[3, 0]*m[1, 0]+standby_coordinate[3,
                                                                              1]*m[1, 1]+standby_coordinate[3, 2]*m[1, 2]+m[1, 3]
        path[idx, 3, 2] = standby_coordinate[3, 0]*m[2, 0]+standby_coordinate[3,
                                                                              1]*m[2, 1]+standby_coordinate[3, 2]*m[2, 2]+m[2, 3]

        path[idx, 4, 0] = standby_coordinate[4, 0]*m[0, 0]+standby_coordinate[4,
                                                                              1]*m[0, 1]+standby_coordinate[4, 2]*m[0, 2]+m[0, 3]
        path[idx, 4, 1] = standby_coordinate[4, 0]*m[1, 0]+standby_coordinate[4,
                                                                              1]*m[1, 1]+standby_coordinate[4, 2]*m[1, 2]+m[1, 3]
        path[idx, 4, 2] = standby_coordinate[4, 0]*m[2, 0]+standby_coordinate[4,
                                                                              1]*m[2, 1]+standby_coordinate[4, 2]*m[2, 2]+m[2, 3]

        path[idx, 5, 0] = standby_coordinate[5, 0]*m[0, 0]+standby_coordinate[5,
                                                                              1]*m[0, 1]+standby_coordinate[5, 2]*m[0, 2]+m[0, 3]
        path[idx, 5, 1] = standby_coordinate[5, 0]*m[1, 0]+standby_coordinate[5,
                                                                              1]*m[1, 1]+standby_coordinate[5, 2]*m[1, 2]+m[1, 3]
        path[idx, 5, 2] = standby_coordinate[5, 0]*m[2, 0]+standby_coordinate[5,
                                                                              1]*m[2, 1]+standby_coordinate[5, 2]*m[2, 2]+m[2, 3]
        result.append(m)

    for i in range(quarter):
        m = get_rotate_x_matrix(i*step_angle)
        m[1, 3] = y_radius-i * step_offset
        idx = i+quarter*3

        path[idx, 0, 0] = standby_coordinate[0, 0]*m[0, 0]+standby_coordinate[0,
                                                                              1]*m[0, 1]+standby_coordinate[0, 2]*m[0, 2]+m[0, 3]
        path[idx, 0, 1] = standby_coordinate[0, 0]*m[1, 0]+standby_coordinate[0,
                                                                              1]*m[1, 1]+standby_coordinate[0, 2]*m[1, 2]+m[1, 3]
        path[idx, 0, 2] = standby_coordinate[0, 0]*m[2, 0]+standby_coordinate[0,
                                                                              1]*m[2, 1]+standby_coordinate[0, 2]*m[2, 2]+m[2, 3]

        path[idx, 1, 0] = standby_coordinate[1, 0]*m[0, 0]+standby_coordinate[1,
                                                                              1]*m[0, 1]+standby_coordinate[1, 2]*m[0, 2]+m[0, 3]
        path[idx, 1, 1] = standby_coordinate[1, 0]*m[1, 0]+standby_coordinate[1,
                                                                              1]*m[1, 1]+standby_coordinate[1, 2]*m[1, 2]+m[1, 3]
        path[idx, 1, 2] = standby_coordinate[1, 0]*m[2, 0]+standby_coordinate[1,
                                                                              1]*m[2, 1]+standby_coordinate[1, 2]*m[2, 2]+m[2, 3]

        path[idx, 2, 0] = standby_coordinate[2, 0]*m[0, 0]+standby_coordinate[2,
                                                                              1]*m[0, 1]+standby_coordinate[2, 2]*m[0, 2]+m[0, 3]
        path[idx, 2, 1] = standby_coordinate[2, 0]*m[1, 0]+standby_coordinate[2,
                                                                              1]*m[1, 1]+standby_coordinate[2, 2]*m[1, 2]+m[1, 3]
        path[idx, 2, 2] = standby_coordinate[2, 0]*m[2, 0]+standby_coordinate[2,
                                                                              1]*m[2, 1]+standby_coordinate[2, 2]*m[2, 2]+m[2, 3]

        path[idx, 3, 0] = standby_coordinate[3, 0]*m[0, 0]+standby_coordinate[3,
                                                                              1]*m[0, 1]+standby_coordinate[3, 2]*m[0, 2]+m[0, 3]
        path[idx, 3, 1] = standby_coordinate[3, 0]*m[1, 0]+standby_coordinate[3,
                                                                              1]*m[1, 1]+standby_coordinate[3, 2]*m[1, 2]+m[1, 3]
        path[idx, 3, 2] = standby_coordinate[3, 0]*m[2, 0]+standby_coordinate[3,
                                                                              1]*m[2, 1]+standby_coordinate[3, 2]*m[2, 2]+m[2, 3]

        path[idx, 4, 0] = standby_coordinate[4, 0]*m[0, 0]+standby_coordinate[4,
                                                                              1]*m[0, 1]+standby_coordinate[4, 2]*m[0, 2]+m[0, 3]
        path[idx, 4, 1] = standby_coordinate[4, 0]*m[1, 0]+standby_coordinate[4,
                                                                              1]*m[1, 1]+standby_coordinate[4, 2]*m[1, 2]+m[1, 3]
        path[idx, 4, 2] = standby_coordinate[4, 0]*m[2, 0]+standby_coordinate[4,
                                                                              1]*m[2, 1]+standby_coordinate[4, 2]*m[2, 2]+m[2, 3]

        path[idx, 5, 0] = standby_coordinate[5, 0]*m[0, 0]+standby_coordinate[5,
                                                                              1]*m[0, 1]+standby_coordinate[5, 2]*m[0, 2]+m[0, 3]
        path[idx, 5, 1] = standby_coordinate[5, 0]*m[1, 0]+standby_coordinate[5,
                                                                              1]*m[1, 1]+standby_coordinate[5, 2]*m[1, 2]+m[1, 3]
        path[idx, 5, 2] = standby_coordinate[5, 0]*m[2, 0]+standby_coordinate[5,
                                                                              1]*m[2, 1]+standby_coordinate[5, 2]*m[2, 2]+m[2, 3]
        result.append(m)

    return path
    # return result, "matrix", 50, (0, quarter*2)


def gen_rotatey_path(standby_coordinate):
    # standby_coordinate = np.ones((6,3))
    g_steps = 20

    swing_angle = 15
    x_radius = 15

    assert (g_steps % 4) == 0
    quarter = int(g_steps/4)

    path = np.zeros((g_steps, 6, 3))

    result = []
    step_angle = swing_angle / quarter
    step_offset = x_radius / quarter

    for i in range(quarter):
        m = get_rotate_y_matrix(swing_angle - i*step_angle)
        m[1, 3] = -i * step_offset
        path[i, 0, 0] = standby_coordinate[0, 0]*m[0, 0]+standby_coordinate[0,
                                                                            1]*m[0, 1]+standby_coordinate[0, 2]*m[0, 2]+m[0, 3]
        path[i, 0, 1] = standby_coordinate[0, 0]*m[1, 0]+standby_coordinate[0,
                                                                            1]*m[1, 1]+standby_coordinate[0, 2]*m[1, 2]+m[1, 3]
        path[i, 0, 2] = standby_coordinate[0, 0]*m[2, 0]+standby_coordinate[0,
                                                                            1]*m[2, 1]+standby_coordinate[0, 2]*m[2, 2]+m[2, 3]

        path[i, 1, 0] = standby_coordinate[1, 0]*m[0, 0]+standby_coordinate[1,
                                                                            1]*m[0, 1]+standby_coordinate[1, 2]*m[0, 2]+m[0, 3]
        path[i, 1, 1] = standby_coordinate[1, 0]*m[1, 0]+standby_coordinate[1,
                                                                            1]*m[1, 1]+standby_coordinate[1, 2]*m[1, 2]+m[1, 3]
        path[i, 1, 2] = standby_coordinate[1, 0]*m[2, 0]+standby_coordinate[1,
                                                                            1]*m[2, 1]+standby_coordinate[1, 2]*m[2, 2]+m[2, 3]

        path[i, 2, 0] = standby_coordinate[2, 0]*m[0, 0]+standby_coordinate[2,
                                                                            1]*m[0, 1]+standby_coordinate[2, 2]*m[0, 2]+m[0, 3]
        path[i, 2, 1] = standby_coordinate[2, 0]*m[1, 0]+standby_coordinate[2,
                                                                            1]*m[1, 1]+standby_coordinate[2, 2]*m[1, 2]+m[1, 3]
        path[i, 2, 2] = standby_coordinate[2, 0]*m[2, 0]+standby_coordinate[2,
                                                                            1]*m[2, 1]+standby_coordinate[2, 2]*m[2, 2]+m[2, 3]

        path[i, 3, 0] = standby_coordinate[3, 0]*m[0, 0]+standby_coordinate[3,
                                                                            1]*m[0, 1]+standby_coordinate[3, 2]*m[0, 2]+m[0, 3]
        path[i, 3, 1] = standby_coordinate[3, 0]*m[1, 0]+standby_coordinate[3,
                                                                            1]*m[1, 1]+standby_coordinate[3, 2]*m[1, 2]+m[1, 3]
        path[i, 3, 2] = standby_coordinate[3, 0]*m[2, 0]+standby_coordinate[3,
                                                                            1]*m[2, 1]+standby_coordinate[3, 2]*m[2, 2]+m[2, 3]

        path[i, 4, 0] = standby_coordinate[4, 0]*m[0, 0]+standby_coordinate[4,
                                                                            1]*m[0, 1]+standby_coordinate[4, 2]*m[0, 2]+m[0, 3]
        path[i, 4, 1] = standby_coordinate[4, 0]*m[1, 0]+standby_coordinate[4,
                                                                            1]*m[1, 1]+standby_coordinate[4, 2]*m[1, 2]+m[1, 3]
        path[i, 4, 2] = standby_coordinate[4, 0]*m[2, 0]+standby_coordinate[4,
                                                                            1]*m[2, 1]+standby_coordinate[4, 2]*m[2, 2]+m[2, 3]

        path[i, 5, 0] = standby_coordinate[5, 0]*m[0, 0]+standby_coordinate[5,
                                                                            1]*m[0, 1]+standby_coordinate[5, 2]*m[0, 2]+m[0, 3]
        path[i, 5, 1] = standby_coordinate[5, 0]*m[1, 0]+standby_coordinate[5,
                                                                            1]*m[1, 1]+standby_coordinate[5, 2]*m[1, 2]+m[1, 3]
        path[i, 5, 2] = standby_coordinate[5, 0]*m[2, 0]+standby_coordinate[5,
                                                                            1]*m[2, 1]+standby_coordinate[5, 2]*m[2, 2]+m[2, 3]

        # result.append(m)

    for i in range(quarter):
        m = get_rotate_y_matrix(-i*step_angle)
        m[1, 3] = -x_radius + i * step_offset

        idx = i+quarter

        path[idx, 0, 0] = standby_coordinate[0, 0]*m[0, 0]+standby_coordinate[0,
                                                                              1]*m[0, 1]+standby_coordinate[0, 2]*m[0, 2]+m[0, 3]
        path[idx, 0, 1] = standby_coordinate[0, 0]*m[1, 0]+standby_coordinate[0,
                                                                              1]*m[1, 1]+standby_coordinate[0, 2]*m[1, 2]+m[1, 3]
        path[idx, 0, 2] = standby_coordinate[0, 0]*m[2, 0]+standby_coordinate[0,
                                                                              1]*m[2, 1]+standby_coordinate[0, 2]*m[2, 2]+m[2, 3]

        path[idx, 1, 0] = standby_coordinate[1, 0]*m[0, 0]+standby_coordinate[1,
                                                                              1]*m[0, 1]+standby_coordinate[1, 2]*m[0, 2]+m[0, 3]
        path[idx, 1, 1] = standby_coordinate[1, 0]*m[1, 0]+standby_coordinate[1,
                                                                              1]*m[1, 1]+standby_coordinate[1, 2]*m[1, 2]+m[1, 3]
        path[idx, 1, 2] = standby_coordinate[1, 0]*m[2, 0]+standby_coordinate[1,
                                                                              1]*m[2, 1]+standby_coordinate[1, 2]*m[2, 2]+m[2, 3]

        path[idx, 2, 0] = standby_coordinate[2, 0]*m[0, 0]+standby_coordinate[2,
                                                                              1]*m[0, 1]+standby_coordinate[2, 2]*m[0, 2]+m[0, 3]
        path[idx, 2, 1] = standby_coordinate[2, 0]*m[1, 0]+standby_coordinate[2,
                                                                              1]*m[1, 1]+standby_coordinate[2, 2]*m[1, 2]+m[1, 3]
        path[idx, 2, 2] = standby_coordinate[2, 0]*m[2, 0]+standby_coordinate[2,
                                                                              1]*m[2, 1]+standby_coordinate[2, 2]*m[2, 2]+m[2, 3]

        path[idx, 3, 0] = standby_coordinate[3, 0]*m[0, 0]+standby_coordinate[3,
                                                                              1]*m[0, 1]+standby_coordinate[3, 2]*m[0, 2]+m[0, 3]
        path[idx, 3, 1] = standby_coordinate[3, 0]*m[1, 0]+standby_coordinate[3,
                                                                              1]*m[1, 1]+standby_coordinate[3, 2]*m[1, 2]+m[1, 3]
        path[idx, 3, 2] = standby_coordinate[3, 0]*m[2, 0]+standby_coordinate[3,
                                                                              1]*m[2, 1]+standby_coordinate[3, 2]*m[2, 2]+m[2, 3]

        path[idx, 4, 0] = standby_coordinate[4, 0]*m[0, 0]+standby_coordinate[4,
                                                                              1]*m[0, 1]+standby_coordinate[4, 2]*m[0, 2]+m[0, 3]
        path[idx, 4, 1] = standby_coordinate[4, 0]*m[1, 0]+standby_coordinate[4,
                                                                              1]*m[1, 1]+standby_coordinate[4, 2]*m[1, 2]+m[1, 3]
        path[idx, 4, 2] = standby_coordinate[4, 0]*m[2, 0]+standby_coordinate[4,
                                                                              1]*m[2, 1]+standby_coordinate[4, 2]*m[2, 2]+m[2, 3]

        path[idx, 5, 0] = standby_coordinate[5, 0]*m[0, 0]+standby_coordinate[5,
                                                                              1]*m[0, 1]+standby_coordinate[5, 2]*m[0, 2]+m[0, 3]
        path[idx, 5, 1] = standby_coordinate[5, 0]*m[1, 0]+standby_coordinate[5,
                                                                              1]*m[1, 1]+standby_coordinate[5, 2]*m[1, 2]+m[1, 3]
        path[idx, 5, 2] = standby_coordinate[5, 0]*m[2, 0]+standby_coordinate[5,
                                                                              1]*m[2, 1]+standby_coordinate[5, 2]*m[2, 2]+m[2, 3]
        # result.append(m)

    for i in range(quarter):
        m = get_rotate_y_matrix(i*step_angle-swing_angle)
        m[1, 3] = i * step_offset
        idx = i+quarter*2

        path[idx, 0, 0] = standby_coordinate[0, 0]*m[0, 0]+standby_coordinate[0,
                                                                              1]*m[0, 1]+standby_coordinate[0, 2]*m[0, 2]+m[0, 3]
        path[idx, 0, 1] = standby_coordinate[0, 0]*m[1, 0]+standby_coordinate[0,
                                                                              1]*m[1, 1]+standby_coordinate[0, 2]*m[1, 2]+m[1, 3]
        path[idx, 0, 2] = standby_coordinate[0, 0]*m[2, 0]+standby_coordinate[0,
                                                                              1]*m[2, 1]+standby_coordinate[0, 2]*m[2, 2]+m[2, 3]

        path[idx, 1, 0] = standby_coordinate[1, 0]*m[0, 0]+standby_coordinate[1,
                                                                              1]*m[0, 1]+standby_coordinate[1, 2]*m[0, 2]+m[0, 3]
        path[idx, 1, 1] = standby_coordinate[1, 0]*m[1, 0]+standby_coordinate[1,
                                                                              1]*m[1, 1]+standby_coordinate[1, 2]*m[1, 2]+m[1, 3]
        path[idx, 1, 2] = standby_coordinate[1, 0]*m[2, 0]+standby_coordinate[1,
                                                                              1]*m[2, 1]+standby_coordinate[1, 2]*m[2, 2]+m[2, 3]

        path[idx, 2, 0] = standby_coordinate[2, 0]*m[0, 0]+standby_coordinate[2,
                                                                              1]*m[0, 1]+standby_coordinate[2, 2]*m[0, 2]+m[0, 3]
        path[idx, 2, 1] = standby_coordinate[2, 0]*m[1, 0]+standby_coordinate[2,
                                                                              1]*m[1, 1]+standby_coordinate[2, 2]*m[1, 2]+m[1, 3]
        path[idx, 2, 2] = standby_coordinate[2, 0]*m[2, 0]+standby_coordinate[2,
                                                                              1]*m[2, 1]+standby_coordinate[2, 2]*m[2, 2]+m[2, 3]

        path[idx, 3, 0] = standby_coordinate[3, 0]*m[0, 0]+standby_coordinate[3,
                                                                              1]*m[0, 1]+standby_coordinate[3, 2]*m[0, 2]+m[0, 3]
        path[idx, 3, 1] = standby_coordinate[3, 0]*m[1, 0]+standby_coordinate[3,
                                                                              1]*m[1, 1]+standby_coordinate[3, 2]*m[1, 2]+m[1, 3]
        path[idx, 3, 2] = standby_coordinate[3, 0]*m[2, 0]+standby_coordinate[3,
                                                                              1]*m[2, 1]+standby_coordinate[3, 2]*m[2, 2]+m[2, 3]

        path[idx, 4, 0] = standby_coordinate[4, 0]*m[0, 0]+standby_coordinate[4,
                                                                              1]*m[0, 1]+standby_coordinate[4, 2]*m[0, 2]+m[0, 3]
        path[idx, 4, 1] = standby_coordinate[4, 0]*m[1, 0]+standby_coordinate[4,
                                                                              1]*m[1, 1]+standby_coordinate[4, 2]*m[1, 2]+m[1, 3]
        path[idx, 4, 2] = standby_coordinate[4, 0]*m[2, 0]+standby_coordinate[4,
                                                                              1]*m[2, 1]+standby_coordinate[4, 2]*m[2, 2]+m[2, 3]

        path[idx, 5, 0] = standby_coordinate[5, 0]*m[0, 0]+standby_coordinate[5,
                                                                              1]*m[0, 1]+standby_coordinate[5, 2]*m[0, 2]+m[0, 3]
        path[idx, 5, 1] = standby_coordinate[5, 0]*m[1, 0]+standby_coordinate[5,
                                                                              1]*m[1, 1]+standby_coordinate[5, 2]*m[1, 2]+m[1, 3]
        path[idx, 5, 2] = standby_coordinate[5, 0]*m[2, 0]+standby_coordinate[5,
                                                                              1]*m[2, 1]+standby_coordinate[5, 2]*m[2, 2]+m[2, 3]
        # result.append(m)

    for i in range(quarter):
        m = get_rotate_y_matrix(i*step_angle)
        m[1, 3] = x_radius-i * step_offset
        idx = i+quarter*3

        path[idx, 0, 0] = standby_coordinate[0, 0]*m[0, 0]+standby_coordinate[0,
                                                                              1]*m[0, 1]+standby_coordinate[0, 2]*m[0, 2]+m[0, 3]
        path[idx, 0, 1] = standby_coordinate[0, 0]*m[1, 0]+standby_coordinate[0,
                                                                              1]*m[1, 1]+standby_coordinate[0, 2]*m[1, 2]+m[1, 3]
        path[idx, 0, 2] = standby_coordinate[0, 0]*m[2, 0]+standby_coordinate[0,
                                                                              1]*m[2, 1]+standby_coordinate[0, 2]*m[2, 2]+m[2, 3]

        path[idx, 1, 0] = standby_coordinate[1, 0]*m[0, 0]+standby_coordinate[1,
                                                                              1]*m[0, 1]+standby_coordinate[1, 2]*m[0, 2]+m[0, 3]
        path[idx, 1, 1] = standby_coordinate[1, 0]*m[1, 0]+standby_coordinate[1,
                                                                              1]*m[1, 1]+standby_coordinate[1, 2]*m[1, 2]+m[1, 3]
        path[idx, 1, 2] = standby_coordinate[1, 0]*m[2, 0]+standby_coordinate[1,
                                                                              1]*m[2, 1]+standby_coordinate[1, 2]*m[2, 2]+m[2, 3]

        path[idx, 2, 0] = standby_coordinate[2, 0]*m[0, 0]+standby_coordinate[2,
                                                                              1]*m[0, 1]+standby_coordinate[2, 2]*m[0, 2]+m[0, 3]
        path[idx, 2, 1] = standby_coordinate[2, 0]*m[1, 0]+standby_coordinate[2,
                                                                              1]*m[1, 1]+standby_coordinate[2, 2]*m[1, 2]+m[1, 3]
        path[idx, 2, 2] = standby_coordinate[2, 0]*m[2, 0]+standby_coordinate[2,
                                                                              1]*m[2, 1]+standby_coordinate[2, 2]*m[2, 2]+m[2, 3]

        path[idx, 3, 0] = standby_coordinate[3, 0]*m[0, 0]+standby_coordinate[3,
                                                                              1]*m[0, 1]+standby_coordinate[3, 2]*m[0, 2]+m[0, 3]
        path[idx, 3, 1] = standby_coordinate[3, 0]*m[1, 0]+standby_coordinate[3,
                                                                              1]*m[1, 1]+standby_coordinate[3, 2]*m[1, 2]+m[1, 3]
        path[idx, 3, 2] = standby_coordinate[3, 0]*m[2, 0]+standby_coordinate[3,
                                                                              1]*m[2, 1]+standby_coordinate[3, 2]*m[2, 2]+m[2, 3]

        path[idx, 4, 0] = standby_coordinate[4, 0]*m[0, 0]+standby_coordinate[4,
                                                                              1]*m[0, 1]+standby_coordinate[4, 2]*m[0, 2]+m[0, 3]
        path[idx, 4, 1] = standby_coordinate[4, 0]*m[1, 0]+standby_coordinate[4,
                                                                              1]*m[1, 1]+standby_coordinate[4, 2]*m[1, 2]+m[1, 3]
        path[idx, 4, 2] = standby_coordinate[4, 0]*m[2, 0]+standby_coordinate[4,
                                                                              1]*m[2, 1]+standby_coordinate[4, 2]*m[2, 2]+m[2, 3]

        path[idx, 5, 0] = standby_coordinate[5, 0]*m[0, 0]+standby_coordinate[5,
                                                                              1]*m[0, 1]+standby_coordinate[5, 2]*m[0, 2]+m[0, 3]
        path[idx, 5, 1] = standby_coordinate[5, 0]*m[1, 0]+standby_coordinate[5,
                                                                              1]*m[1, 1]+standby_coordinate[5, 2]*m[1, 2]+m[1, 3]
        path[idx, 5, 2] = standby_coordinate[5, 0]*m[2, 0]+standby_coordinate[5,
                                                                              1]*m[2, 1]+standby_coordinate[5, 2]*m[2, 2]+m[2, 3]
        # result.append(m)

    return path


def gen_rotatez_path(standby_coordinate):
    # standby_coordinate = np.ones((6,3))
    g_steps = 20

    z_lift = 4.5
    xy_radius = 1

    assert (g_steps % 4) == 0

    path = np.zeros((g_steps, 6, 3))

    step_angle = 2*np.pi / g_steps

    for i in range(g_steps):
        x = xy_radius * np.cos(i*step_angle)
        y = xy_radius * np.sin(i*step_angle)

        m = get_rotate_y_matrix(np.arctan2(
            x, z_lift)*180/np.pi) * get_rotate_x_matrix(np.arctan2(y, z_lift)*180/np.pi)
        path[i, 0, 0] = standby_coordinate[0, 0]*m[0, 0]+standby_coordinate[0,
                                                                            1]*m[0, 1]+standby_coordinate[0, 2]*m[0, 2]+m[0, 3]
        path[i, 0, 1] = standby_coordinate[0, 0]*m[1, 0]+standby_coordinate[0,
                                                                            1]*m[1, 1]+standby_coordinate[0, 2]*m[1, 2]+m[1, 3]
        path[i, 0, 2] = standby_coordinate[0, 0]*m[2, 0]+standby_coordinate[0,
                                                                            1]*m[2, 1]+standby_coordinate[0, 2]*m[2, 2]+m[2, 3]

        path[i, 1, 0] = standby_coordinate[1, 0]*m[0, 0]+standby_coordinate[1,
                                                                            1]*m[0, 1]+standby_coordinate[1, 2]*m[0, 2]+m[0, 3]
        path[i, 1, 1] = standby_coordinate[1, 0]*m[1, 0]+standby_coordinate[1,
                                                                            1]*m[1, 1]+standby_coordinate[1, 2]*m[1, 2]+m[1, 3]
        path[i, 1, 2] = standby_coordinate[1, 0]*m[2, 0]+standby_coordinate[1,
                                                                            1]*m[2, 1]+standby_coordinate[1, 2]*m[2, 2]+m[2, 3]

        path[i, 2, 0] = standby_coordinate[2, 0]*m[0, 0]+standby_coordinate[2,
                                                                            1]*m[0, 1]+standby_coordinate[2, 2]*m[0, 2]+m[0, 3]
        path[i, 2, 1] = standby_coordinate[2, 0]*m[1, 0]+standby_coordinate[2,
                                                                            1]*m[1, 1]+standby_coordinate[2, 2]*m[1, 2]+m[1, 3]
        path[i, 2, 2] = standby_coordinate[2, 0]*m[2, 0]+standby_coordinate[2,
                                                                            1]*m[2, 1]+standby_coordinate[2, 2]*m[2, 2]+m[2, 3]

        path[i, 3, 0] = standby_coordinate[3, 0]*m[0, 0]+standby_coordinate[3,
                                                                            1]*m[0, 1]+standby_coordinate[3, 2]*m[0, 2]+m[0, 3]
        path[i, 3, 1] = standby_coordinate[3, 0]*m[1, 0]+standby_coordinate[3,
                                                                            1]*m[1, 1]+standby_coordinate[3, 2]*m[1, 2]+m[1, 3]
        path[i, 3, 2] = standby_coordinate[3, 0]*m[2, 0]+standby_coordinate[3,
                                                                            1]*m[2, 1]+standby_coordinate[3, 2]*m[2, 2]+m[2, 3]

        path[i, 4, 0] = standby_coordinate[4, 0]*m[0, 0]+standby_coordinate[4,
                                                                            1]*m[0, 1]+standby_coordinate[4, 2]*m[0, 2]+m[0, 3]
        path[i, 4, 1] = standby_coordinate[4, 0]*m[1, 0]+standby_coordinate[4,
                                                                            1]*m[1, 1]+standby_coordinate[4, 2]*m[1, 2]+m[1, 3]
        path[i, 4, 2] = standby_coordinate[4, 0]*m[2, 0]+standby_coordinate[4,
                                                                            1]*m[2, 1]+standby_coordinate[4, 2]*m[2, 2]+m[2, 3]

        path[i, 5, 0] = standby_coordinate[5, 0]*m[0, 0]+standby_coordinate[5,
                                                                            1]*m[0, 1]+standby_coordinate[5, 2]*m[0, 2]+m[0, 3]
        path[i, 5, 1] = standby_coordinate[5, 0]*m[1, 0]+standby_coordinate[5,
                                                                            1]*m[1, 1]+standby_coordinate[5, 2]*m[1, 2]+m[1, 3]
        path[i, 5, 2] = standby_coordinate[5, 0]*m[2, 0]+standby_coordinate[5,
                                                                            1]*m[2, 1]+standby_coordinate[5, 2]*m[2, 2]+m[2, 3]

    return path


def gen_twist_path(standby_coordinate):
    g_steps = 20
    raise_angle = 3
    twist_x_angle = 20
    twise_y_angle = 12
    assert (g_steps % 4) == 0

    quarter = int(g_steps / 4)
    step_x_angle = twist_x_angle / quarter
    step_y_angle = twise_y_angle / quarter

    m = get_rotate_x_matrix(raise_angle)

    path = np.zeros((g_steps, 6, 3))

    for i in range(quarter):
        temp = m * get_rotate_z_matrix(i*step_x_angle) * \
            get_rotate_x_matrix(i*step_y_angle)

        idx = i+quarter*0

        path[idx, 0, 0] = standby_coordinate[0, 0]*temp[0, 0]+standby_coordinate[0,
                                                                                 1]*temp[0, 1]+standby_coordinate[0, 2]*temp[0, 2]+temp[0, 3]
        path[idx, 0, 1] = standby_coordinate[0, 0]*temp[1, 0]+standby_coordinate[0,
                                                                                 1]*temp[1, 1]+standby_coordinate[0, 2]*temp[1, 2]+temp[1, 3]
        path[idx, 0, 2] = standby_coordinate[0, 0]*temp[2, 0]+standby_coordinate[0,
                                                                                 1]*temp[2, 1]+standby_coordinate[0, 2]*temp[2, 2]+temp[2, 3]

        path[idx, 1, 0] = standby_coordinate[1, 0]*temp[0, 0]+standby_coordinate[1,
                                                                                 1]*temp[0, 1]+standby_coordinate[1, 2]*temp[0, 2]+temp[0, 3]
        path[idx, 1, 1] = standby_coordinate[1, 0]*temp[1, 0]+standby_coordinate[1,
                                                                                 1]*temp[1, 1]+standby_coordinate[1, 2]*temp[1, 2]+temp[1, 3]
        path[idx, 1, 2] = standby_coordinate[1, 0]*temp[2, 0]+standby_coordinate[1,
                                                                                 1]*temp[2, 1]+standby_coordinate[1, 2]*temp[2, 2]+temp[2, 3]

        path[idx, 2, 0] = standby_coordinate[2, 0]*temp[0, 0]+standby_coordinate[2,
                                                                                 1]*temp[0, 1]+standby_coordinate[2, 2]*temp[0, 2]+temp[0, 3]
        path[idx, 2, 1] = standby_coordinate[2, 0]*temp[1, 0]+standby_coordinate[2,
                                                                                 1]*temp[1, 1]+standby_coordinate[2, 2]*temp[1, 2]+temp[1, 3]
        path[idx, 2, 2] = standby_coordinate[2, 0]*temp[2, 0]+standby_coordinate[2,
                                                                                 1]*temp[2, 1]+standby_coordinate[2, 2]*temp[2, 2]+temp[2, 3]

        path[idx, 3, 0] = standby_coordinate[3, 0]*temp[0, 0]+standby_coordinate[3,
                                                                                 1]*temp[0, 1]+standby_coordinate[3, 2]*temp[0, 2]+temp[0, 3]
        path[idx, 3, 1] = standby_coordinate[3, 0]*temp[1, 0]+standby_coordinate[3,
                                                                                 1]*temp[1, 1]+standby_coordinate[3, 2]*temp[1, 2]+temp[1, 3]
        path[idx, 3, 2] = standby_coordinate[3, 0]*temp[2, 0]+standby_coordinate[3,
                                                                                 1]*temp[2, 1]+standby_coordinate[3, 2]*temp[2, 2]+temp[2, 3]

        path[idx, 4, 0] = standby_coordinate[4, 0]*temp[0, 0]+standby_coordinate[4,
                                                                                 1]*temp[0, 1]+standby_coordinate[4, 2]*temp[0, 2]+temp[0, 3]
        path[idx, 4, 1] = standby_coordinate[4, 0]*temp[1, 0]+standby_coordinate[4,
                                                                                 1]*temp[1, 1]+standby_coordinate[4, 2]*temp[1, 2]+temp[1, 3]
        path[idx, 4, 2] = standby_coordinate[4, 0]*temp[2, 0]+standby_coordinate[4,
                                                                                 1]*temp[2, 1]+standby_coordinate[4, 2]*temp[2, 2]+temp[2, 3]

        path[idx, 5, 0] = standby_coordinate[5, 0]*temp[0, 0]+standby_coordinate[5,
                                                                                 1]*temp[0, 1]+standby_coordinate[5, 2]*temp[0, 2]+temp[0, 3]
        path[idx, 5, 1] = standby_coordinate[5, 0]*temp[1, 0]+standby_coordinate[5,
                                                                                 1]*temp[1, 1]+standby_coordinate[5, 2]*temp[1, 2]+temp[1, 3]
        path[idx, 5, 2] = standby_coordinate[5, 0]*temp[2, 0]+standby_coordinate[5,
                                                                                 1]*temp[2, 1]+standby_coordinate[5, 2]*temp[2, 2]+temp[2, 3]
    for i in range(quarter):
        temp = m * get_rotate_z_matrix((quarter-i)*step_x_angle) * \
            get_rotate_x_matrix((quarter-i)*step_y_angle)
        idx = i+quarter*1

        path[idx, 0, 0] = standby_coordinate[0, 0]*temp[0, 0]+standby_coordinate[0,
                                                                                 1]*temp[0, 1]+standby_coordinate[0, 2]*temp[0, 2]+temp[0, 3]
        path[idx, 0, 1] = standby_coordinate[0, 0]*temp[1, 0]+standby_coordinate[0,
                                                                                 1]*temp[1, 1]+standby_coordinate[0, 2]*temp[1, 2]+temp[1, 3]
        path[idx, 0, 2] = standby_coordinate[0, 0]*temp[2, 0]+standby_coordinate[0,
                                                                                 1]*temp[2, 1]+standby_coordinate[0, 2]*temp[2, 2]+temp[2, 3]

        path[idx, 1, 0] = standby_coordinate[1, 0]*temp[0, 0]+standby_coordinate[1,
                                                                                 1]*temp[0, 1]+standby_coordinate[1, 2]*temp[0, 2]+temp[0, 3]
        path[idx, 1, 1] = standby_coordinate[1, 0]*temp[1, 0]+standby_coordinate[1,
                                                                                 1]*temp[1, 1]+standby_coordinate[1, 2]*temp[1, 2]+temp[1, 3]
        path[idx, 1, 2] = standby_coordinate[1, 0]*temp[2, 0]+standby_coordinate[1,
                                                                                 1]*temp[2, 1]+standby_coordinate[1, 2]*temp[2, 2]+temp[2, 3]

        path[idx, 2, 0] = standby_coordinate[2, 0]*temp[0, 0]+standby_coordinate[2,
                                                                                 1]*temp[0, 1]+standby_coordinate[2, 2]*temp[0, 2]+temp[0, 3]
        path[idx, 2, 1] = standby_coordinate[2, 0]*temp[1, 0]+standby_coordinate[2,
                                                                                 1]*temp[1, 1]+standby_coordinate[2, 2]*temp[1, 2]+temp[1, 3]
        path[idx, 2, 2] = standby_coordinate[2, 0]*temp[2, 0]+standby_coordinate[2,
                                                                                 1]*temp[2, 1]+standby_coordinate[2, 2]*temp[2, 2]+temp[2, 3]

        path[idx, 3, 0] = standby_coordinate[3, 0]*temp[0, 0]+standby_coordinate[3,
                                                                                 1]*temp[0, 1]+standby_coordinate[3, 2]*temp[0, 2]+temp[0, 3]
        path[idx, 3, 1] = standby_coordinate[3, 0]*temp[1, 0]+standby_coordinate[3,
                                                                                 1]*temp[1, 1]+standby_coordinate[3, 2]*temp[1, 2]+temp[1, 3]
        path[idx, 3, 2] = standby_coordinate[3, 0]*temp[2, 0]+standby_coordinate[3,
                                                                                 1]*temp[2, 1]+standby_coordinate[3, 2]*temp[2, 2]+temp[2, 3]

        path[idx, 4, 0] = standby_coordinate[4, 0]*temp[0, 0]+standby_coordinate[4,
                                                                                 1]*temp[0, 1]+standby_coordinate[4, 2]*temp[0, 2]+temp[0, 3]
        path[idx, 4, 1] = standby_coordinate[4, 0]*temp[1, 0]+standby_coordinate[4,
                                                                                 1]*temp[1, 1]+standby_coordinate[4, 2]*temp[1, 2]+temp[1, 3]
        path[idx, 4, 2] = standby_coordinate[4, 0]*temp[2, 0]+standby_coordinate[4,
                                                                                 1]*temp[2, 1]+standby_coordinate[4, 2]*temp[2, 2]+temp[2, 3]

        path[idx, 5, 0] = standby_coordinate[5, 0]*temp[0, 0]+standby_coordinate[5,
                                                                                 1]*temp[0, 1]+standby_coordinate[5, 2]*temp[0, 2]+temp[0, 3]
        path[idx, 5, 1] = standby_coordinate[5, 0]*temp[1, 0]+standby_coordinate[5,
                                                                                 1]*temp[1, 1]+standby_coordinate[5, 2]*temp[1, 2]+temp[1, 3]
        path[idx, 5, 2] = standby_coordinate[5, 0]*temp[2, 0]+standby_coordinate[5,
                                                                                 1]*temp[2, 1]+standby_coordinate[5, 2]*temp[2, 2]+temp[2, 3]
    for i in range(quarter):
        temp = m * get_rotate_z_matrix(-i*step_x_angle) * \
            get_rotate_x_matrix(i*step_y_angle)
        idx = i+quarter*2

        path[idx, 0, 0] = standby_coordinate[0, 0]*temp[0, 0]+standby_coordinate[0,
                                                                                 1]*temp[0, 1]+standby_coordinate[0, 2]*temp[0, 2]+temp[0, 3]
        path[idx, 0, 1] = standby_coordinate[0, 0]*temp[1, 0]+standby_coordinate[0,
                                                                                 1]*temp[1, 1]+standby_coordinate[0, 2]*temp[1, 2]+temp[1, 3]
        path[idx, 0, 2] = standby_coordinate[0, 0]*temp[2, 0]+standby_coordinate[0,
                                                                                 1]*temp[2, 1]+standby_coordinate[0, 2]*temp[2, 2]+temp[2, 3]

        path[idx, 1, 0] = standby_coordinate[1, 0]*temp[0, 0]+standby_coordinate[1,
                                                                                 1]*temp[0, 1]+standby_coordinate[1, 2]*temp[0, 2]+temp[0, 3]
        path[idx, 1, 1] = standby_coordinate[1, 0]*temp[1, 0]+standby_coordinate[1,
                                                                                 1]*temp[1, 1]+standby_coordinate[1, 2]*temp[1, 2]+temp[1, 3]
        path[idx, 1, 2] = standby_coordinate[1, 0]*temp[2, 0]+standby_coordinate[1,
                                                                                 1]*temp[2, 1]+standby_coordinate[1, 2]*temp[2, 2]+temp[2, 3]

        path[idx, 2, 0] = standby_coordinate[2, 0]*temp[0, 0]+standby_coordinate[2,
                                                                                 1]*temp[0, 1]+standby_coordinate[2, 2]*temp[0, 2]+temp[0, 3]
        path[idx, 2, 1] = standby_coordinate[2, 0]*temp[1, 0]+standby_coordinate[2,
                                                                                 1]*temp[1, 1]+standby_coordinate[2, 2]*temp[1, 2]+temp[1, 3]
        path[idx, 2, 2] = standby_coordinate[2, 0]*temp[2, 0]+standby_coordinate[2,
                                                                                 1]*temp[2, 1]+standby_coordinate[2, 2]*temp[2, 2]+temp[2, 3]

        path[idx, 3, 0] = standby_coordinate[3, 0]*temp[0, 0]+standby_coordinate[3,
                                                                                 1]*temp[0, 1]+standby_coordinate[3, 2]*temp[0, 2]+temp[0, 3]
        path[idx, 3, 1] = standby_coordinate[3, 0]*temp[1, 0]+standby_coordinate[3,
                                                                                 1]*temp[1, 1]+standby_coordinate[3, 2]*temp[1, 2]+temp[1, 3]
        path[idx, 3, 2] = standby_coordinate[3, 0]*temp[2, 0]+standby_coordinate[3,
                                                                                 1]*temp[2, 1]+standby_coordinate[3, 2]*temp[2, 2]+temp[2, 3]

        path[idx, 4, 0] = standby_coordinate[4, 0]*temp[0, 0]+standby_coordinate[4,
                                                                                 1]*temp[0, 1]+standby_coordinate[4, 2]*temp[0, 2]+temp[0, 3]
        path[idx, 4, 1] = standby_coordinate[4, 0]*temp[1, 0]+standby_coordinate[4,
                                                                                 1]*temp[1, 1]+standby_coordinate[4, 2]*temp[1, 2]+temp[1, 3]
        path[idx, 4, 2] = standby_coordinate[4, 0]*temp[2, 0]+standby_coordinate[4,
                                                                                 1]*temp[2, 1]+standby_coordinate[4, 2]*temp[2, 2]+temp[2, 3]

        path[idx, 5, 0] = standby_coordinate[5, 0]*temp[0, 0]+standby_coordinate[5,
                                                                                 1]*temp[0, 1]+standby_coordinate[5, 2]*temp[0, 2]+temp[0, 3]
        path[idx, 5, 1] = standby_coordinate[5, 0]*temp[1, 0]+standby_coordinate[5,
                                                                                 1]*temp[1, 1]+standby_coordinate[5, 2]*temp[1, 2]+temp[1, 3]
        path[idx, 5, 2] = standby_coordinate[5, 0]*temp[2, 0]+standby_coordinate[5,
                                                                                 1]*temp[2, 1]+standby_coordinate[5, 2]*temp[2, 2]+temp[2, 3]
    for i in range(quarter):
        temp = m * get_rotate_z_matrix((-quarter+i)*step_x_angle) * \
            get_rotate_x_matrix((quarter-i)*step_y_angle)
        idx = i+quarter*3

        path[idx, 0, 0] = standby_coordinate[0, 0]*temp[0, 0]+standby_coordinate[0,
                                                                                 1]*temp[0, 1]+standby_coordinate[0, 2]*temp[0, 2]+temp[0, 3]
        path[idx, 0, 1] = standby_coordinate[0, 0]*temp[1, 0]+standby_coordinate[0,
                                                                                 1]*temp[1, 1]+standby_coordinate[0, 2]*temp[1, 2]+temp[1, 3]
        path[idx, 0, 2] = standby_coordinate[0, 0]*temp[2, 0]+standby_coordinate[0,
                                                                                 1]*temp[2, 1]+standby_coordinate[0, 2]*temp[2, 2]+temp[2, 3]

        path[idx, 1, 0] = standby_coordinate[1, 0]*temp[0, 0]+standby_coordinate[1,
                                                                                 1]*temp[0, 1]+standby_coordinate[1, 2]*temp[0, 2]+temp[0, 3]
        path[idx, 1, 1] = standby_coordinate[1, 0]*temp[1, 0]+standby_coordinate[1,
                                                                                 1]*temp[1, 1]+standby_coordinate[1, 2]*temp[1, 2]+temp[1, 3]
        path[idx, 1, 2] = standby_coordinate[1, 0]*temp[2, 0]+standby_coordinate[1,
                                                                                 1]*temp[2, 1]+standby_coordinate[1, 2]*temp[2, 2]+temp[2, 3]

        path[idx, 2, 0] = standby_coordinate[2, 0]*temp[0, 0]+standby_coordinate[2,
                                                                                 1]*temp[0, 1]+standby_coordinate[2, 2]*temp[0, 2]+temp[0, 3]
        path[idx, 2, 1] = standby_coordinate[2, 0]*temp[1, 0]+standby_coordinate[2,
                                                                                 1]*temp[1, 1]+standby_coordinate[2, 2]*temp[1, 2]+temp[1, 3]
        path[idx, 2, 2] = standby_coordinate[2, 0]*temp[2, 0]+standby_coordinate[2,
                                                                                 1]*temp[2, 1]+standby_coordinate[2, 2]*temp[2, 2]+temp[2, 3]

        path[idx, 3, 0] = standby_coordinate[3, 0]*temp[0, 0]+standby_coordinate[3,
                                                                                 1]*temp[0, 1]+standby_coordinate[3, 2]*temp[0, 2]+temp[0, 3]
        path[idx, 3, 1] = standby_coordinate[3, 0]*temp[1, 0]+standby_coordinate[3,
                                                                                 1]*temp[1, 1]+standby_coordinate[3, 2]*temp[1, 2]+temp[1, 3]
        path[idx, 3, 2] = standby_coordinate[3, 0]*temp[2, 0]+standby_coordinate[3,
                                                                                 1]*temp[2, 1]+standby_coordinate[3, 2]*temp[2, 2]+temp[2, 3]

        path[idx, 4, 0] = standby_coordinate[4, 0]*temp[0, 0]+standby_coordinate[4,
                                                                                 1]*temp[0, 1]+standby_coordinate[4, 2]*temp[0, 2]+temp[0, 3]
        path[idx, 4, 1] = standby_coordinate[4, 0]*temp[1, 0]+standby_coordinate[4,
                                                                                 1]*temp[1, 1]+standby_coordinate[4, 2]*temp[1, 2]+temp[1, 3]
        path[idx, 4, 2] = standby_coordinate[4, 0]*temp[2, 0]+standby_coordinate[4,
                                                                                 1]*temp[2, 1]+standby_coordinate[4, 2]*temp[2, 2]+temp[2, 3]

        path[idx, 5, 0] = standby_coordinate[5, 0]*temp[0, 0]+standby_coordinate[5,
                                                                                 1]*temp[0, 1]+standby_coordinate[5, 2]*temp[0, 2]+temp[0, 3]
        path[idx, 5, 1] = standby_coordinate[5, 0]*temp[1, 0]+standby_coordinate[5,
                                                                                 1]*temp[1, 1]+standby_coordinate[5, 2]*temp[1, 2]+temp[1, 3]
        path[idx, 5, 2] = standby_coordinate[5, 0]*temp[2, 0]+standby_coordinate[5,
                                                                                 1]*temp[2, 1]+standby_coordinate[5, 2]*temp[2, 2]+temp[2, 3]

    return path
