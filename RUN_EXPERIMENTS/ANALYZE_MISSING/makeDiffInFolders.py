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
   
for folder in glob.glob("./*"):
    fileList = []
    if("graph" in folder or "ALL" in folder or "temp" in folder or "pyca" in folder):
        continue
    if(not os.path.isdir(folder)):
        continue
    if(not os.path.exists(folder+"/diff/")):
        os.mkdir(folder+"/diff/")
    if(not os.path.exists(folder+"/diff/doneExtra/")):
        os.mkdir(folder+"/diff/doneExtra/")
    if(not os.path.exists(folder+"/diff/missExtra/")):
        os.mkdir(folder+"/diff/missExtra/")
    if(not os.path.exists(folder+"/patterns/")):
        os.mkdir(folder+"/patterns/")
    with open(folder+"/diff/analysis-missing.csv", "a+") as r1:
            r1.write("Benchmarks;Extra;Missing;Sum\n")
    print(folder)
    
    for file in glob.glob(folder + "/*.csv"):
        if("ana" in file):
            continue
        with open(file, "r") as rf:
            basename = os.path.basename(file)
            lines = rf.readlines()
            index = 0
            for row in lines:
                 splittedLines = row.split(";")
                 j= 0
                 index += 1
                 if(index == 1):
                        continue
                 while("./gen" not in splittedLines[j] and "../runGen" not in splittedLines[j] and "./texts" not in splittedLines[j] and "./attack" not in splittedLines[j]):
                     j += 1
                 regex = (";").join(splittedLines[0:j])
                 regex = regex.replace("\"\"", "\"")
                 if(regex[0] == '\"'):
                     regex = regex[1:-1]
                 with open(folder+"/patterns/"+basename.replace(".csv", ".txt"), "a+") as w1:
                    w1.write(regex + "\n")
       # break 
    for file in glob.glob(folder + "/patterns/*.txt"):
        if("ana" in file):
            continue
        basename = os.path.basename(file)
        fileList.append(basename)
        filtered = []
        filtered2 = []
        filteredOr = []
        filtered2Ed = []
        filtered3 = []
        plus = 0
        minus = 0
        with open(file, "r") as r1:
            for line in r1:
                filtered.append(line)
        if(os.path.exists("./ALL_TESTED_PATTERNS/"+basename)):
            with open("./ALL_TESTED_PATTERNS/"+basename, "r") as r2:
                        for line in r2:
                            filtered2.append(line)
                        
        
        #print('---------------')    
        #for r in filtered2Ed:
         #   print(r) 
            
        for r in range(0, len(filtered)):
            reg = filtered[r]
            if(reg not in filtered2):
                with open(folder+"/diff/doneExtra/"+basename, "a") as w1:
                    w1.write(reg)
                    minus += 1
                            
        for reg in filtered2:
            if(reg not in filtered):
               with open(folder+"/diff/missExtra/"+basename, "a") as w2:
                w2.write(reg)
                plus += 1
        
        with open(folder+"/diff/analysis-missing.csv", "a+") as r1:
            r1.write(basename+";"+str(plus)+";"+str(minus)+";"+str(minus-plus)+"\n")
                  
    #for patternFile in glob.glob("./ALL_TESTED_PATTERNS/*.txt"):
     #   pFile = patternFile.replace("ALL_TESTED_PATTERNS", folder + "/diff")
      #  if(patternFile not in fileList):
       #     shutil.copy(patternFile, folder + "/diff/missExtra/")
        
        
        