#!/usr/bin/env python3

# script edit yang textfile

import argparse
import sys
import glob
import re
import os
import pathlib

textFile = "all.txt"
index = 0
for name in glob.glob("./*.txt"):
    if(textFile in name):
        continue 
    with open(name, 'r') as infile:
        for line in infile.readlines(): 
            outfile = open(textFile, 'a+')
            outfile.write(line)

