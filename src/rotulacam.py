
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

import sys 


PLOT_WIDTH = 80 #mm
PLOT_HEIGHT = 100 #mm

HEAD_SIZE = 2 #mm 

SAFE_HEIGHT = 3 
SPEED = 1000 

def rgb_to_grayscale(img):

    arr_x = []
    for x in img:
        arr_y = []
        for y in x:
            arr_y.append(int(sum(y)/3))
        arr_x.append(arr_y)
    return arr_x 

def rgb_to_bw(img, trigger):

    grayscale = rgb_to_grayscale(img)

    arr_x = []
    for x in grayscale:
        arr_y = []
        for y in x:
            if y > trigger:
                arr_y.append(254)
            else:
                arr_y.append(0)
        arr_x.append(arr_y)
    return arr_x 

def imagesize(img):
    return (len(img[0]), len(img)) 

def scale(img, new_x, new_y):

    orig_x, orig_y = imagesize(img)

    scalefactor_x = new_x / orig_x 
    scalefactor_y = new_y / orig_y

    arr_y = []
    for y in range(new_y):
        arr_x = []
        for x in range(new_x):
            
            interpol_x = round(x / scalefactor_x)
            if interpol_x >= orig_x:
                interpol_x = orig_x -1
            interpol_y = round(y / scalefactor_y)
            if interpol_y >= orig_y:
                interpol_y = orig_y -1

            #print(x, y, scalefactor_x, scalefactor_y, interpol_x, interpol_y, orig_x, orig_y)
            arr_x.append(img[interpol_y][interpol_x])

        arr_y.append(arr_x)
    return arr_y

def path_gen(x_size, y_size):
    path = []

    dir = False
    for x in range(x_size):

        if dir:
            for y in range(y_size):
                path.append((x,y))
             
        else:
            for y in range(y_size-1, -1, -1):
                path.append((x,y))
        dir = not dir

    return path  

def gcode(img):

    f = open('out.gcode', 'w')

    f.write('G0 G90 G40 G21 G17 G94 G80\n')
    f.write("G0Z%s\n" % (SAFE_HEIGHT))

    x_size, y_size = imagesize(img)

    #Generate the path
    path = path_gen(x_size, y_size)

    for p in path:
        x, y = p
        if img[y][x] < 128:
            f.write("G0 X%s Y%s \n" % (x, y))
            f.write("G1 Z0 F%s\n" % (SPEED))
        else: 
            f.write("G0Z%s\n" % (SAFE_HEIGHT))
            f.write("G0 X%s Y%s Z%s\n" % (x, y, SAFE_HEIGHT))

    #for y in range(y_size):
    #    for x in range(x_size-1, 0, -1):
    #        if img[y][x] < 128:
    #            f.write("G0 X%s Y%s Z%s\n" % (x, y, SAFE_HEIGHT))
    #            f.write("G1 Z0 F%s\n" % (SPEED))
    #            f.write("G0Z%s\n" % (SAFE_HEIGHT))


    f.write('M30\n')
    f.close()
if __name__ == "__main__":
     
    #Load the image
    img = mpimg.imread('../gioconda.jpg')

    img_width, img_height = imagesize(img)

    print(img_width, img_height)

    #print(img)
    #Plot the image 
    #imgplot = plt.imshow(rgb_to_bw(img, 58))
    pixels_width = int(PLOT_WIDTH/HEAD_SIZE)
    pixels_heigth = int(PLOT_HEIGHT/HEAD_SIZE)

    limg = scale(rgb_to_bw(img, 58), pixels_width, pixels_heigth)
    imgplot = plt.imshow(limg)

    gcode(limg)
    plt.show()