#!/usr/bin/env python

import os
import sys
import json
import argparse
import numpy as np
import nibabel as nib
from scipy.io import loadmat
from dipy.tracking.utils import move_streamlines

def wmc_to_trk(tck, wmc, t1, trk_out, json_out=False):
    """
    Read a wmc matlab data structure and a reference image as input.
    Output a trk file as a single collection of classified fibers.
    A numerical code is associated to each fiber to denote the
    specific bundle. An optional json file may report the labels of
    bundles.
    """
        
    #fg_classified = wmc['fg_classified']
    classification = wmc['classification']
    
    affine = t1.affine
    header = t1.header
    dim = header.get_data_shape()[:3]
    vox_sizes = header.get_zooms()[:3]

    bundles = []
    all_streamlines = []
    labels = {'bundles' : []}
    
    # Loop through all bundles
    #tract_idx=0
    index = classification['index'][0][0]
    #print("classification-----------------")
    #print(classification['index'][0][0])

    #count fibers for each classification
    unique, counts = np.unique(index, return_counts=True)
    bundle_counts = dict(zip(unique, counts))

    tract_idx=0
    for name in classification['names'][0][0]:
        tract_idx+=1
        print tract_idx,name[0]
    #
    #    # loop through all the streamline of a bundle
    #    indexes = np.where(index == tract_idx)
    #    #print(indexes)
    #    #print(tck)
    #    #print(np.take(tck.streamlines, indexes))
    #    bundle = np.take(tck.streamlines, indexes[0])
    #    all_streamlines.append(np.array(bundle))

    #    bundle_index = np.empty(len(indexes[0]), dtype=np.uint8)
    #    bundle_index.fill(tract_idx)
    #    bundles.extend(bundle_index)

        info = {}
        info['id'] = tract_idx
        info['label'] = str(name[0][0])
        info['count'] = bundle_counts[tract_idx]
        labels['bundles'].append(info)
   
    #print("pulling non0 - indexes")
    indexes = np.where(index != 0)
    #print(indexes)
    #print("pulling non0 - streamlines")
    #print(indexes[0])
    non0_streamlines = np.take(tck.streamlines, indexes[0])
    #print(non0_streamlines)
    #print(non0_streamlines)

    bundle_code = {'bundle_code': index}

    transformed_streamlines = move_streamlines(non0_streamlines, np.linalg.inv(affine))
    t = nib.streamlines.tractogram.Tractogram( \
        data_per_streamline=bundle_code, \
        streamlines=transformed_streamlines, \
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
    #arser = argparse.ArgumentParser()
    #args = parser.parse_args()
    with open('config.json') as config_f:
        config = json.load(config_f)
    
    print("loading %s" % config['tck'])
    tck = nib.streamlines.load(config['tck'])
    print("loading %s" % config['wmc'])
    wmc = loadmat(config['wmc'])
    print("loading %s" % config['t1'])
    t1 = nib.load(config['t1'])

    print("converting to trk")
    wmc_to_trk(tck, wmc, t1, "trk/track.trk", "trk/info.json")

    sys.exit()
    

