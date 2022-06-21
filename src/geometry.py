from Geometry3D import Point, ConvexPolygon, intersection, Segment
from common import X, Y, Z
from numpy import cross 
from math import atan, pi

class Geometry: 

    """
        Load the mesh and convert it into a geometry
    """
    def __init__(self, mesh):

        self.mesh = mesh 

        self.polygons = []
        
        self._calculate_size()

        for t in self.mesh.vectors:
            try:
                self.polygons.append(
                    self._polygon_from_three_points((
                        self._point_from_array(t[X]),
                        self._point_from_array(t[Y]),
                        self._point_from_array(t[Z])
                    ))
                    )
            except ZeroDivisionError:
                pass


    def _point_from_array(self, point_array):
        return Point(*point_array.astype('float'))

    def _polygon_from_three_points(self, points):
        return ConvexPolygon(points)


    """
        Get the 2 extreme vertices of the object
    """
    def _calculate_size(self):
        self.size = {'min': [1000000000,1000000000,1000000000], 'max': [0,0,0], 'abs': [0,0,0] }

        for pol in self.mesh.vectors:
            for point_array in pol:
                for i in (X, Y, Z):
                    if point_array[i] < self.size['min'][i]:
                        self.size['min'][i] = point_array[i]

                    if point_array[i] > self.size['max'][i]:
                        self.size['max'][i] = point_array[i]

        for i in (X, Y, Z):
            self.size['abs'][i] = abs(self.size['max'][i] - self.size['min'][i])
            

 



class Slice:
    
    def _tool_angle(self, polygon):
        c = cross((list(polygon.points[0]), list(polygon.points[1])) , (list(polygon.points[0]), list(polygon.points[2])))
        #p0 = Point(c[0])
        p1 = Point (c[1])
        #print(c)
        A = atan(c[1][Y]/c[1][Z]) * (180/pi)
        B = atan(c[1][X]/c[1][Z]) * (180/pi)
        C = atan(c[1][X]/c[1][Y]) * (180/pi)

        return A, B, C
        """
        try:
            self.cross.append(
                Segment(p0, p1)
            )
        except ValueError:
            pass
        """

    def __init__(self, geometry, z):

        self.z = z 
        self.geometry = geometry 

        # Create the slicing plane 
        self.plane = ConvexPolygon((
            Point(self.geometry.size['min'][X], self.geometry.size['min'][Y], self.z),
            Point(self.geometry.size['max'][X], self.geometry.size['max'][Y], self.z),
            Point(self.geometry.size['max'][X], self.geometry.size['min'][Y], self.z),
            Point(self.geometry.size['min'][X], self.geometry.size['max'][Y], self.z),
        ))

        #Array of intercepting polygon 
        self.intercept = []

        for polygon in self.geometry.polygons:
            i = intersection(self.plane, polygon)
            if i is not None:




                self.intercept.append({'segment': i, 'angle': self._tool_angle(polygon)})

                
        
        #print(self.cross)