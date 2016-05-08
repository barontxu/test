'''
    General OpenSet and AStartSolver for inherit to any problem depends on A star
'''
import matplotlib.pyplot as plt
import random

from base import OpenSetBase
from shape import generate_polygons, add_polygon_to_plot, Polygon, Line, Point

random.seed(3)

class OpenSetList(OpenSetBase):

    def __init__(self):
        self.openset = []
        self.expanded = []

    def append(self, point, g, h, f, parent):
        if point in self.expanded:
            return
        if not point in self.openset:
            point.g = g
            point.h = h
            point.f = f
            point.parent = parent
            self.openset.append(point)
        else:
            index = self.openset.index(point)
            point = self.openset[index]
            if point.g > g:
                point.parent = parent
                point.g = g
            point.h = h
            point.f = h + point.g
        self.openset = sorted(self.openset, cmp=lambda x,y:cmp(x.f, y.f), reverse=True)

    def pop(self):
        p = self.openset.pop()
        self.expanded.append(p)
        return p

    @property
    def top(self):
        return self.openset[-1]

class AStarSolver(object):

    def __init__(self, nodes):
        '''
            nodes contains start and end as the first and last one
            node has g, f, h, and knows its successor_and_costs
        '''
        self.nodes = nodes
        self.openset = OpenSetList()
        self.start = nodes[0]
        self.end = nodes[-1]
        self.logger = []

    def h_function(self, node):
        '''
            heuristic function
        '''
        pass

    def end_state(self):
        '''
            return a bool
        '''
        pass

    def start_search(self):
        g = self.start.g = 0
        h = self.start.h = self.h_function(self.start)
        f = self.start.f = self.start.h
        self.openset.append(self.start, g, f, h ,None)

        #start loop
        while True:
            p = self.openset.pop()
            #if abs(p.x - 2.33462939052) < 0.0001:
            #    from IPython import embed; embed()
            for each in p.successor_and_costs:
                successor = each[0]
                cost = each[1]
                g = p.g + cost
                h = self.h_function(successor)
                f = g + h
                self.openset.append(successor, g, h, f, p)
            if self.end_state:
                break
        s = self.end
        xs = []
        ys = []
        while s:
            xs.append(s.x)
            ys.append(s.y)
            s = s.parent
        plt.plot(xs, ys)
        return

class AStarSolverPolygon(AStarSolver):
    '''
        specify for polygon
    '''

    def h_function(self, node):
        return node.dist(self.end)

    @property
    def end_state(self):
        if self.end == self.openset.top:
            return True
        return False


def prepare(size, polygons_info, start, end):
    '''
        something neccesary such as construct the whole picture
    '''
    polygons = generate_polygons(*polygons_info)
    for each in polygons:
        add_polygon_to_plot(each)
    start = Point(start)
    end = Point(end)
    points = [start]
    for polygon in polygons:
        points += polygon.vertices
    points += [end]

    #get successor_and_costs for every points
    for i in xrange(len(points)-1):
        # -1 for end point does not need to get successor
        point_i = points[i]
        siblings = [point_i]
        belonging = check_belonging(point_i, polygons)
        if belonging[0]:
            for each in belonging[1]:
                point_i.add_successor(each)
            siblings = belonging[2].vertices
        for other_point in points:
            if other_point in siblings:
                continue
            flag = True
            for polygon in polygons:
                if polygon.whether_intersect_line(Line((point_i, other_point))):
                    flag = False
                    break
            if flag:
                point_i.add_successor(other_point)
    return points

def check_belonging(point, polygons):
    for polygon in polygons:
        if point in polygon.vertices:
            l = len(polygon.vertices)
            index = polygon.vertices.index(point)
            point1 = polygon.vertices[index-1]
            point2 = polygon.vertices[index+1 if index+1 < l else 0]
            return True, [point1, point2], polygon

    return False,


if __name__ == '__main__':
    polygons_info = (100, 10, ((0,0), (5,5)))
    points = prepare((5, 5), polygons_info, (0,0), (5,5))
    solver = AStarSolverPolygon(points)
    solver.start_search()
    plt.show()
