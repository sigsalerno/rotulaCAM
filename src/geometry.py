from Geometry3D import Point, ConvexPolygon, intersection, Segment
from common import X, Y, Z
from numpy import cross, subtract, add, divide, linalg
from math import atan2, pi, asin
class Geometry: 

    """
        Load the mesh and convert it into a geometry
    """
    def __init__(self, mesh):

        self.mesh = mesh 

        self.polygons = []
        
        #Calculate the mesh global size
        self._calculate_size()

        #Import the vectors
        for t in self.mesh.vectors:
            try:
                self.polygons.append(
                    ConvexPolygon((
                        self._point_from_array(t[0]),
                        self._point_from_array(t[1]),
                        self._point_from_array(t[2])
                    ))
                    )
            except ZeroDivisionError:
                pass

    #Here we repositione the mesh in the center of the plane. This should not be automatic
    def _point_from_array(self, point_array):
        arr = [
            point_array.astype('float')[X] - self.size['center'][X],
            point_array.astype('float')[Y] - self.size['center'][Y],
            point_array.astype('float')[Z] 
        ]

        return Point(arr)


    """
        Get the 2 extreme vertices of the object, calculate the size
    """
    def _calculate_size(self):

        self.size = {'min': [1000000000,1000000000,1000000000], 'max': [0,0,0], 'abs': [0,0,0], 'center': [0,0,0] }

        for pol in self.mesh.vectors:
            for point_array in pol:
                for i in (X, Y, Z):
                    if point_array[i] < self.size['min'][i]:
                        self.size['min'][i] = point_array[i]

                    if point_array[i] > self.size['max'][i]:
                        self.size['max'][i] = point_array[i]

        for i in (X, Y, Z):
            self.size['abs'][i] = abs(self.size['max'][i] - self.size['min'][i])
            self.size['center'][i] = self.size['abs'][i]/2
            self.size['max'][i] = self.size['max'][i] - self.size['center'][i]
            self.size['min'][i] = self.size['min'][i] - self.size['center'][i]
            

 



class Slice:
    
    #Return everytime the same length (1), as we don't need the magnitude
    def _tool_vector(self, polygon):
        #Translate the first point as the origin 
        v1 = subtract(list(polygon.points[1]), list(polygon.points[0]))
        v2 = subtract(list(polygon.points[2]), list(polygon.points[0]))

        cv = cross(v1, v2)
        
        scv =  divide(cv, linalg.norm(cv))
        return scv

    #Calculate the perpendicular of the polygon, for the tool
    def _tool_angle(self, polygon):

        scv = self._tool_vector(polygon)

        A = asin(scv[X]) * (180/pi)
        B = asin(scv[Y]) * (180/pi)
        C = asin(scv[Z]) * (180/pi)
        
        return A, B, C
        

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
        self.points = []

        def genpoint(point, polygon):
            #The order will give the path to our adventurer
            #Is clockwise
            order = atan2(point[X], point[Y]) 

            return {
                'point': point, 
                'angle': self._tool_angle(polygon), 
                'order': order,
                'segment': Segment(point, Point(add(tuple(point), self._tool_vector(polygon))))
                }

        for polygon in self.geometry.polygons:
            i = intersection(self.plane, polygon)
            if i is not None:
                if type(i) == Segment:
                    self.points.append(genpoint(i.start_point, polygon))
                    self.points.append(genpoint(i.end_point, polygon))
                else:
                    self.points.append(genpoint(i, polygon))

        self.points.sort(key = lambda x: x['order'])

"""
        self.vectors = []

        for point in self.points:

            self.vectors.append(
                Segment(
                    Point(point['point']),
                    Point(add(
                        tuple(point['point']), 
                        (tan(point['angle'][X]), tan(point['angle'][Y]), tan(point['angle'][Z]))
                    ))
                )
            )
"""

        