import numpy as np
import random
from queue import Queue

from mappointer_helper import *
from mappointer_config import *

########################################################################################
if useSeed:
    random.seed(a=seed, version=2)
########################################################################################




def deb_gen(args):
    _num_points = args["num_points"] or 100
    points = []
    for i in range(int(np.sqrt(_num_points))):
        for j in range(int(np.sqrt(_num_points))):
            point = {
                "pos": (i,0,j),
                "type": "simple_point"
            }
            points.append(point)
    return points


def randgen1(args):
    _num_points = args["num_points"] or 100
    points = []
    for i in range(_num_points):
        point = {
            "pos": (random.uniform(-10, 10), random.uniform(-10, 10), random.uniform(-10, 10)),
            "type": "simple_point"
        }
        rand_chance = random.randint(0,100)
        if rand_chance < 3:
            point["type"] = "point2"

        points.append(point)

    return points


def sphere_points_gen(args):
    print("")
    # # # # # #
    _num_points = args["num_points"] or 100
    _radius = args["radius"] or 100
    _chaos_strength = args["chaos_strength"] or 1
    _height = args["height"] or _radius
    _safe_dist = args["safe_dist"] or 0.1
    # # # # # #

    points = []
    gen_i = 0
    while(gen_i < _num_points):
        print_rewrite(f"{bcolors.OKCYAN} -> Вершины {gen_i} / {_num_points}")
        # Генерация случайных углов
        theta = 2 * np.pi * np.random.rand()
        phi = np.arccos(2 * np.random.rand() - 1)

        r = np.random.rand() ** (1 / _chaos_strength)  # Модификация радиуса

        # Конвертация сферических координат в декартовы
        x = r * np.sin(phi) * np.cos(theta) *_radius
        y = r * np.sin(phi) * np.sin(theta) *_height
        z = r * np.cos(phi)                 *_radius

        newpoint = {
            "pos": (x,y,z),
            "type": "simple_point"
        }


        #Проверка на мин раст до других точек
        min_dist_fail = False
        for point in points:
            if points_dist(newpoint, point) < _safe_dist:
                min_dist_fail = True
                break

        if min_dist_fail:
            continue

        points.append(newpoint)
        gen_i+=1

    print_rewrite(f"{bcolors.OKGREEN} • Вершины {_num_points} / {_num_points}")
    print(f"{bcolors.OKGREEN} • Вершины созданы")
    return points


########################################################################################
def generate_points(args):
    print(f"\n{bcolors.HEADER}Генерация вершин:")
    # return deb_gen(args)
    # return randgen1(args)
    return sphere_points_gen(args)
########################################################################################
    

# !!! Теперь соединенин у точки - словарь, с расстояниями (а не просто массив индексов)!

def gen_links1(points, args):
    # # # # # #
    _link_distance_threshold = args["link_distance_threshold"] or 1.0
    _link_max = args["link_max"] or 5.0
    _link_min = args["link_max"] or 1
    _link_delete_chance = args["link_delete_chance"] or 0.5
    _subgraphs_links = args["subgraphs_links"] or 1
    # # # # # #

    pointsCnt = len(points)

    # Инициализация связей
    print(" Инициализация связей")
    links = {}
    for i, point_a in enumerate(points):
        links[i] = { 
            "link_points": {}, 
            "type": "simple_link",
            "disctances": {},
        }
    print_rewrite(f"{bcolors.OKGREEN} • Инициализация связей")

    # Соеденить по distance threshold
    print(" Соединие по расстоянию")
    for i, point_a in enumerate(points):
        print_rewrite(f"{bcolors.OKCYAN} -> Соединие по расстоянию {i} / {pointsCnt}")
        lnk = links[i]
        for j, point_b in enumerate(points):
            if i != j:
                lnk2 = links[j]

                dst = points_dist(point_a, point_b)

                if not j in lnk["disctances"]:
                    lnk["disctances"][j] = dst
                    lnk2["disctances"][i] = dst

                if dst < _link_distance_threshold:
                    if not j in lnk["link_points"]:
                        lnk["link_points"][j] = dst
                        lnk2["link_points"][i] = dst
    print_rewrite(f"{bcolors.OKGREEN} • Соединие по расстоянию {pointsCnt} / {pointsCnt}")

    # Удалить по [min <-> max] и delete chance
    print(" Вероятностное удаление")
    for lnk_i, point_a in enumerate(points):
        print_rewrite(f"{bcolors.OKCYAN} -> Вероятностное удаление {lnk_i} / {pointsCnt}")
        lnk = links[lnk_i]
        lnk_links_cnt = len(lnk["link_points"])
        if lnk_links_cnt > _link_min:
    
            to_delete = []
            for lnk_nbr_i, _ in lnk["link_points"].items():
                
                lnk_links_cnt = len(lnk["link_points"])
                if lnk_links_cnt <= _link_min:
                    break

                chance = _link_delete_chance
                if lnk_links_cnt > _link_max:
                    chance = 1.0

                if throw_with_сhance(chance):
                    to_delete.append(lnk_nbr_i)

            for delete_index in to_delete:
                del lnk["link_points"][delete_index]
                del links[delete_index]["link_points"][lnk_i]

    print_rewrite(f"{bcolors.OKGREEN} • Вероятностное удаление {pointsCnt} / {pointsCnt}")

    # Собрать подграфы
    print(" Поиск подграфов")
    all_subgraphs = {}
    point_subgraphs = {}
    visited = set()
    subgraph_index = 0
    for lnk_i, _ in enumerate(points):
        if lnk_i in visited:
            continue

        subgraph = []
        bypass = Queue()
        bypass.put(lnk_i)

        while(True):
            if bypass.empty():
                break

            index = bypass.get()
            if index in visited:
                continue

            visited.add(index)
            subgraph.append(index)
            point_subgraphs[index] = subgraph_index

            for nbr in links[index]["link_points"]:
                bypass.put(nbr)
            
        all_subgraphs[subgraph_index] = subgraph
        # print(f"{subgraph_index}-{subgraph}")
        subgraph_index += 1
        print_rewrite(f"{bcolors.OKCYAN} -> Поиск подграфов: {subgraph_index}")

    print_rewrite(f"{bcolors.OKGREEN} • Поиск подграфов: {subgraph_index}")


    # Проложить связь между сабграфами
    print(" Соединение подграфов")
    while(True):
        subg_count = len(all_subgraphs.items())
        print_rewrite(f"{bcolors.OKCYAN} -> Соединение подграфов, осталось: {subg_count}")
        if subg_count < 2:
            break

        # Берем кратчайший подграф, для сокращение поиска расстояний
        shortest_subg_i = 0
        shortest_len = 200000
        for subg_i, subg in all_subgraphs.items():
            dlena_subg = len(subg)
            if dlena_subg < shortest_len:
                shortest_len = dlena_subg
                shortest_subg_i = subg_i
            

        subg_i = shortest_subg_i
        subg = all_subgraphs[subg_i]

        # Поиск среди точек подграфа, близжайшей точки не относящейся к нему
        mindst_in_subg = 1000000000
        colesest_to_subg = 0
        closest_in_subg = 0

        for point_i in subg:
            lnk = links[point_i]
            lnk_cnt = len( lnk["link_points"] )
            if lnk_cnt > (_link_max-1):
                continue

            for point2_i, dst in lnk["disctances"].items():
                if point2_i in subg:
                    continue
                
                finded_point_links_cnt = len( links[point2_i]["link_points"] )
                if finded_point_links_cnt >= (_link_max-1):
                    continue

                if (dst < mindst_in_subg):
                    mindst_in_subg = dst
                    colesest_to_subg = point2_i
                    closest_in_subg = point_i

        # Соденить с найденным сабграфом
        links[closest_in_subg]["link_points"][colesest_to_subg] = True
        links[colesest_to_subg]["link_points"][closest_in_subg] = True

        finded_subg_index = point_subgraphs[colesest_to_subg]
        
        subg.extend( all_subgraphs[finded_subg_index] )
        for point_i in all_subgraphs[finded_subg_index]:
            point_subgraphs[point_i] = subg_i

        del all_subgraphs[finded_subg_index]

    print_rewrite(f"{bcolors.OKGREEN} • Подграфы соеденены")

    print(f"{bcolors.OKGREEN} • Связи созданы")

    return links

########################################################################################
def create_links(points, args):
    print(f"\n{bcolors.HEADER}Генерация связей:")
    return gen_links1(points, args)
########################################################################################





def test(points, links):
    print(f"\n{bcolors.HEADER}Тестирование:"+bcolors.OKCYAN)

    # Проверка на соеденения
    visited = set()
    bypass = Queue()
    bypass.put(0)

    while(True):
        if bypass.empty():
            break

        index = bypass.get()
        if index in visited:
            continue

        visited.add(index)
        for nbr in links[index]["link_points"]:
            bypass.put(nbr)

    result = len(visited) == len(points)
    if result:
        print(" – Граф связанный")
    else:
        print(" – Размокнутый граф")


    # Мин и макс кол-во связей
    min_links = 10000
    max_links = 0

    for lnk_i, lnk in links.items():
        lnk_count = len(lnk["link_points"])
        if lnk_count > max_links:
            max_links = lnk_count
        if lnk_count < min_links:
            min_links = lnk_count

    print(f" – Минимальное кол-во связей: {min_links}")
    print(f" – Максимальное кол-во связей: {max_links}")
    print(bcolors.RESET)