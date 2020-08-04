#!/usr/bin/env python3

import os
import sys
import json
import argparse

import numpy as np
from scipy.io import loadmat

import nibabel as nib
from nibabel.streamlines import Field
from nibabel.orientations import aff2axcodes

if __name__ == '__main__':
    with open('config.json') as config_f:
        config = json.load(config_f)
    
    print("loading %s" % config['tck'])
    tck = nib.streamlines.load(config['tck'])
    print("loading %s" % config['wmc'])
    wmc = loadmat(config['wmc'])
    print("loading %s" % config['t1'])
    t1 = nib.load(config['t1'])

    #use index as bundle_code
    index = wmc['classification']['index'][0][0]
    bundle_code = data_per_streamline = {'bundle_code': index}

    #save as trk
    trk = nib.streamlines.tractogram.Tractogram( \
        data_per_streamline=bundle_code, \
        affine_to_rasmm=t1.affine, \
        streamlines=tck.streamlines)
    nib.streamlines.save(trk, "trk/track.trk")


