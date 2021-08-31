#!/usr/bin/env python3

# script edit yang textfile

import argparse
import csv
import sys
import glob
import re
import os
import json
import shutil
   

class OpenFiles():
    def __init__(self):
        self.files = []
    def open(self, file_name):
        f = open(file_name)
        self.files.append(f)
        return f
    def close(self):
        list(map(lambda f: f.close(), self.files))
        
files = OpenFiles()


with open("analysis-filterDone.csv", "w") as a:
    a.write("Benchmark;Filtered Out;Found\n")
    
dictPat = {}
for file in glob.glob("./ALL_TESTED_PATTERNS/*.txt"):
    with open(file, "r") as rf:
        basename = os.path.basename(file).replace(".txt", "")
        dictPat[basename] = rf.readlines()
head = []  
for folder in glob.glob("./*"):
    if("ca-size" in folder or "ALL" in folder or "graph" in folder or "temp" in folder or not os.path.isdir(folder) or "pyca" in folder):
        continue
    with open("analysis-filterDone.csv", "a+") as a:
       a.write(folder+ "\n")
       
    for file in glob.glob(folder + "/*.csv"):
        basename = os.path.basename(file)
        bs = basename.replace("table-", "")
        lines = []
        index = 0
        if(not os.path.exists(folder + "/original/")):
          os.mkdir(folder + "/original")
        shutil.move(file, folder + "/original")
        # crate tmp if not exists
        if(not os.path.exists(folder + "/tmp")):
            os.mkdir(folder + "/tmp/")
        # read input file
        r1 = open(folder + "/original/" + basename, "r")
        i = 0
        found = 0
        # iterate over a folder        
        for row in r1:
            i += 1  
            if(i == 1):
               # remember the head 
               head = row
               continue
            j = 0
            splittedLines = row.split(";")
            while("../text" not in splittedLines[j] and "./att" not in splittedLines[j] and "./text" not in splittedLines[j]  and "./gen" not in splittedLines[j] and "../runGen" not in splittedLines[j] and "./texts" not in splittedLines[j] and "./attac" not in splittedLines[j]):
                j += 1
            regex = (";").join(splittedLines[0:j])
            # cut quotes if needed
            try:
                if(regex[0] == "\""):
                    regex = regex[1:-1]
            except:
                print(file)
                continue
            # replace double quotes
            regex = regex.replace("\"\"", "\"")
            flagF = False
            for d in dictPat.keys():
                if(regex + "\n" in dictPat[d]):
                         found += 1
                         flagF = True
                         if(not os.path.exists(folder + "/tmp/"+ d + ".csv")):
                             fw = open(folder + "/tmp/"+ d + ".csv", "a+", newline='')
                             fw.write(head)
                             fw.write(row)
                             fw.close()
                         else:
                             fw = open(folder + "/tmp/"+ d + ".csv", "a+", newline='')
                             fw.write(row)
                             fw.close()
                         
            if(not flagF):
                index += 1
        r1.close()
        with open("analysis-filterDone.csv", "a+") as a:
            a.write(basename + ";"+str(index) + ";"+str(found)+"\n")
       
files.close()