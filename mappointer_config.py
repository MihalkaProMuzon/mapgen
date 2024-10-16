import numpy as np
import random

##### DRAW CONFIG ##################################################################
# !В дров кафинг... в кофе... тьфу мля! В настройке крч тока нечеткую цифру можнэ

POINT_TYPES = {                             # Настрой точке
    "simple_point": {                       
        "point_size": 0.04,                 # Большивность точке
        "point_col": (0.0, 0.9, 1.0),       # Крассость точке       
    },
    "selected": {                      
        "point_size": 0.12,                  
        "point_col": (0.8, 1.0, 0.6),       
    },
}
LINK_TYPES = {                              # Настрой палке
    "simple_link": {
        "line_col": (0.2, 0.2, 0.2),        # Крассость палке
        "lines_count": 1,                   # Многость палок (1 - палка без понтов этих фраерских)
        "lines_spread": 0,                  # Наскока размотало палки
    },
    "selected_link": {
        "line_col": (0.7, 0.9, 0.5),       
        "lines_count": 2,               
        "lines_spread": 0.01,               
    }
}

BACK_COL = (0.02, 0.0, 0.05)        # Петушиность задника
DISPLAY_SIZE = (1400,1000)          # Намалевано
GLARE_DRAW = True                   # Вырви моргала
GLARE_SPEED = 0.002                 # Быстро моргать
GLARE_POWER = 0.45                  # Сильно моргнуть

ARROWS_SENSITIVITY = 1              # С какой силой смотреть
MOUSE_SENSITIVITY = 0.13            # Как мощьно вглядываться

MOV_SPEED_BOOSTED = 0.35            # Двигать быстро
MOV_SPEED_BASE = 0.08               # Двигать пойдет

MOUSE_RETURN_DISTANCE = 200         # Вот мышью водишь, она шоб в край экрана не въебаться 
                                    # переодически возвращается вот вот это крч

CAM_START_POS = [5.5,8.0,-10.0]     # Где камера начинает ваще
CAM_START_YAW = 30                  # Как камера начинает горизонально
CAM_START_PITCH = 40                # Этоооо... забыл... крч чета вертикально

FPS = 90                            # Шакальность всратости


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