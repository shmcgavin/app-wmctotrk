#!/usr/bin/env python

import numpy as np
import nibabel as nib
from scipy.io import loadmat
import os
import sys


def save_trk(streamlines, out_file, affine=None, vox_sizes=None, vox_order='LAS', dim=None):
    """
    This function saves tracts in Trackvis '.trk' format.
    The default values for the parameters are the values for the HCP data.
    """
    if affine is None:
        affine = np.array([[  1.25,    0.  ,    0.  ,  -90.  ],
                           [   0.  ,    1.25,    0.  , -126.  ],
                           [   0.  ,    0.  ,    1.25,  -72.  ],
                           [   0.  ,    0.  ,    0.  ,    1.  ]], 
                          dtype=np.float32)
    if vox_sizes == None:
        vox_sizes = np.array([1.25, 1.25, 1.25], dtype=np.float32)   
    if dim == None:
        dim = np.array([145, 174, 145], dtype=np.int16)
    if out_file.split('.')[-1] != 'trk':
        print("Format not supported.")

    # Create a new header with the correct affine 
    hdr = nib.streamlines.trk.TrkFile.create_empty_header()
    hdr['voxel_sizes'] = vox_sizes
    hdr['voxel_order'] = vox_order
    hdr['dimensions'] = dim
    hdr['voxel_to_rasmm'] = affine
    hdr['nb_streamlines'] = len(streamlines)
    hdr['nb_properties_per_streamline'] = 1
    #hdr['property_name'] = 'track_number'
    #dps = {'track_number': np.array([])}
    #for i in range(0, len(streamlines)):
    #    dps['track_number'] = np.append(dps['track_number'], i)
    hdr['property_name'] = 'fiber_group_name'

    #for i in range(0, len(streamlines)):
        #dps['fiber_group_name'] = np.append(dps['fiber_group_name'], i)


    #t = nib.streamlines.tractogram.Tractogram(streamlines=streamlines, affine_to_rasmm=np.eye(4))
    t = nib.streamlines.tractogram.Tractogram(streamlines=streamlines, data_per_streamline=dps, affine_to_rasmm=affine)
    nib.streamlines.save(t, out_file, header=hdr)


if __name__ == '__main__':

    dps = {'fiber_group_name': np.array([])}
    x = loadmat(sys.argv[1])
    fg_classified = x['fg_classified']
    t1_fname = sys.argv[2]

    os.mkdir("output")
    z = []
    for i in range(0, len(fg_classified[0])):  #for each fiber group
        g = fg_classified[0,i]['fibers'][0:len(fg_classified[0,i]['fibers'])] #collects all streamlines in the tract
        fiber_group_name = fg_classified[0,i][0][0].replace(" ", "_")
        fg = (fiber_group_name[:20]) if len(fiber_group_name) > 20 else fiber_group_name
        for j in range(0, len(g)):  #for each streamline in the tract
            l = []
            for k in range(0, len(g[j][0][0])): #for each point in the streamline
                h = [g[j][0][0][k], g[j][0][1][k], g[j][0][2][k]]
                l.append(h)  #builds the matrix for the streamline
            z.append(l)
            dps['fiber_group_name'] = np.append(i)

    s = nib.streamlines.array_sequence.ArraySequence(z)
#    out_name = 'output/%s.trk' %fg_classified[0,i][0][0].replace(" ","_")
    out_name = 'output.trk'
    if t1_fname == None:
        save_trk(s, out_name)
    else:
        t1 = nib.load(t1_fname)
        aff_vox_to_ras = t1.affine
        header = t1.header
        dimensions = header.get_data_shape()
        voxel_sizes = header.get_zooms()
        save_trk(s, out_name, affine=aff_vox_to_ras, vox_sizes=voxel_sizes, dim=dimensions)
