#! /usr/bin/env python
import numpy
from os.path import isdir, join
import pylab
class Data(object):
    """ Data from 2dnls solver. """
    def __init__(self, out_dir):
        if not isdir(out_dir):
            print out_dir + " is not a valid directory."

        self.x_file = open(join(out_dir, 'x'))
        self.y_file = open(join(out_dir, 'y'))
        self.z_file = open(join(out_dir, 'z'))
        
        # x, y, z data
        self.x = [ float(i) for i in self.x_file.readlines() ]
        self.y = [ float(i) for i in self.y_file.readlines() ] 
        self.z = [ float(i) for i in self.z_file.readlines() ]

        self.nx = len(self.x)
        self.ny = len(self.y)
        self.nz = len(self.z)

        self.a2 = numpy.zeros((self.nx, self.ny, self.nz))
        for i in range(self.nz):
            ar_file_name = join(out_dir, 'ar.' + '%04g' % i)
            ai_file_name = join(out_dir, 'ai.' + '%04g' % i)
            
            ar = numpy.genfromtxt(ar_file_name)
            ai = numpy.genfromtxt(ai_file_name)
            a = ar + 1j * ai
            self.a2[:, :, i]  = a * a.conjugate()
        self.a2 = self.a2.real

class ZSlice(object):
    def __init__(self, index, out_dir):
        self.x_file = open(join(out_dir, 'x'))
        self.y_file = open(join(out_dir, 'y'))

        self.x = [ float(i) for i in self.x_file.readlines() ]
        self.y = [ float(i) for i in self.y_file.readlines() ] 

        
        ar_file_name = join(out_dir, 'ar.' + '%04g' % index)
        ai_file_name = join(out_dir, 'ai.' + '%04g' % index)
        
        ar = numpy.genfromtxt(ar_file_name)
        ai = numpy.genfromtxt(ai_file_name)
        a = ar + 1j * ai
        self.a2 = a * a.conjugate()
        self.a2 = self.a2.real

def plot_all(out_dir, save_dir):
    z_file  = open(join(out_dir, 'z'))
    z = [ float(i) for i in z_file.readlines() ]
    nz = len(self.z)
    for i in range(nz):
        z_slice = ZSlice(i, out_dir)
        pylab.clf()
        pylab.imshow(z_slice, interpolation='none',
                extent=[
                        min(z_slice.x), max(z_slice.x), 
                        min(z_slice.y), max(z_slice.y) ])
        pylab.gca().set_xlabel('x/w_0')
        pylab.gca().set_ylabel('y/w_0')
        pylab.title('z = %s' % i)
        pylab.colorbar()
        pylab.savefig(join(save_dir, 'slice%s' % i)

from tools.tools import lineout, z_section
import tools.townes as townesk
# TODO
#from plots.plots import plot_all
