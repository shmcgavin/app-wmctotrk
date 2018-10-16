#!/usr/bin/env python

import numpy
import nibabel
from scipy.io import loadmat
import os

ident = numpy.eye(4) #TODO allow this to be a variable inputted by user


x = loadmat('/Users/davidhunt/Documents/5bb62f5112512a003f32ed4e/output.mat') #TODO make this path a variable
fg_classified = x['fg_classified']
fg_classified = loadmat('/Users/davidhunt/Documents/5bb62f5112512a003f32ed4e/output.mat')['fg_classified']

os.mkdir("output")
os.chdir("output") #creates an output directory for the .trk files

for i in range(0, len(fg_classified[0])):  #for each fiber group


    g = fg_classified[0,i][8][0:len(fg_classified[0,i][8])]   #collects all tracts in the group
    os.mkdir(fg_classified[0,i][0][0]) #creates a new folder for each fiber group
    os.chdir(fg_classified[0,i][0][0])
    for j in range(0, len(g)):  #for each tract in the group

        l = []
        for k in range(0, len(g[j][0][0])): #for each point in the tract
            h = [g[j][0][0][k], g[j][0][1][k], g[j][0][2][k]]
            l.append(h)  #builds the matrix for the tract


        s = nibabel.streamlines.array_sequence.ArraySequence([l])
        t = nibabel.streamlines.tractogram.Tractogram(streamlines=s, affine_to_rasmm=ident)
        trk = nibabel.streamlines.trk.TrkFile(t)
        trk.save("output" + str(i) + "by" + str(j) + ".trk") #creates the trk file with "i" and "j" (fiber group #, and tract #) appended

    os.chdir("..") #moves back to output directory for the next fiber group
