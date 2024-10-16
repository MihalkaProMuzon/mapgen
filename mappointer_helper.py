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
    WARNING = '\033[31m'
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



def path_finder(links, point_from_i, point_to_i):    
    nbrs = [point_from_i]
    next_nbrs = []

    distances = {point_from_i: {"dst": 0}}

    i = 0
    while(True):
        if len(nbrs) < 1:
            break
        
        i += 1
        print_rewrite(f"{bcolors.OKCYAN}Прокладываем маршрут #{i}")
        for p_i in nbrs:
            dst = distances[p_i]["dst"] + 1
            for nbr_p_i in links[p_i]["link_points"]:
                if nbr_p_i not in distances:
                    distances[nbr_p_i] = {
                        "dst": dst,
                        "lnk": p_i
                    }
                    next_nbrs.append(nbr_p_i)

                if distances[nbr_p_i]["dst"] > dst:
                    distances[nbr_p_i]["dst"] = dst
                    distances[nbr_p_i]["lnk"] = p_i
                    next_nbrs.append(nbr_p_i)

        nbrs = next_nbrs
        next_nbrs = []
    
    if point_to_i not in distances:
        print_rewrite(f"{bcolors.WARNING}Маршрут не найден;")
        return
    
    print_rewrite(f"{bcolors.OKGREEN} Длина найденого маршрута - {distances[point_to_i]["dst"]}; {bcolors.RESET}")

    return distances