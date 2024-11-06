import os
import argparse
import math as m
import numpy as np
from matplotlib import pyplot as plt
from hyperpyyaml import load_hyperpyyaml
from PIL import Image


def make_graph():
    fig = plt.figure()
    plt.axis([-5, 5, -5, 5])
    plt.xticks(np.arange(-5, 5, 1))
    plt.yticks(np.arange(-5, 5, 1))
    plt.grid()
    plt.axline((0, 0), (1, 0), color='black', linewidth=1)
    plt.axline((0, 0), (0, 1), color='black', linewidth=1)
    plt.scatter(0, 0, color='black')
    return fig

def make_gif(cnt, mx, my, x, y, rdir):
    frames = []
    mx, my = round(mx), round(my)
    x, y = round(x + mx), round(y + my)
    for i in range(1, cnt + 1):
        frame = Image.open(f'pos_rob_{i}.png')
        frames.append(frame)
    frames[0].save(f'{rdir}from({mx},{my})to({x},{y}).gif', save_all=True,
                   append_images=frames[1:], optimize=True, duration=50)
    for i in range(1, cnt + 1):
        os.remove(f'pos_rob_{i}.png')

def arg_pars(file):
    parser = argparse.ArgumentParser()
    parser.add_argument(file, type=str, help='file containing all arguments')
    with open(file, 'r') as inf:
        args = load_hyperpyyaml(inf)
    return args


class RobotPosition:
    def __init__(self, args): 
        self.args = args

    def writing_coords(self):
        with open('data.yml', 'w') as ouf:
            for k, v in self.args.items():
                ouf.write(f'{k}: {v}\n')

    def laser(self, pnt, crn, i):
        corn = str(crn[i]).replace('pi', str(m.pi)).split('/')
        if len(corn) == 1:
            corn = float(corn[0]) + np.deg2rad(self.args['deg'])
        else:
            corn, div = map(float, corn)
            corn = corn / div + np.deg2rad(self.args['deg'])
        x, y = pnt[i][0], pnt[i][1]
        deg = str(self.args['sensor_geo']).replace('pi', str(m.pi)).split('/')
        pi, div = map(float, deg)
        deg = pi / div
        arc_l = corn - deg
        xl, yl = x + self.args['sensor_len'] * np.cos(arc_l), y + self.args['sensor_len'] * np.sin(arc_l)
        arc_r = corn + deg
        xr, yr = x + self.args['sensor_len'] * np.cos(arc_r), y + self.args['sensor_len'] * np.sin(arc_r)
        return x, y, arc_l, arc_r, [(x, y), (xl, yl), (xr, yr)]

    def pos_rob(self, fig):
        arr = self.args['car']
        car = plt.Polygon(arr, color='black', fill=True)
        ax = plt.gca()
        ax.add_patch(car)
        pnt, crn = self.args['sensor'], self.args['sensor_corners']
        r = self.args['sensor_len']
        for i in range(len(pnt)):
            x, y, arc_l, arc_r, coords = self.laser(pnt, crn, i)
            laser = plt.Polygon(coords, color='red', fill=True)
            ax.add_patch(laser)
            plt.scatter(x, y, color='blue', linewidths=5)
            theta = np.linspace(arc_l, arc_r, 100)
            rx = r * np.cos(theta) + x
            ry = r * np.sin(theta) + y
            mass = [(rx[i], ry[i]) for i in range(len(rx))]
            laser = plt.Polygon(mass, color='red', fill=True)
            ax.add_patch(laser)
        return fig

    def turn(self, deg):
        self.args['deg'] = (self.args['deg'] + deg) % 360
        mid = self.args['mid']
        basic = [[np.cos(np.deg2rad(deg)), np.sin(np.deg2rad(deg))],
                 [-np.sin(np.deg2rad(deg)), np.cos(np.deg2rad(deg))]]
        T = np.transpose(basic)
        for i in range(len(self.args['car'])):
            coord = self.args['car'][i]
            coord = np.matmul(T, np.subtract(coord, mid))
            self.args['car'][i] = np.add(coord, mid).tolist()
        for i in range(len(self.args['sensor'])):
            coord = self.args['sensor'][i]
            coord = np.matmul(T, np.subtract(coord, mid))
            self.args['sensor'][i] = np.add(coord, mid).tolist()

    def position(self, x, y):
        self.args['mid'][0] += x
        self.args['mid'][1] += y
        for i in range(len(self.args['car'])):
            self.args['car'][i][0] += x
            self.args['car'][i][1] += y
        for i in range(len(self.args['sensor'])):
            self.args['sensor'][i][0] += x
            self.args['sensor'][i][1] += y

    def movement(self, x, y, rdir):
        v1, v2 = self.args['sensor'][2], [x, y]
        mx, my = map(int, self.args['mid'])
        mid = self.args['mid']
        x, y = x - mx, y - my
        v1, v2 = np.subtract(v1, mid), np.subtract(v2, mid)
        cos = np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))
        deg = np.rad2deg(np.arccos(cos))
        T = [[np.cos(np.deg2rad(deg)), np.sin(np.deg2rad(deg))],
            [-np.sin(np.deg2rad(deg)), np.cos(np.deg2rad(deg))]]
        a = np.matmul(T, np.transpose(v1))
        deg *= -1
        T = [[np.cos(np.deg2rad(deg)), np.sin(np.deg2rad(deg))],
             [-np.sin(np.deg2rad(deg)), np.cos(np.deg2rad(deg))]]
        b = np.matmul(T, np.transpose(v1))
        deg *= -1
        a, b = np.subtract(v2, a), np.subtract(v2, b)
        a, b = abs(a[0]) + abs(a[1]), abs(b[0]) + abs(b[1])
        if a < b:
            k = -1
        else:
            k = 1
        cnt_t = m.ceil(deg/10) * 2
        deg = deg * k * (1/cnt_t)
        for i in range(1, cnt_t + 1):
            self.turn(deg)
            fig = self.pos_rob(make_graph())
            fig.savefig(f'pos_rob_{i}.png')
            plt.close(fig)
        cnt_m = m.ceil(np.linalg.norm([x, y])) * 5
        step_x, step_y = x * (1/cnt_m), y * (1/cnt_m)
        for i in range(1, cnt_m + 1):
            self.position(step_x, step_y)
            fig = self.pos_rob(make_graph())
            fig.savefig(f'pos_rob_{i+cnt_t}.png')
            plt.close(fig)
        make_gif(cnt_m + cnt_t, mx, my, x, y, rdir)
