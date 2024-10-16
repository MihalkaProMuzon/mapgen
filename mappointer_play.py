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

def raycast_select(mpos, camera_pos, camera_front):
	camera_pos = np.array(camera_pos)
	camera_front = np.array(camera_front)

	iterpoint = camera_pos
	for _ in range(100):
		iterpoint = iterpoint + camera_front * 0.2
		for point_i, point in enumerate(Map.points):
			if in_distance(iterpoint, point["pos"], 0.5):
				select_point(point_i)
				return

def select_point(point_i):
    if point_i in Map.selected_points:
        return
    point = Map.points[point_i]
    Map.selected_points[point_i] = point["type"]
    point["type"] = "selected"

def select_link(point_a, point_b):
    if not point_a in Map.selected_links:
        Map.selected_links[point_a] = {}
    if not point_b in Map.selected_links[point_a]:
    	Map.selected_links[point_a][point_b] = Map.links[point_a]["link_points"][point_b]

    if not point_b in Map.selected_links:
        Map.selected_links[point_b] = {}
    if not point_a in Map.selected_links[point_b]:
    	Map.selected_links[point_b][point_a] = Map.links[point_b]["link_points"][point_a]

    Map.links[point_a]["link_points"][point_b] = "selected_link"
    Map.links[point_b]["link_points"][point_a] = "selected_link"

def deselect_all():
    for selpoint_i,type in Map.selected_points.items():
        Map.points[selpoint_i]["type"] = type
    Map.selected_points = {}

    for sellink_i,val in Map.selected_links.items():
        for selnbr_i,type in val.items():
            Map.links[sellink_i]["link_points"][selnbr_i] = type
    Map.selected_links = {}







def actionA():
	print("Снять выделения;")
	deselect_all()

def actionB():
	print("Проложить маршрут:")
	if len(Map.selected_points) != 2:
		print(f"{bcolors.WARNING} выделенных вершин должно быть 2!;{bcolors.RESET}")
		return

	points_path = []
	for k, v in Map.selected_points.items():
		points_path.append(k)
	

	print_rewrite(f"Проложить маршрут {points_path[0]} - {points_path[1]}:")
	print(" прокладывается")
	point_from_i = points_path[0]
	point_to_i = points_path[1]
	distances = path_finder(Map.links, point_from_i, point_to_i)	

	iter_point = point_to_i
	while(True):
		next_point = distances[iter_point]["lnk"]
		select_link(iter_point, next_point)
		if next_point == point_from_i:
			break
		iter_point = next_point


def actionC():
	print("Актион C;")