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

import mappointer_generator as mapgen
import mappointer_play as play
from mappointer_helper import *
from mappointer_config import *

colorama.init()


class Map:
	points = mapgen.generate_points(points_args)	
	links = mapgen.create_links(points, links_args)
	selected_points = {}
	selected_links = {}

play.Map = Map

mapgen.test(Map.points, Map.links)
print(bcolors.RESET)

def draw_point(point, tick, index):
	if not point["type"] in POINT_TYPES:
		print(f"Для точек {point['type']} не заданы параметры отрисовки!")
		return

	param = POINT_TYPES[point["type"]]

	glPushMatrix()
	glTranslatef(*point["pos"])
	# glRotate(*rot)

	col = param["point_col"]
	if GLARE_DRAW:
		col = np.array(col)
		pos = point["pos"]
		col += np.cos(tick * GLARE_SPEED  + index) * GLARE_POWER
		glColor3f(*param["point_col"])

	glColor3f(*col)	

	quadric = gluNewQuadric()
	gluSphere(quadric, param["point_size"], 4, 2)
	gluDeleteQuadric(quadric)
	
	glPopMatrix()

def draw_line(link_type, pos1,pos2):
    if not link_type in LINK_TYPES:
    	print(f"Палки {link['type']} не имеют параметров отрисовки!")
    	return
    param = LINK_TYPES[link_type]

    glBegin(GL_LINES)
    glColor3f(*param["line_col"])

    lcount = param["lines_count"]

    if lcount == 1:
    	glVertex3f(*pos1)
    	glVertex3f(*pos2)
    else:
        sprd = param["lines_spread"]
        posshifts = np.linspace(-sprd, sprd, lcount)
        for shift in posshifts:
            glVertex3f(pos1[0],pos1[1] + shift, pos1[2])
            glVertex3f(pos2[0],pos2[1] + shift, pos2[2])
    
    glEnd()          

key_state = {
	"exit": False,

	"mov_frwd": False,
	"mov_left": False,
	"mov_back": False,
	"mov_right": False,
	"mov_up": False,
	"mov_down": False,

	"up" : False,
	"down" : False,
	"left" : False,
	"right" : False,

	"boost" : False,

	"action1": False,
	"action2": False,
	"actionA": False,
	"actionB": False,
	"actionC": False,

	"m_clk_pos": (0,0),
	"m_clk_iterX": 0,
	"m_clk_iterY": 0,
	"m_clk_yaw": 0,
	"m_clk_pitch": 0,
}

key_mapping = {
	pygame.K_z: 'exit',
	pygame.K_w: 'mov_frwd',
	pygame.K_s: 'mov_back',
	pygame.K_a: 'mov_left',
	pygame.K_d: 'mov_right',
	pygame.K_e: 'mov_up',
	pygame.K_q: 'mov_down',
	pygame.K_LSHIFT: 'boost',
	pygame.K_RSHIFT: 'boost',
	pygame.K_UP: 'up',
	pygame.K_DOWN: 'down',
	pygame.K_1: 'actionA',
	pygame.K_2: 'actionB',
	pygame.K_3: 'actionC',
}



def rotate_y(matrix, angle):
	theta = np.radians(angle)
	rotation_y = np.array([[np.cos(theta), 0, np.sin(theta)],
							[0, 1, 0],
							[-np.sin(theta), 0, np.cos(theta)]])
	return np.dot(matrix, rotation_y)

def rotate_x(matrix, angle):
	theta = np.radians(angle)
	rotation_x = np.array([[1, 0, 0],
							[0, np.cos(theta), -np.sin(theta)],
							[0, np.sin(theta), np.cos(theta)]])
	return np.dot(matrix, rotation_x)




def main():
	global key_state, key_mapping, points, links

	pygame.init()
	display = DISPLAY_SIZE
	pygame.display.set_mode(display, DOUBLEBUF|OPENGL)
	glEnable(GL_DEPTH_TEST)

	camera_pos = np.array(CAM_START_POS)
	yaw = CAM_START_YAW
	pitch = CAM_START_PITCH
	mov_speed = 0.1

	clock = pygame.time.Clock()

	while True:
		tick = pygame.time.get_ticks()
		points = Map.points
		links = Map.links
		# Some cam math ##############################			#
		
		camera_rotation = np.array([[0, 0, 1],
									[0, 1, 0],
									[1, 0, 0]])
		camera_rotation = rotate_x(camera_rotation, -pitch)		
		camera_rotation = rotate_y(camera_rotation, yaw)
		

		camera_front = camera_rotation[0]
		camera_up = camera_rotation[1]
		camera_right = -camera_rotation[2]
	
		# Keys ##############################					#
		for event in pygame.event.get():
			if event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
				state = event.type == pygame.KEYDOWN
				if event.key in key_mapping:
					key_state[key_mapping[event.key]] = state

			if event.type == pygame.MOUSEBUTTONDOWN:
				pygame.mouse.set_visible(False)
				key_state['m_clk_pos'] =  pygame.mouse.get_pos()
				key_state['m_clk_iterX'] =  0
				key_state['m_clk_iterY'] =  0
				key_state['m_clk_yaw'] = yaw
				key_state['m_clk_pitch'] = pitch
				if event.button == 1:
					key_state['action1'] = True
				elif event.button == 3:
					key_state['action2'] = not key_state['action2']
					pygame.mouse.set_visible(not key_state['action2'])


			if event.type == pygame.MOUSEBUTTONUP:
				if event.button == 1:
					pygame.mouse.set_visible(not key_state['action2'])
					key_state['action1'] = False

		# Handle Keys ##############################			#
		if key_state['exit']:
			pygame.quit()
			quit()

		if key_state['mov_frwd']:
			camera_pos += mov_speed * camera_front
		if key_state['mov_back']:
			camera_pos -= mov_speed * camera_front
		if key_state['mov_up']:
			camera_pos += mov_speed * camera_up
		if key_state['mov_down']:
			camera_pos -= mov_speed * camera_up
		if key_state['mov_left']:
			camera_pos -= mov_speed * camera_right
		if key_state['mov_right']:
			camera_pos += mov_speed * camera_right
		
		if key_state['right']:
			yaw += ARROWS_SENSITIVITY
			key_state["m_clk_yaw"] += ARROWS_SENSITIVITY
		if key_state['left']:
			yaw -= ARROWS_SENSITIVITY
			key_state["m_clk_yaw"] -= ARROWS_SENSITIVITY
		if key_state['up']:
			pitch -= ARROWS_SENSITIVITY
			key_state["m_clk_pitch"] -= ARROWS_SENSITIVITY
		if key_state['down']:
			pitch += ARROWS_SENSITIVITY
			key_state["m_clk_pitch"] += ARROWS_SENSITIVITY

		if key_state['boost']:
			mov_speed = MOV_SPEED_BOOSTED
		else:
			mov_speed = MOV_SPEED_BASE

		if key_state["actionA"]:
			play.actionA()
			key_state["actionA"] = False
		if key_state["actionB"]:
			play.actionB()
			key_state["actionB"] = False
		if key_state["actionC"]:
			play.actionC()
			key_state["actionC"] = False

		if key_state["action1"]:
			mpos = pygame.mouse.get_pos()
			play.raycast_select(mpos, camera_pos, camera_front)
			key_state["action1"] = False

		if key_state["action2"]:
			mpos = pygame.mouse.get_pos()
			saved_position = key_state["m_clk_pos"]

			offset_x = mpos[0] - saved_position[0]
			offset_y = mpos[1] - saved_position[1]

			if offset_x > MOUSE_RETURN_DISTANCE:
				mpos = (saved_position[0],mpos[1])
				pygame.mouse.set_pos(mpos[0],mpos[1])
				key_state["m_clk_iterX"] += 1
			if offset_x < -MOUSE_RETURN_DISTANCE:
				mpos = (saved_position[0],mpos[1])
				pygame.mouse.set_pos(mpos[0],mpos[1])
				key_state["m_clk_iterX"] -= 1
			if offset_y > MOUSE_RETURN_DISTANCE:
				mpos = (mpos[0], saved_position[1])
				pygame.mouse.set_pos(mpos[0],mpos[1])
				key_state["m_clk_iterY"] += 1
			if offset_y < -MOUSE_RETURN_DISTANCE:
				mpos = (mpos[0], saved_position[1])
				pygame.mouse.set_pos(mpos[0],mpos[1])
				key_state["m_clk_iterY"] -= 1

			offset_x = mpos[0] - saved_position[0]
			offset_y = mpos[1] - saved_position[1]

			yaw =  key_state["m_clk_yaw"] + (offset_x + MOUSE_RETURN_DISTANCE*key_state["m_clk_iterX"]) * MOUSE_SENSITIVITY
			pitch = key_state["m_clk_pitch"] + (offset_y + MOUSE_RETURN_DISTANCE*key_state["m_clk_iterY"]) * MOUSE_SENSITIVITY





		# Draw ##############################					#
		glClearColor(*BACK_COL, 1.0) 
		glLoadIdentity()
		gluPerspective(45, display[0]/display[1], 0.1, 1000.0)
	
		gluLookAt(*camera_pos, * (camera_pos + camera_front), *camera_up)

		drawed_links = {}
		for link_indx, linkV in links.items():
			p1 = points[link_indx]
			for p2_indx, link_type in linkV['link_points'].items():
				k1 = f"{link_indx}-{p2_indx}"
				k2 = f"{p2_indx}-{link_indx}"
				if not ((k1 in drawed_links) or (k2 in drawed_links)):
					p2 = points[p2_indx]
					draw_line(link_type, p1["pos"], p2["pos"])
					drawed_links[k1] = True
					drawed_links[k2] = True

		pI = 0
		for point in points:
			draw_point(point,tick,pI)
			pI+=1;

		pygame.display.flip()
		glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
		clock.tick(FPS)
		#pygame.time.wait(5)

print()
print("###############################################################")
print("####                  MapPointer generator                #####")
print()
print(" [ WASD   ] - Передвижение")
print(" [ EQ     ] - Вверх вниз")
print(" [ SHIFT  ] - Ускорить движение")
print(" [ ARROWS ] - Вращение камеры")
print(" [ 1      ] - Снять все выделения")
print(" [ 2      ] - Проложить маршрут между 2 точками")
print(" [Левая кл. мыши ] - Выделение вершины перед камерой")
print(" [Правая кл. мыши] -  Вкл./Выкл. вращение камеры")
print("  [  Z    ] - Закрыть программу")
print()
print("###############################################################")
print()

main()