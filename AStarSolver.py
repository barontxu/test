'''
    General OpenSet and AStartSolver for inherit to any problem depends on A star
'''
import matplotlib.pyplot as plt

from base import OpenSetBase
from shape import generate_polygons, Polygon, Line, Point


class OpenSetList(OpenSetBase):

    def __init__(self):
        self.openset = []
        self.expanded = []

    def append(self, point):
        if point in self.expanded:
            return
        self.openset.append(point)
        sorted(self.openset, cmp=lambda x,y:cmp(x.f, y.f), reverse=True)

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
            node has g, f, h
        '''
        self.nodes = nodes
        self.openset = OpenSetList()
        self.start = nodes[0]
        self.end = nodes[-1]

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
        self.start.g = 0
        self.start.h = self.h_function(self.start)
        self.start.f = self.start.h
        self.openset.append(self.start)

        #start loop
        while True:
            p = self.openset.pop()
            for each in p.successor_and_costs:
                successor = each[0]
                cost = each[1]
                successor.g = p.g + cost
                successor.h = self.h_function(successor)
                successor.f = successor.g + successor.h
                self.openset.append(successor)
            if self.end_state:
                break


class AStarSolverPolygon(AStarSolver):

    def h_function(self, node):
        return self.node.dist(self.end)

    def end_state(self):
        if self.end == self.openset.top:
            return True
        return False


def prepare():
    pass


if __name__ == '__main__':
    prepare()
