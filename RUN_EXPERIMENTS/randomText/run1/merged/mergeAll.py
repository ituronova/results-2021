#!/usr/bin/env python3

# script edit yang textfile

import argparse
import csv
import sys
import glob
import re
import os
import pathlib

textFile = "50MB.csv"
index = 0
for name in glob.glob("./*.csv"):
    if(textFile in name):
        continue 
    with open(name, 'r') as infile:
        for line in infile.readlines(): 
            index += 1
            #print(line)
            if(index == 1 or "pattern;" not in line):
                 outfile = open(textFile, 'a+')
                 outfile.write(line)

