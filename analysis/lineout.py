def lineout(a, slice_indx, line_height=None):
    if line_height is None:
        line_height = len(a[ :, 0, 0])/2
    return a.x, a[line_height, :, slice_indx]

def slice(a, slice_indx):
    return a[:, :, slice_indx]
