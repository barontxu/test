import numpy
import random
import numpy as np
from math import *
from time import sleep

import matplotlib.pyplot as plt

from base import Shape
MAX_VERTICES_DEFAULT = 8

random.seed(1)

class Polygon(Shape):

    def __init__(self, vertices):
        '''
            vertices are list of Point
        '''
        self.ori_vertices = vertices
        self.vertices = []
        for each in vertices:
            self.vertices.append(Point(each))
        self.edges = []
        l = len(vertices)
        for i in xrange(l):
            self.edges.append(Line([self.vertices[i],
                                   self.vertices[i+1 if i+1 < l else 0]]))

    def whether_intersect_polygon(self, polygon):
        '''
            judge whether intersect with polygon
        '''
        flag = False
        for each in polygon2.edges:
            if polygon1.whether_intersect_line(each):
                flag = True
                break
        for each in polygon1.edges:
            if polygon2.whether_intersect_line(each):
                flag = True
                if flag:
                    break
        return flag

    def whether_intersect_line(self, line):
        '''
            judge whether intersect with line
        '''
        nr_v = len(self.vertices)
        flag = False
        for i in xrange(nr_v):
            if line.whether_intersect(Line((self.vertices[i],
                                            self.vertices[i+1 if i+1 < nr_v else 0]))):
                flag = True
                break
        return flag

    def whether_in(self, point):
        l = len(polygon.vertices)
        point = (point.x, point.y)
        if point in convex_hull(polygon.ori_vertices+[point]):
            return False
        else:
            return True


class Line(Shape):

    def __init__(self, points):
        assert len(points) == 2
        assert isinstance(points[0], Point)
        self.points = points

    def ccw(A,B,C):
        return (C.y-A.y)*(B.x-A.x) > (B.y-A.y)*(C.x-A.x)

    def whether_intersect(self, line):
        A = self.points[0]
        B = self.points[1]
        C = line.points[0]
        D = line.points[1]
        return ccw(A,C,D) != ccw(B,C,D) and ccw(A,B,C) != ccw(A,B,D)


class Point(Shape):
    '''
        not only a geometry shape but also contains info such as f g h
    '''

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


'''
    below is the part produce Polygons
'''
def cross(o, a, b):
    '''
        cross product of a-o, b-o
    '''
    return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])

def convex_hull(points):
    """
        compute convex hull of points
    """
    assert len(points) >= 3
    points = sorted(set(points))

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
        pos_range is a list contain two points that define a box the polygon should be in
    '''
    ru = random.uniform
    pr0 = pos_range[0]
    pr1 = pos_range[1]
    points = [ (ru( pr0[0], pr1[0] ), ru( pr0[1], pr1[1] )) for _ in xrange(max_vertices)]
    points_left = convex_hull(points)
    if len(points_left) >= 3:
        return Polygon(points_left)
    else:
        return None

def generate_polygons(max_nr_polygon, max_vertices, pos_range):
    '''
        generate polygons, pos_range is two points as above
    '''
    ru = random.uniform
    prx = (pos_range[0][0], pos_range[1][0])
    pry = (pos_range[0][1], pos_range[1][1])
    parts = [( (ru(*prx), ru(*prx)), (ru(*pry), ru(*pry)) ) for _ in xrange(max_nr_polygon)]
    polygons = []
    for part in parts:
        part0 = sorted(part[0])
        part1 = sorted(part[1])
        part = [(part0[0], part1[0]),
                (part0[1], part1[1])]
        new_polygon = generate_a_polygon(max_vertices, part)
        if not new_polygon:
            continue
        flag = False
        for each in polygons:
            if each.whether_intersect_polygon(new_polygon):
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


