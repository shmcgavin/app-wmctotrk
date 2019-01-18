#!/usr/bin/env python

import os
import sys
import json
import argparse
import numpy as np
import nibabel as nib
from scipy.io import loadmat
from dipy.tracking.utils import move_streamlines


def wmc_to_trk(wmc_src, img_src, trk_out, json_out=False):
    """
    Read a wmc matlab data structure and a reference image as input.
    Output a trk file as a single collection of classified fibers.
    A numerical code is associated to each fiber to denote the
    specific bundle. An optional json file may report the labels of
    bundles.
    """
        
    wmc = loadmat(wmc_src)
    fg_classified = wmc['fg_classified']
    
    img = nib.load(img_src)
    affine = img.affine
    header = img.header
    dim = header.get_data_shape()[:3]
    vox_sizes = header.get_zooms()[:3]

    streamlines = []
    bundles = []
    labels = {'bundles' : []}
    
    # Loop through all bundles
    for i in range(0, len(fg_classified[0])):
        # collect all bundles of the same category
        g = fg_classified[0,i]['fibers'][0:len(fg_classified[0,i]['fibers'])]
    
        # loop through all the streamline of a bundle
        for j in range(0, len(g)):  
            points = []
            
            # loop through all the points of a streamline
            bundle_size = len(g[j][0][0])
            for k in range(0, bundle_size):
                p = [g[j][0][0][k], g[j][0][1][k], g[j][0][2][k]]
                points.append(p)
            streamlines.append(np.array(points))
            bundles.append(i+1)
        info = {}
        info['id'] = "%s" % (i+1)
        info['label'] = fg_classified[0,i][0][0]
        info['count'] = "%s" % len(g)
        labels['bundles'].append(info)
   
    bundle_code = {'bundle_code': bundles}    
    transformed_streamlines = move_streamlines(streamlines, np.linalg.inv(affine))
    t = nib.streamlines.tractogram.Tractogram(streamlines=transformed_streamlines, \
                                              data_per_streamline=bundle_code, \
                                              affine_to_rasmm=affine)

    # Create a new header with the correct affine 
    hdr = nib.streamlines.trk.TrkFile.create_empty_header()
    hdr['voxel_sizes'] = vox_sizes
    hdr['voxel_order'] = 'LAS'
    hdr['dimensions'] = dim
    hdr['voxel_to_rasmm'] = affine

    trk_file = nib.streamlines.trk.TrkFile(t, hdr)
    trk_file.save(trk_out)
    
    if json_out:
        with open(json_out, 'w') as trk_json:
            json.dump(labels, trk_json, indent=4)



if __name__ == '__main__':
    
    parser = argparse.ArgumentParser()
    parser.add_argument( 'wmc_src', nargs='?',default='',
                        help='The source wmc file')
    parser.add_argument('img_src', nargs='?', const=1, default='',
                        help='The reference MR image file')
    parser.add_argument('trk_out', nargs='?',  const=1, default='default',
                        help='The output tractogram trk file')
    parser.add_argument('json_out', nargs='?',  const=1, default=False,
                        help='The output json file with bundle labels')
    args = parser.parse_args()
    
    wmc_to_trk(args.wmc_src, args.img_src, args.trk_out, args.json_out)

    sys.exit()
    
