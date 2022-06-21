from stl import mesh
from Geometry3D import Renderer
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
        
        for z in range(1, slice_number):
            levels.append(round((height/slice_number) * z, 1))

        self.slices = []

        for z in levels:
            self.slices.append(Slice(self.geometry, z))


    def gcode(self):
        f = open('out.gcode', 'w')

        f.write('G0 G90 G40 G21 G17 G94 G80\n')
        #f.write("G0Z%s\n" % (SAFE_HEIGHT))

        for slice in self.slices:
            for point in slice.points:
                p = point['point']
                f.write("G1 X%f Y%f Z%f B%f C%f\n F%f" % (p[X], p[Y], p[Z], point['angle'][Y], point['angle'][Z], parameters.TOOL_FEED))
                
        f.write('M30\n')
        f.close()

if __name__ == "__main__":

    #Init rotulacam
    cam = RotulaCAM()

    #Load the stl
    cam.load_stl('../Testobj.stl')

    #Slice the model 
    cam.slice()

    #Generate gcode
    cam.gcode()

    #Some rendering 
    r = Renderer()

    for polygon in cam.geometry.polygons:
        r.add((polygon,'r',1),normal_length = 0)

    for slice in cam.slices:
        for inter in slice.points:
            r.add((inter['point'],'b',2),normal_length = 0)
        

    #r.add((cam.plane,'b',1),normal_length = 0)
    r.show()
    #First, open the file 

