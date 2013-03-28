#! /usr/bin/env python
import matplotlib
# Tell matplotlib to use Agg backend so that it does not need $DISPLAY
matplotlib.use('Agg')
import numpy
import pylab

def get_z_indx(z_cord, data_dir):
    z_file = open('out/z')
    z = [ float(i) for i in z_file.readlines() ]
    return z.index(z_cord)

def z_slice(z_cord=False, z_indx=False, data_dir):
    if z_cord == False && z_indx == False:
        raise Exception("Set Z_cord or Z_indx")
    if z_cord != False:
        z_indx = get_z_indx(z_cord, data_dir)
    
    ar_file_name    = 'out/ar.' + '%04g' % z_indx
    ai_file_name    = 'out/ai.' + '%04g' % z_indx

    ar  = numpy.genfromtxt(ar_file_name)
    ai  = numpy.genfromtxt(ai_file_name)
    
    a   = ar + 1j * ai
    a2  a * a.conjugate()
    a2  = a2.real
    return a2

def get_cord(data_dir, axis):
    cord_file   = open('out/' + axis)
    cords   = [ float(i) for i in cord_file.readlines() ]
    return cords

def x_cord(data_dir):
    return get_cord(data_dir, 'x')

def y_cord(data_dir):
    return get_cord(data_dir, 'y')

def z_cord(data_dir):
    return get_cord(data_dir, 'z')

if __name__ == '__main__':
    pass
