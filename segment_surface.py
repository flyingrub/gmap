#!/usr/bin/python
# -*- coding: utf-8 -*-
import numpy as np
from numpy.linalg import norm

def mnorm(setofpoints):    
    # We supposed we have n-dimentional array of points and should return n-dimentional array of norm
    return norm(setofpoints, axis=len(setofpoints.shape)-1)

def mmultiply(setofvalues, dvector):
    # We supposed we have n-dimentional array of values to mulltiply to one vector
    return setofvalues[...,np.newaxis] * dvector

def segment_distance(start_point, end_point):
    length = norm(end_point-start_point)
    directional_vector = (end_point-start_point)/length
    
    def distance(points):
        point_vectors_start = points - start_point
        point_vectors_end = points - end_point
        start_distances = mnorm(point_vectors_start) # Distances of points to start_point 
        end_distances = mnorm(point_vectors_end) # Distances of points to end_point 
        distances = np.minimum(start_distances,end_distances)

        dot_products = np.dot(point_vectors_start, directional_vector)# point_vectors . directional_vector (use np.dot)
        projected_points = mmultiply(dot_products, directional_vector) + start_point # Coordinates of projections, using dot_products and mmultiply
        line_distances = mnorm(points - projected_points)# Distances of points to projected_points
        segment_points = np.where((0<dot_products) & (dot_products<length))
        distances[segment_points] = line_distances[segment_points]
        return distances

    return distance

from implicit_surface import ImplicitSurface

class SegmentImplicitSurface(ImplicitSurface):
    def __init__(self, start_point=[0,0,0], end_point=[0,0,1], radius = 1):
        super(ImplicitSurface, self).__init__()
        self.distance = segment_distance(np.array(start_point), np.array(end_point))
        self.radius = radius
        # Instantiate attributes of the class to store the center and 
        # necessary parameters (e.g. radius for Stolte).

    def potential_evaluator(self):
        def potential(x,y,z):
            points = np.transpose(np.array([x,y,z]),range(1,np.array(x).ndim+1)+[0])
            d = self.distance(points)
            pot = (1 / self.radius**8) * (d**2 - self.radius**2)**4
            return d-self.radius
        return potential
