from matplotlib.patches import Polygon
import numpy
from stl import mesh
from Geometry3D import Point, ConvexPolygon, Renderer, Segment, intersection, xy_plane
from common import X, Y, Z
from geometry import Geometry, Slice
import parameters 

class RotulaCAM:

    """
        Load the STL and convert it into a geometry
    """
    def load_stl(self, filename):

        self.loaded_mesh = mesh.Mesh.from_file(filename)

        self.geometry = Geometry(self.loaded_mesh) 
      

    def slice(self):

        height = self.geometry.size['abs'][Z] 

        slice_number = round( height / parameters.TOOL_DIAMETER ) 

        levels = []
        print(height, slice_number)
        for z in range(1, slice_number):
            levels.append(round((height/slice_number) * z, 1))

        print(levels)
        self.slices = []

        for z in levels:
            self.slices.append(Slice(self.geometry, z))


    def gcode(self):
        f = open('out.gcode', 'w')

        f.write('G0 G90 G40 G21 G17 G94 G80\n')
        #f.write("G0Z%s\n" % (SAFE_HEIGHT))

        for slice in self.slices:
            for segment in slice.intercept:
                try:
                    print(dir(segment['segment']))
                    for p in segment['segment']:
                        f.write("G1 X%f Y%f Z%f B%f C%f\n" % (p[X], p[Y], p[Z], segment['angle'][Y], segment['angle'][Z]))
                except TypeError as e:
                    print("error")
                    print(e)
        f.write('M30\n')
        f.close()

if __name__ == "__main__":

    print("Start")

    cam = RotulaCAM()

    cam.load_stl('../Testobj.stl')
    cam.slice()
    #cam.interpolate()
    
    cam.gcode()

    print(cam.geometry.size)




    #Some rendering 
    r = Renderer()

    for polygon in cam.geometry.polygons:
        r.add((polygon,'r',1),normal_length = 0)

    for slice in cam.slices:
        for inter in slice.intercept:
            #print(inter)
            r.add((inter['segment'],'b',2),normal_length = 0)
        

    #r.add((cam.plane,'b',1),normal_length = 0)
    r.show()
    #First, open the file 

