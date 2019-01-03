# coding: utf8

import numpy as np

class ImplicitSurface(object):
    def __init__(self):
        pass

    def potential_evaluator(self):
        def potential(x,y,z):
            points = np.transpose(np.array([x,y,z]),range(1,np.array(x).ndim+1)+[0])
            return np.zeros_like(points[...,0])
        return potential

    def surface_mesh(self, grid_size=128, grid_resolution=1, potential_value=0.5):
        from skimage.measure import marching_cubes_lewiner

        grid_limit = grid_size*grid_resolution/2
        x,y,z = np.mgrid[-grid_limit:grid_limit:grid_resolution,-grid_limit:grid_limit:grid_resolution,-grid_limit:grid_limit:grid_resolution]

        potential_field = self.potential_evaluator()(x,y,z)
        surface_points, surface_triangles, tangents, values = marching_cubes_lewiner(potential_field,potential_value)
        surface_points = np.array(surface_points)*grid_resolution - grid_limit
        surface_points = np.array(surface_points,dtype=np.float64)
        return surface_points, surface_triangles

    def pgl_surface_mesh(self, grid_size=128, grid_resolution=1, potential_value=0.5, color=[190,205,205], transparency=0):
        points, triangles = self.surface_mesh(grid_size, grid_resolution, potential_value)
        import openalea.plantgl.all as pgl
        if color is None:
            color = [np.random.randint(0,255) for i in xrange(3)] 
        mat = pgl.Material(tuple(color), diffuse=0.25, transparency=transparency)
        s = pgl.Scene()
        s += pgl.Shape(pgl.FaceSet(pgl.Point3Array(points), pgl.Index3Array([[int(i) for i in tr] for tr in triangles])), mat)
        return s

    def pgl_display(self, grid_size=128, grid_resolution=1, potential_value=0.5, color=[190,205,205], transparency=0, add = False):
        import openalea.plantgl.all as pgl
        s = self.pgl_surface_mesh(grid_size, grid_resolution, potential_value, color, transparency)
        if add : 
            pgl.Viewer.add(s)
        else : 
            pgl.Viewer.display(s)

    def mpl_display(self, grid_size=128, grid_resolution=1, potential_value=0.5, color=[190,205,205], transparency=0):
        import  matplotlib.pyplot as plt
        from mpl_toolkits.mplot3d import Axes3D
        from mpl_toolkits.mplot3d.art3d import Poly3DCollection
        points, triangles = self.surface_mesh(grid_size, grid_resolution, potential_value)

        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')

        poly = Poly3DCollection( points[triangles] )
        poly.set_facecolors([color[0]/255.,color[1]/255.,color[2]/255.,1-transparency])
        poly.set_edgecolor('k')
        ax.add_collection3d(poly)
        vmin = min([min(points[:,i]) for i in xrange(3)])
        vmax = min([max(points[:,i]) for i in xrange(3)])
        ax.set_xlim(vmin, vmax)
        ax.set_ylim(vmin, vmax)
        ax.set_zlim(vmin, vmax)

        plt.tight_layout()

        plt.show()

    def display(self, grid_size=128, grid_resolution=1, potential_value=0.5, color=[190,205,205], transparency=0):
        try:
            import openalea.plantgl.all as pgl
            self.pgl_display( grid_size, grid_resolution, potential_value, color, transparency)
        except ImportError:
            self.mpl_display( grid_size, grid_resolution, potential_value, color, transparency)
            


#fonction de melange par simple somme : transition douce
class AdditionalBlendingImplicitSurface(ImplicitSurface):

    def __init__(self, surfaces=[]):
        super(ImplicitSurface, self).__init__()
        self.surfaces = surfaces #collection de surfaces implicites

    def add(self, surface):
        self.surfaces.append(surface)

    def potential_evaluator(self):
        def potential(x, y, z):
            p = 0
            for surface in self.surfaces:
                p += surface.potential_evaluator()(x, y, z)
            return p
        return potential

#fonction de melange en gardant le maximum : transition franche
class MaximumBlendingImplicitSurface(ImplicitSurface):
    def __init__(self, surfaces=[]):
        super(ImplicitSurface, self).__init__()
        self.surfaces = surfaces

    def add(self, surface):
        self.surfaces.append(surface)

    def potential_evaluator(self):
        def potential(x, y, z):
            p = self.surfaces[0].potential_evaluator()(x, y, z)
            for surface in self.surfaces[1:]:
                potential_3D = surface.potential_evaluator()(x, y, z)
                p = np.maximum(p, potential_3D)
            return p
        return potential

#fonction de melange en gardant le maximum : transition franche
class MinimumBlendingImplicitSurface(ImplicitSurface):
    def __init__(self, surfaces=[]):
        super(ImplicitSurface, self).__init__()
        self.surfaces = surfaces

    def add(self, surface):
        self.surfaces.append(surface)

    def potential_evaluator(self):
        def potential(x, y, z):
            p = self.surfaces[0].potential_evaluator()(x, y, z)
            for surface in self.surfaces[1:]:
                potential_3D = surface.potential_evaluator()(x, y, z)
                p = np.minimum(p, potential_3D)
            return p
        return potential