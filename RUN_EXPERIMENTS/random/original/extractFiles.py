import csv
import glob
import os
import sys
import re
from os import path
import shutil

    
    
for folder in glob.glob("./res*"):
    for file in glob.glob(folder + "/*"):
        basename = os.path.basename(file)
        if(not os.path.exists(basename)):
            shutil.move(file, "./")
   