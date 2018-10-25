#!/usr/bin/env python

import numpy
import nibabel
from scipy.io import loadmat
import os
import sys

ident = sys.argv[2]
ident = ident.replace("-","")
ident = ident.split()
affine = []
for g in range(0,16):
	affine.append(float(ident[g]))
ident = numpy.reshape(affine,(4,4))

x = loadmat(sys.argv[1]) #TODO make this path a variable
fg_classified = x['fg_classified']

os.mkdir("output")
os.chdir("output") #creates an output directory for the .trk files

for i in range(0, len(fg_classified[0])):  #for each fiber group
    z = []
    g = fg_classified[0,i]['fibers'][0:len(fg_classified[0,i]['fibers'])] #collects all streamlines in the tract
    #g = fg_classified[0,i][8][0:len(fg_classified[0,i][8])]
    os.mkdir(fg_classified[0,i]['name'][0]) #creates a new folder for each fiber group
    os.chdir(fg_classified[0,i]['name'][0])
    for j in range(0, len(g)):  #for each streamline in the tract

        l = []
        for k in range(0, len(g[j][0][0])): #for each point in the streamline
            h = [g[j][0][0][k], g[j][0][1][k], g[j][0][2][k]]
            l.append(h)  #builds the matrix for the streamline
        z.append(l)

    s = nibabel.streamlines.array_sequence.ArraySequence(z)
    t = nibabel.streamlines.tractogram.Tractogram(streamlines=s, affine_to_rasmm=ident)
    trk = nibabel.streamlines.trk.TrkFile(t)
    trk.save(fg_classified[0,i][0][0].replace(" ","_") + ".trk") #creates the trk file for the tract

    os.chdir("..") #moves back to output directory for the next tract
