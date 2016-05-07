import numpy
import random
import numpy as np
from math import *
from time import sleep

import matplotlib.pyplot as plt
import matplotlib
from matplotlib.patches import Polygon
from matplotlib.collections import PatchCollection

MAX_VERTICES_DEFAULT = 8

random.seed(1)

class Polygon(object):

    def __init__(self, vertices):
        self.ori_vertices = vertices
        self.vertices = []
        for each in vertices:
            self.vertices.append(Point(each))

    def whether_intersect(self, line):
        nr_v = len(self.vertices)
        flag = False
        for i in xrange(nr_v):
            if i == nr_v - 1:
                if line.whether_intersect(Line(self.vertices[i], self.vertices[0])):
                    flag = True
                    break
            else:
                if line.whether_intersect(Line( (self.vertices[i], self.vertices[i+1]))):
                    flag = True
                    break
        return flag

class Line(object):

    def __init__(self, points):
        assert len(points) == 2
        self.points = points

    def ccw(A,B,C):
        return (C.y-A.y)*(B.x-A.x) > (B.y-A.y)*(C.x-A.x)

    def whether_intersect(self, line):
        A = self.points[0]
        B = self.points[1]
        C = line.points[0]
        D = line.points[1]
        return ccw(A,C,D) != ccw(B,C,D) and ccw(A,B,C) != ccw(A,B,D)

class Point(object):

    def __init__(self, xy, parent=None):
        self.x = xy[0]
        self.y = xy[1]
        self.prob_successor_and_distances = []
        self.parent = parent
        self.index = -1
        self.g = -1
        self.h = -1
        self.f = -1

    def dist(self, point):
        return sqrt( (self.x-point.x)**2 + (self.y-point.y)**2 )

    def add_successor(self, point):
        self.prob_successor_and_distances.append((point,
                                                self.dist(point)))

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
        return Polygon(points_left)
    else:
        return None

def whether_in(polygon, point):
    l = len(polygon.vertices)
    point = (point.x, point.y)
    if point in convex_hull(polygon.ori_vertices+[point]):
        return False
    else:
        return True

def whether_intersect(polygon1, polygon2):
    flag = False
    for each in polygon2.vertices:
        if whether_in(polygon1, each):
            flag = True
            break
    for each in polygon1.vertices:
        if whether_in(polygon2, each):
            flag = True
            if flag:
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
    index = 0
    for part in parts:
        index += 1
        part0 = sorted(part[0])
        part1 = sorted(part[1])
        part = [(part0[0], part1[0]),
                (part0[1], part1[1])]
        new_polygon = generate_a_polygon(max_vertices, part)
        if not new_polygon:
            continue
        flag = False
        for each in polygons:
            if whether_intersect(each, new_polygon):
                flag = True
                print 'intersect'
                break
        if flag:
            continue
        polygons.append(new_polygon)
    return polygons

def add_polygon_to_plot(polygon):
    xs = [each[0] for each in polygon.ori_vertices]
    xs = xs + [xs[0]]
    ys = [each[1] for each in polygon.ori_vertices]
    ys = ys + [ys[0]]
    plt.plot(xs, ys)


if __name__ == "__main__":
    polygons = generate_polygons(100, 20, ((0,0), (3,4)))
    for each in polygons:
        add_polygon_to_plot(each)
    plt.show()
