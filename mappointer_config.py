import numpy as np
import random

##### DRAW CONFIG ##################################################################

POINT_TYPES = {                             # Настройка вершин
    "simple_point": {                       
        "point_size": 0.1,                  # Размер
        "point_col": (0.0, 0.9, 1.0),       # Цвет
    },
    "selected": {                      
        "point_size": 0.12,                  
        "point_col": (0.8, 1.0, 0.6),       
    },
}
LINK_TYPES = {                              # Настройка связей
    "simple_link": {
        "line_col": (0.2, 0.2, 0.2),        # Цвет
        "lines_count": 1,                   # Кол-во линий
        "lines_spread": 0,                  # Ширина линий (если кол-во больше 1)
    },
    "selected_link": {
        "line_col": (0.7, 0.9, 0.5),       
        "lines_count": 2,               
        "lines_spread": 0.01,               
    }
}

BACK_COL = (0.02, 0.0, 0.05)        # Фоновый цвет
DISPLAY_SIZE = (1400,1000)          # Размер окна
GLARE_DRAW = True                   # Блики вершин
GLARE_SPEED = 0.002                 # Скорость бликов
GLARE_POWER = 0.45                  # Интенсивность блика

ARROWS_SENSITIVITY = 1              # Чуствительность поворота камеры
MOUSE_SENSITIVITY = 0.13            # Чуствительность поворота камеры мышью

MOV_SPEED_BOOSTED = 0.35            # Скорость быстрого перемещния
MOV_SPEED_BASE = 0.08               # Скорость перемещая по умолчанию

MOUSE_RETURN_DISTANCE = 200         # Дистанция свободы курсора при захвате мыши

CAM_START_POS = [5.5,8.0,-10.0]     # Стартовая позиция камеры
CAM_START_YAW = 30                  # Стартовый поворот камеры по горизонтали
CAM_START_PITCH = 40                # Стартовый поворот камеры по вертикали

FPS = 90                            # Предельная частота кадров


##### GEN CONFIG #######################################################################

points_args = {
    "radius":20,
    "chaos_strength":2,
    "height": 2,
    "safe_dist": 0.5,
    "num_points": 500,
}



links_args = {
    "link_distance_threshold": 1.5,
    "link_max": 4,
    "link_min": 1,
    "link_delete_chance": 0.5,
    "subgraphs_links": 1,
}

##### SEED ##################################################################

seed = "123"
useSeed = False
# useSeed = True