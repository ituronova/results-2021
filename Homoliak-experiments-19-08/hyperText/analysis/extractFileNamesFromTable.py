#!/usr/bin/env python3

import argparse
import csv
import sys
import glob
import os

for name in glob.glob("./*.csv"):
    if("anal" in name):
        continue
    if("noedit" in name):
        continue
    file1 = open(name, 'r', encoding="utf8")
    lines = []
    
    basename = os.path.basename(name).replace(".csv", ".txt")
    b = basename.split('_')
    basename = ("_").join(b)
    basename = basename.replace("genText-","")
    basename = basename.replace("table-","")
    index = 0
    outputfile = "missing.txt" 
    for line in file1:
        j = 0;
        index += 1
        if(index == 1):
            continue
        splittedLine = line.split(';')
        #print(splittedLine)
        while("./hyperTexts" not in splittedLine[j] and "../text" not in splittedLine[j]and "./text" not in splittedLine[j] and "../runGen" not in splittedLine[j] and "./gen" not in splittedLine[j] and "./attack" not in splittedLine[j]):
            j += 1
        #regex = (';').join(splittedLine[0:j])
        #if(regex[0] == "\""):
         #   regex = regex[1:-1]
        inputfile = splittedLine[j]
        #regex = regex.replace("\"\"", "\"")
        #regex = regex.replace("\\", "\\\\")
        #regex = regex.replace("\"", "\\\"")
        lines.append(inputfile + "\n")
            
    
    file1.close() 
    if(not os.path.exists("./fileNames")):
        os.mkdir("./fileNames")
    file2 = open("./fileNames/"+ outputfile , 'a+', encoding="utf8")
   # print(lines)
    for line in lines:
        file2.write(line)
    file2.close() 
    