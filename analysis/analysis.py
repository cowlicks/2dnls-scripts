#! /usr/bin/env python
import matplotlib
# Tell matplotlib to use Agg backend so that it does not need $DISPLAY
matplotlib.use('Agg')
import numpy
import pylab
class data:
    """ Data from 2dnls solver. """
    def __init__(self):
        self.x_file = open('out/x')
        self.y_file = open('out/y')
        self.z_file = open('out/z')
        
        # x, y, z data
        self.x = [ float(i) for i in self.x_file.readlines() ]
        self.y = [ float(i) for i in self.y_file.readlines() ] 
        self.z = [ float(i) for i in self.z_file.readlines() ]

        self.nx = len(self.x)
        self.ny = len(self.y)
        self.nz = len(self.z)

        self.a2 = numpy.zeros((self.nx, self.ny, self.nz))
        for i in range(self.nz):
            ar_file_name = 'out/ar.' + '%04g' % i
            ai_file_name = 'out/ai.' + '%04g' % i
            
            ar = numpy.genfromtxt(ar_file_name)
            ai = numpy.genfromtxt(ai_file_name)
            a = ar + 1j * ai
            self.a2[:, :, i]  = a * a.conjugate()

        self.a2 = self.a2.real

        # Max value at each z.
        self.max_a2 = [numpy.amax(self.a2[:, :, i]) for i in range(self.nz)]
        # Total energy. This is constant up to rounding error, so it is only
        # computed at one z.
        self.total_a2 = 0
        for i in self.a2[:, :, 0].flat:
            self.total_a2 += i

    def plot(self, a2_slice):
        """ Plot a grid """
        pylab.imshow(a2_slice, extent=[min(self.x), max(self.x), min(self.y), max(self.y)])
        pylab.gca().set_xlabel('x/w_0')
        pylab.gca().set_ylabel('y/w_0')
        pylab.colorbar()
        pylab.title('Title')
        pylab.show()

    def make_plots(self, a2):
        """ Create image files for all z"""
        for i in range(self.nz):
            pylab.clf()
            pylab.imshow(a2[:, :, i], interpolation='none', extent=[
                min(self.x), max(self.x), min(self.y), max(self.y)])
            pylab.gca().set_xlabel('x/w_0')
            pylab.gca().set_ylabel('y/w_0')
            pylab.title('z = %s' % i)
            pylab.colorbar()
            pylab.savefig("pylabfig" + str(i))
    def total_e(self, a2_slice):
        """ Sum the energy in a2_slice."""
        sum = 0
        for cell in a2_slice.flat:
            sum += cell
        return sum
    def thresh_e(self, a2_slice, e_thresh):
        """ Return the index and value of all cells above a given energy
        threshold."""
        above = []
        for i, val in numpy.ndenumerate(a2_slice):
            if val > e_thresh:
                above.append(i)
        return above
    def ratio_e(self, a2_slice, e_ratio):
        """ Return the index and value of all cells above given energy ratio to
        the total energy in a2_slice """
        above = []
        for i, val in numpy.ndenumerate(a2_slice):
            if val/self.total_a2 > e_ratio:
                above.append(i)
        return above
    def top_view(self, a2):
        """ Generate a top down veiw of the laser propagating through the
        plasma. """
        top_view = numpy.zeros((self.nz, self.nx))
        for z in range(self.nz):
            for col in range(self.nx):
                col_sum = 0
                for row in range(self.ny):
                   col_sum += a2[row, col, z]
                top_view[z, col] = col_sum
        return top_view
    def plot_top_view(self, a2):
        top_view = numpy.zeros((self.nz, self.nx))
        for z in range(self.nz):
            for col in range(self.nx):
                col_sum = 0
                for row in range(self.ny):
                   col_sum += a2[row, col, z]
                top_view[z, col] = col_sum
        pylab.clf()
        pylab.imshow(top_view, interpolation='none', extent=[min(self.x),
            max(self.x), min(self.z), max(self.z)])
        pylab.gca().set_ylabel('z/z_r')
        pylab.gca().set_xlabel('x/w_0')
        pylab.title('Top view')
        pylab.colorbar()
        pylab.savefig('Top_view')

d = data()
d.make_plots(d.a2)
d.plot_top_view(d.a2)
