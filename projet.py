#!/usr/bin/python
# -*- coding: utf-8 -*-
import segment_surface
segment_surface = reload(segment_surface)
from segment_surface import *

def question1():
    distance = segment_distance(np.array([0,0,0]), np.array([0,0,1]))
    dist = distance(np.array([[0,0,0],[0,0,0.5],[0,0,2],[0,1,0.5],[1,0,0.5]]))
    print dist
    assert norm(dist - [0,0,1,1,1] ) < 1e-5

def question2():
    SegmentImplicitSurface().display(50,0.1,0.1)

from skeleton import *
from math import *
 
def question3():
    s = Skeleton()
    s.add_segment((0,0,0),(0,0,1),0.4)
    s.add_segment((0,0,1),(0,-1,1+sqrt(3)),0.2)
    s.add_segment((0,0,1),(0,1,1+sqrt(3)),0.2)
    s.implicit_surface().display(100,0.1,0.2)


from gmap_tools import gmap_from_triangular_mesh

def gmapfromimplicit():
    print 'implicit surface to triangles'
    points, triangles = SegmentImplicitSurface().surface_mesh(50,0.2,0.1)
    print 'triangle to gmap'
    return gmap_from_triangular_mesh(points, triangles)

def question4():
    gmap = gmapfromimplicit()
    print 'display'
    gmap.dart_display(radius=0.02)


def question6():
    import gmap; reload(gmap)
    import basicshapes; reload(basicshapes)
    from basicshapes import cube
    gmap, darts = cube()
    gmap.remove_cell(0,1)
    gmap.dart_display()
    gmap.print_alphas()


if __name__ == '__main__':
    question6()
