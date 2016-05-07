import numpy
import random
import numpy as np

import matplotlib.pyplot as plt
import matplotlib
from matplotlib.patches import Polygon
from matplotlib.collections import PatchCollection

MAX_VERTICES_DEFAULT = 8

def convex_hull(points):
    """
        compute convex hull of points
    """
    assert len(points) >= 3
    points = sorted(set(points))

    #cross product
    def cross(o, a, b):
        return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])

    lower = []
    for p in points:
        while len(lower) >= 2 and cross(lower[-2], lower[-1], p) <= 0:
            lower.pop()
        lower.append(p)

    upper = []
    for p in reversed(points):
        while len(upper) >= 2 and cross(upper[-2], upper[-1], p) <= 0:
            upper.pop()
        upper.append(p)

    return lower[:-1] + upper[:-1]

def generate_a_polygon(max_vertices, pos_range):
    '''
        pos_range is a list contain two pointsthat define a box polygon should be in
    '''
    points = [(random.uniform(pos_range[0][0], pos_range[1][0]),
                   random.uniform(pos_range[0][1], pos_range[1][1])) \
                   for _ in xrange(max_vertices)]
    points_left = convex_hull(points)
    if len(points_left) >= 3:
        return points_left
    else:
        return []

def whether_in(polygon, point):
    l = len(polygon)
    if l == len(convex_hull(polygon+[point])):
        return True
    else:
        return False

def whether_intersect(polygon1, polygon2):
    flag = False
    for each in polygon2:
        if whether_in(polygon1, each):
            flag = True
            break
    return flag

def generate_polygons(max_nr_polygon, max_vertices, pos_range):
    '''
     generate polygons
    '''
    ru = random.uniform
    parts = [((ru(pos_range[0][0], pos_range[1][0]),
              ru(pos_range[0][0], pos_range[1][0])),
              (ru(pos_range[0][0], pos_range[1][0]),
              ru(pos_range[0][0], pos_range[1][0]))) \
                 for _ in xrange(max_nr_polygon)]
    polygons = []
    for part in parts:
        part0 = sorted(part[0])
        part1 = sorted(part[1])
        part = [(part0[0], part1[0]),
                (part0[1], part1[1])]
        new_polygon = generate_a_polygon(max_vertices, part)
        flag = False
        for each in polygons:
            if whether_intersect(each, new_polygon):
                flag = True
                break
        if flag:
            continue
        polygons.append(new_polygon)
    return polygons

def add_polygon_to_plot(polygon):
    xs = [each[0] for each in polygon]
    xs = xs + [xs[0]]
    ys = [each[1] for each in polygon]
    ys = ys + [ys[0]]
    plt.plot(xs, ys)


if __name__ == "__main__":
    polygons = generate_polygons(100, 10, ((1,2), (3,4)))
    for each in polygons:
        add_polygon_to_plot(each)
    plt.show()
