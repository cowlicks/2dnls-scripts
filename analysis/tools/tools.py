#! /usr/bin/env python

def lineout(a, z_indx, line_height=None):
    if line_height is None:
        line_height = len(a.a2[ :, 0, 0])/2
    return a.x, a.a2[line_height, :, z_indx]

def z_section(a, z_indx):
    return a.a2[:, :, z_indx]

