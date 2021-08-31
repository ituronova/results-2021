#!/usr/bin/env python3

# script edit yang textfile

import argparse
import csv
import sys
import glob
import re
import os
import json
import pandas as pd
import shutil
   

for folder in glob.glob("./*"):
    if("ALL" in folder or "graph" in folder or "temp" in folder or not os.path.isdir(folder) or "pyca" in folder):
        continue
    for file in glob.glob(folder + "/tmp/*.csv"):
        shutil.move(file, folder + "/")
        

def compare(line1, line2):
   if(len(line1) > 1 and len(line2) > 1):
       l = line1[1] #re2
       a1 = l == "TO" or (l != "ERR" and  "nvalid" not in l and  "Err" not in l and "HERE" not in l and "tar" not in l and len(l) > 0 and float(l) > 10)
       l = line2[1] #re2
       a2 = l== "TO" or (l != "ERR" and  "nvalid" not in l and  "Err" not in l and "HERE" not in l and "tar" not in l and len(l) > 0 and float(l) > 10)
       if(a1 and not a2):
            return True
       if(a2 and not a1):
            return False
       
       a1 = [1 for l in line1[1:3] + line1[4:6] + [line1[13]] if l == "TO" or ("nvalid" not in l and l != "ERR" and  "Err" not in l and "HERE" not in l and "tar" not in l and len(l) > 0 and float(l) > 10)]
       a2 = [1 for l in line2[1:3] + line2[4:6] + [line2[13]] if l == "TO" or ("nvalid" not in l and l != "ERR" and  "Err" not in l and "HERE" not in l and "tar" not in l and len(l) > 0 and float(l) > 10)]
       if(a1 > a2):
            return True
       if(a2 > a1):
            return False
       
   l1 = [1 for l in line1[0:14] if l == "TO" or ("nvalid" not in l and l != "ERR" and  "Err" not in l and "HERE" not in l and "tar" not in l and len(l) > 0 and float(l) > 10)]
   l2 = [1 for l in line2[0:14] if l == "TO" or ("nvalid" not in l and l != "ERR" and  "Err" not in l and "HERE" not in l and "tar" not in l and len(l) > 0 and float(l) > 10)]
   if(len(l1) == 0):
      return False
   if(len(l2) == 0):
      return True
   return len(l1) > len(l2)


for folder in glob.glob("./*"):
    if("ALL" in folder or "graph" in folder or "temp" in folder or not os.path.isdir(folder) or "pyca" in folder):
        continue
    if(not os.path.exists(folder + "/removeDup")):
        os.mkdir(folder + "/removeDup")   
    with open(folder + "/removeDup/analysis.csv", 'w') as csvFile: 
        csvFile.write('Benchmarks;Patterns\n')

    for fname in glob.glob(folder + "/*.csv"):
        fname = os.path.basename(fname)
        lines = {}
        with open(folder + "/"+fname, 'r') as csvFile:
            index =0
            reg = 0
            for line in csvFile:
                splittedLine = line[:-1].split(';')
                prefix = []
                j=0
                index += 1
                if(index == 1):
                    with open(folder + "/removeDup/"+ fname, 'a+') as outFile:
                       outFile.write(line)
                       continue
                while(j < len(splittedLine) -1 and ("./att" not in splittedLine[j] and "../text" not in splittedLine[j] and "./att" not in splittedLine[j] and "./text" not in splittedLine[j] and "attacks" not in splittedLine[j] and "../run" not in splittedLine[j] and "generated" not in splittedLine[j])):
                    prefix.append(splittedLine[j])
                    j+=1
                
                regex = (';').join(splittedLine[:j])
                rest = [splittedLine[j], [l.replace(",", ".")  for l in splittedLine[j+1:]]]
                
                if(regex[0] == '\"'):
                    regex = regex[1:-1]
                if(regex not in lines.keys()):
                    lines[regex] = rest
                else:
                   reg += 1
                   if(compare(rest[1], lines[regex][1])):
                      lines[regex] = rest
        with open(folder + "/removeDup/"+ fname, 'a+') as outFile:         
             for item in lines.items():
                outFile.write(item[0] + ";" +item[1][0] + ";" + (';').join(item[1][1]) + "\n")
        with open(folder + "/removeDup/analysis.csv", 'a+') as csvFile: 
           csvFile.write(fname+';'+str(reg)+'\n')              
       # break            
    if(not os.path.exists(folder + "/original-dup")):
        os.mkdir(folder + "/original-dup")
    for file in glob.glob(folder + "/*.csv"):
        shutil.move(file, folder + "/original-dup")
    for file in glob.glob(folder + "/removeDup/*.csv"):
        shutil.move(file, folder)    
    os.rmdir(folder + "/removeDup")          


if(not os.path.exists("./temp")):
    os.mkdir("./temp")


line = []
csv_columns = []

def analyze(r1, base, folder):
    index = 0 
    listT = []
    attacks = 0
    with open(r1, newline='') as csvfile:
        #spamreader = csv.reader(csvfile, delimiter=';')
        for row in csvfile:
            index += 1
            splittedLine = row.split(";")
            
            
            if(index == 1):
                
                continue
            #dot, python, perl, ruby, java, node
            #print(len(row))
            #print(row)
            j = 0
            #print(splittedLine)
            while("../text" not in splittedLine[j] and "./att" not in splittedLine[j] and "./text" not in splittedLine[j]  and "./gen" not in splittedLine[j] and "../run" not in splittedLine[j] and "./texts" not in splittedLine[j] and "./attac" not in splittedLine[j]):
                j += 1
            regex = (";").join(splittedLine[0:j])
            if(regex[0] == '\"'):
                regex = regex[1:-1]
                
            regex = regex.replace("\"\"", "\"")
                        
            
            att = splittedLine[j+1:j+15]
            attacks_back = [att[0]] + [att[3]] + att[6:13]
            
            attacks_aut = att[1:3] + att[4:6] + [att[13]]
            re = att[1]
            
            
            tos = len([1 for r in att if len(r) != 0 and r != "ERR" and "nvalid" not in r and "Er" not in r and "in" not in r and (r == "TO" or float(r.replace(",", ".")) > 10)] )
            if( tos > 0):
                # filter attack
                if(regex not in listT):
                    listT.append(regex)
                    with open(folder + "/timeouted/" + base + ".txt",  "a", newline='') as outFile:
                        outFile.write(regex + "\n")
                    attacks += 1 
                # filter backtracking timeouts
                tot = len([1 for r in attacks_back if len(r) != 0 and r != "ERR" and "nvalid" not in r and "Er" not in r and "in" not in r and (r == "TO" or float(r.replace(",", ".")) > 10)] )
                if(tot > 0):
                    with open(folder + "/timeouted-back/" + base + ".txt",  "a", newline='') as outFile:
                        outFile.write(regex + "\n")
                
                # filter automata timeouts
                tot = len([1 for r in attacks_aut if len(r) != 0 and r != "ERR" and "nvalid" not in r and "Er" not in r and "in" not in r and (r == "TO" or float(r.replace(",", ".")) > 10)] )
                if(tot > 0):
                    with open(folder + "/timeouted-aut/" + base + ".txt",  "a", newline='') as outFile:
                        outFile.write(regex + "\n")
                if(re != "ERR" and (re == "TO" or float(re.replace(",", ".")) > 10)):    
                    with open(folder + "/timeouted-aut/" + base + ".csv",  "a", newline='') as outFile:
                        outFile.write(row)
                
    #dict_data = [{'Benchmark': basename, folder +'-patterns': str(len(listT)),  folder + '-attacks': str(attacks)}]
    dict_data = [{'Benchmark': basename,  folder + '-attacks': str(attacks)}]
    
    
    
    csv_file = "./temp/" + folder + ".csv"
    try:
        with open(csv_file,  "a+", newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=csv_columns, delimiter=';')
            for data in dict_data:
                writer.writerow(data)
    except IOError:
        print("I/O error")
    
    

    
    return;
  
for folder in glob.glob("*"): 
    if("ALL" in folder or "graph" in folder or "temp" in folder or not os.path.isdir(folder) or "pyca" in folder):
        continue
    if(not os.path.exists(folder + "/timeouted/")):
        os.mkdir(folder + "/timeouted/")
    if(not os.path.exists(folder + "/timeouted-aut/")):
        os.mkdir(folder + "/timeouted-aut/")
    if(not os.path.exists(folder + "/timeouted-back/")):
        os.mkdir(folder + "/timeouted-back/")
    csv_columns = ['Benchmark',  folder + '-attacks']
    
    with open("./temp/" + folder + ".csv",  "w", newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=csv_columns, delimiter=';')
        writer.writeheader()
        
    for file in glob.glob(folder + "/*.csv"):
        basename = os.path.basename(file)[:-4].replace("table-","")
        #print(basename)
        if("analysis" in file or "*" in folder):
            continue
        analyze(file, basename, folder)
        #break
  # break
all_filenames = [i for i in glob.glob('./temp/*')]
df1 = pd.read_csv(all_filenames[0],delimiter=";")
for f in all_filenames:
    if(f == all_filenames[0]):
        continue
    df2 = pd.read_csv(f, delimiter=";")
    df1 = pd.merge(df1, df2, on=["Benchmark"], how = "outer")


df1 = df1.convert_dtypes()
print(df1)
#export to csv
df1.to_csv( "analysis-attacks.csv", index=False, sep=';')  
#df1.sum(axis = 1, skipna = True) 
    

shutil.rmtree("./temp")     
        
        