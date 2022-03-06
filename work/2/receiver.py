import threading
import socket
import json
import matplotlib.pyplot as plt
import numpy as np
import math
from array import array

_ENDPOINT = ("127.0.0.1", 10000)

vel = {
    "x": 0.0,
    "w": 0.0
}
pos = {
    "x": 0.0,
    "y": 0.0,
    "theta": 0.0
}

x_traj = []
y_traj = []

def calc(pos, vel, dt):
    r = np.array(
        [math.cos(pos["theta"]), -math.sin(pos["theta"]), 0, math.sin(pos["theta"]), math.cos(pos["theta"]), 0, 0, 0,
         1])
    r = r.reshape(3, 3)
    deltaposrel = np.array([vel["x"] * dt, 0, vel["w"] * dt])
    deltaposabs = np.matmul(r, deltaposrel)
    pos["x"] += deltaposabs[0]
    pos["y"] += deltaposabs[1]
    pos["theta"] += deltaposabs[2]


def transformation_matrix(theta):
    r = np.array([math.cos(theta), -math.sin(theta), 0, math.sin(theta), math.cos(theta), 0, 0, 0, 1])
    return r.reshape(3, 3)


def plot_vehicle(x, y, theta, x_traj, y_traj, dt):
    p1_i = np.array([0.5, 0, 1]).T
    p2_i = np.array([-0.5, 0.25, 1]).T
    p3_i = np.array([-0.5, -0.25, 1]).T
    pxy = np.array([x, y, 0]).T

    T = transformation_matrix(theta)
    p1 = np.matmul(T, p1_i) + pxy
    p2 = np.matmul(T, p2_i) + pxy
    p3 = np.matmul(T, p3_i) + pxy

    plt.plot([p1[0], p2[0]], [p1[1], p2[1]], 'k-')
    plt.plot([p2[0], p3[0]], [p2[1], p3[1]], 'k-')
    plt.plot([p3[0], p1[0]], [p3[1], p1[1]], 'k-')

    plt.plot(x_traj, y_traj, 'b--')

    plt.xlim(x-5, x+5)
    plt.ylim(y-5, y+5)

    plt.pause(dt)


def receive():
    global vel

    while True:
        data, addr = sock.recvfrom(65535)
        data = data.decode()
        vel = json.loads(data)


def draw(pos, pause_t):
    x = pos["x"]
    y = pos["y"]
    theta = pos["theta"]
    plot_vehicle(x, y, theta, x_traj, y_traj, dt)


if __name__ == "__main__":

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(_ENDPOINT)

    t = threading.Thread(target=receive)
    t.start()

    dt = 1

    traj = np.array([0, 0])
    traj = traj.reshape(2, 1)

    while True:
        calc(pos, vel, dt)
        x_traj.append(pos["x"])
        y_traj.append(pos["y"])
        print(pos)
        draw(pos, dt)
