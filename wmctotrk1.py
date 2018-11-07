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
    if affine == None:
        affine = np.array([[  -1.25,    0.  ,    0.  ,   90.  ],
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

    t = nib.streamlines.tractogram.Tractogram(streamlines=s, affine_to_rasmm=np.eye(4))
    nib.streamlines.save(t, out_file, header=hdr)


#ident = sys.argv[2]
#ident = ident.replace("-","")
#ident = ident.split()
#affine = []
#for g in range(0,16):
#	affine.append(float(ident[g]))
#ident = numpy.reshape(affine,(4,4))


if __name__ == '__main__':

    x = loadmat(sys.argv[1]) #TODO make this path a variable
    fg_classified = x['fg_classified']
    t1_fname = sys.argv[2]

    os.mkdir("output")
    #os.chdir("output") #creates an output directory for the .trk files

    for i in range(0, len(fg_classified[0])):  #for each fiber group
        z = []
        g = fg_classified[0,i]['fibers'][0:len(fg_classified[0,i]['fibers'])] #collects all streamlines in the tract
        #g = fg_classified[0,i][8][0:len(fg_classified[0,i][8])]
        #os.mkdir(fg_classified[0,i]['name'][0]) #creates a new folder for each fiber group
        #os.chdir(fg_classified[0,i]['name'][0])
        for j in range(0, len(g)):  #for each streamline in the tract
            l = []
            for k in range(0, len(g[j][0][0])): #for each point in the streamline
                h = [g[j][0][0][k], g[j][0][1][k], g[j][0][2][k]]
                l.append(h)  #builds the matrix for the streamline
            z.append(l)

        s = nib.streamlines.array_sequence.ArraySequence(z)
        #t = nibabel.streamlines.tractogram.Tractogram(streamlines=s, affine_to_rasmm=np.eye(4))
        #trk = nibabel.streamlines.trk.TrkFile(t)
        out_name = 'output/%s.trk' %fg_classified[0,i][0][0].replace(" ","_")
        #trk.save(fg_classified[0,i][0][0].replace(" ","_") + ".trk") #creates the trk file for the tract

        if t1_fname == 'null':
            save_trk(s, out_name)
        else:
            t1 = nib.load(t1_fname)
            aff_vox_to_ras = t1.affine
            header = t1.header
            dimensions = header.get_data_shape()
            voxel_sizes = header.get_zooms()
            save_trk(s, out_name, affine=aff_vox_to_ras, vox_sizes=voxel_sizes, dim=dimensions)

        #os.chdir("..") #moves back to output directory for the next tract
