#!/usr/bin/env python3

import argparse
import csv
import sys
import glob
import os

for name in glob.glob("./*.csv"):
    if("anal" in name):
        continue
    file1 = open(name, 'r', encoding="utf8")
    lines = []
    basename = os.path.basename(name).replace(".csv", ".txt").replace("table-","")
    index = 0
    outputfile = os.path.basename(name)[:-4]
    for line in file1:
        j = 0;
        index += 1
        if(index == 1):
            continue
        splittedLine = line.split(';')
        while("./hyperTexts" not in splittedLine[j] and "./text" not in splittedLine[j] and"../text" not in splittedLine[j] and"../runGen" not in splittedLine[j] and "./gen" not in splittedLine[j] and "./attack" not in splittedLine[j]):
            j += 1
        regex = (';').join(splittedLine[0:j])
        if(regex[0] == "\""):
            regex = regex[1:-1]
        inputfile = splittedLine[j]
        regex = regex.replace("\"\"", "\"")
        regex = regex.replace("\\", "\\\\")
        regex = regex.replace("\"", "\\\"")
        
        inputfile = "../runGen5/hyperTexts/" + ("/").join(inputfile.split("/")[-2:])
        lines.append("{\"regex\":\"" + regex + "\", \"file\":\"" + inputfile + "\"}\n")
            
    
    file1.close() 
    if(not os.path.exists("./experiments")):
        os.mkdir("./experiments")
    file2 = open("./experiments/"+ basename , 'w', encoding="utf8")
    for line in lines:
        file2.write(line)
    file2.close() 
    