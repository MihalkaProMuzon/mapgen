import numpy as np
import math
import random
import pygame
import time
from pygame.locals import *
from OpenGL.GL import * 
from OpenGL.GLU import * 
from OpenGL.GLUT import *
import colorama

from mappointer_helper import *
from mappointer_config import *



def raycast_select(points, mpos, camera_pos, camera_front):
	camera_pos = np.array(camera_pos)
	camera_front = np.array(camera_front)

	iterpoint = camera_pos
	for _ in range(100):
		iterpoint = iterpoint + camera_front * 0.2
		for point_i, point in enumerate(points):
			if in_distance(iterpoint, point["pos"], 0.5):
				select_point(points, point_i)
				return


selected_points = {}
def select_point(points, point_i):
	if point_i in selected_points:
		return
	point = points[point_i]
	selected_points[point_i] = point["type"]
	point["type"] = "selected"


def actionA(points, links):
	global selected_points
	print("Снять выделения;")
	for selpoint_i,type in selected_points.items():
		points[selpoint_i]["type"] = type

	selected_points = {}


def actionB(points, links):
	global selected_points
	print("Проложить маршрут:")
	if len(selected_points) != 2:
		print("  выделенных вершин должно быть 2!;")
		return


	


	print(" прокладывается")


def actionC(points, links):
	print("Актион C")