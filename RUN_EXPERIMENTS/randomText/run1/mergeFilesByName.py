#!/usr/bin/env python3

# script edit yang textfile

import argparse
import csv
import sys
import glob
import re
import os
import pathlib
import shutil


if(not os.path.exists("./merged")):
    os.mkdir("./merged")
for fname in glob.glob("./*.txt"):
    os.remove(fname)
for fname in glob.glob("./*.csv"):
    base = os.path.basename(fname)
    baseName = base.split('_')
    baseName = ('_').join(baseName[0:-1])
    print(baseName)
    outfilename = "./merged/"+baseName+".csv"
    index = 0
    done = 0
    
        
    with open(fname, 'r') as readfile:
            lines = readfile.readlines() 
            
            for line in lines: 
                index += 1
                if(index > 1 or not os.path.exists(outfilename)):
                    
                    with open(outfilename, 'a+') as outfile:
                        outfile.write(line)
                
                
                
                