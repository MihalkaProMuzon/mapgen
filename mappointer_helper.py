import numpy as np
import random
import sys
from pygame.locals import *
from OpenGL.GL import * 
from OpenGL.GLU import * 
from OpenGL.GLUT import *

# PLS HELP!!!

class bcolors:
    HEADER = '\033[95m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    RESET = '\033[0m'

def normalize(v):
    norm = np.linalg.norm(v)  # Вычисление длины вектора
    if norm == 0:
        return v  # Возвращаем исходный вектор, если его длина равна нулю
    return v / norm  # Делим вектор на его длину

def points_dist(a, b):
    return np.linalg.norm(np.array(a["pos"]) - np.array(b["pos"]))

def in_distance(a, b, dist):
    calcDist = np.pow(a[0] - b[0],2) + np.pow(a[1] - b[1],2) + np.pow(a[2] - b[2],2)
    distPow = dist * dist
    return calcDist < distPow


def throw_with_сhance(chance):
    random_number = random.uniform(0, 1)
    return random_number <= chance

def print_rewrite(text):
    sys.stdout.write('\033[F')
    sys.stdout.write('\033[K')
    print(text)



def path_finder_iter(points,path,visted):


def path_finder(links, point_from_i, point_to_i):
    lnk_point_from = links[point_from_i]
    lnk_point_to = links[point_to_i]
    
    

    
    lnk_point_from_nbrs = lnk_point_from["link_points"]
    for lnk in lnk_point_from_nbrs:
        path = path_finder_iter()

