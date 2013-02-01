#! /usr/bin/env python
import pylab
import numpy
import os
import re
"""
Code to help find the optimal parameters for energy coupling.
"""

class axes:
    def __init__(self, data_dir):
        self.x_file = open(data_dir + '/x')
        self.y_file = open(data_dir + '/y')
        self.z_file = open(data_dir + '/z')

        # get the x, y, z data
        self.x = [ float(i) for i in self.x_file.readlines() ]
        self.y = [ float(i) for i in self.y_file.readlines() ]
        self.z = [ float(i) for i in self.z_file.readlines() ]
        
        self.nx = len(self.x)
        self.ny = len(self.y)
        self.nz = len(self.z)

class a_data:
    def __init__(self, data_dir, ar_filename, ai_filename):
        ar_filename = data_dir + ar_filename
        ai_filename = data_dir + ai_filename
        self.ar = numpy.genfromtxt(ar_filename)
        self.ai = numpy.genfromtxt(ai_filename)
        self.a  = self.ar + 1j * self.ai
        self.a2_im  = self.a * self.a.conjugate()
        self.a2 = self.a2_im.real

def get_coupled_e(a2, e_ratio):
    """
    Sum the value of all cells with a value higher than thresh. e_ratio is:
    (energy in a pixel)/(total energy)
    """
    e_total     = 0.
    e_coupled   = 0.
    for cell in a2.flat:
        e_total += cell
    e_thresh = e_ratio * e_total
    for cell in a2.flat:
        if cell > e_thresh:
            e_coupled += cell
    return e_coupled/e_total

def get_spread_pz_lists(datadir):
    dirs = os.listdir(datadir)
    # get spreads
    strings = [ re.search('spread(.*)_pz(.*)', i) for i in dirs ]
    spreads = []
    pzs     = []
    for i in strings:
        spreads.append(i.group(1))
        pzs.append(i.group(2))
    # sort them
    spreads = list(set(spreads))
    pzs = list(set(pzs))
    spreads.sort()
    pzs.sort()
    return spreads, pzs




if __name__ == '__main__':
    home = os.path.expanduser('~')
    DATA_DIR = '/2dnls/data'
    RATIO = .2
    RANGE = range(75, 81)
    ar_filenames = [ '/ar.' + '%04g' % i for i in RANGE ]
    ai_filenames = [ '/ai.' + '%04g' % i for i in RANGE ]
    spreads, pzs = get_spread_pz_lists(home + DATA_DIR)
    sprd_vs_pz = numpy.zeros((len(pzs), len(spreads)))
    # Generate sprd_vs_pz.
    for sprd_indx in range(len(spreads)):
        for pz_indx in range(len(pzs)):
            data_subdir = '/spread' + spreads[sprd_indx] + '_pz' + pzs[pz_indx] + '/out' 
            path_to_data = home + DATA_DIR + data_subdir
            # get the average a2.
            coupled_e = 0.
            for fn_indx in range(len(ar_filenames)):
                try:
                    a = a_data(path_to_data, 
                                ar_filenames[fn_indx], 
                                ai_filenames[fn_indx])
                except IOError:
                    sprd_vs_pz[pz_indx, sprd_indx] = 0
                    print 'Error in ' + path_to_data 
                    break
                coupled_e += get_coupled_e(a.a2, RATIO)
            avg_coupled = coupled_e / len(ar_filenames)
            sprd_vs_pz[pz_indx, sprd_indx] = avg_coupled
    # Get some axes data.
    axis_data = axes(path_to_data)


    print sprd_vs_pz
    pylab.imshow(sprd_vs_pz, interpolation='nearest', origin='lower',
                extent=[float(min(spreads)), float(max(spreads)),
                    float(min(pzs)), float(max(pzs))])

    pylab.colorbar()
    pylab.show()



