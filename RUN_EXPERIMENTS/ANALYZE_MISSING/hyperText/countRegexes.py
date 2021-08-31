#!/usr/bin/env python3

# script edit yang textfile

import argparse
import csv
import sys
import glob
import re
import os
import json

with open("analysis-vuln.csv", 'w', newline='') as csvfile:
    writer = csv.writer(csvfile, delimiter=';')
    writer.writerow(['Benchmarks', 'Patterns']) 
    
for file in glob.glob("*.csv"):
    basename = file[0:len(file)-4]
    count = sum(1 for line in open(file))  -1  
    with open("analysis-vuln.csv", 'a', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=';')
        writer.writerow([basename, count])
        
            