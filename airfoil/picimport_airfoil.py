#!/usr/bin/env python

from io import StringIO
import urllib.request
import os

filename = []

data_file = "airfoil_bilder.txt"
current_folder = os.path.dirname(__file__)
data_file_path = os.path.join(current_folder, data_file)

f = open(data_file_path, "r")
for line in f:
    ls=line.split(".")
    filename.append(ls[0])
f.close()
numb= len(filename)
print (numb)

url_gif = "http://www.ae.illinois.edu/m-selig/ads/afplots/"
url_dat = "http://www.ae.illinois.edu/m-selig/ads/coord/"
x = 0
for line in filename:
    file_name=str(url_dat)+str(line)+".dat"
    try:
        file =urllib.request.urlopen(file_name)
    except IOError:
        print ('cannot open', file_name)
    else:
        inhalt = file.read() 
        file.close()
        name= "data/"+str(line)+".dat"
        f = open(name , 'w')
        f.write(inhalt)
        f.close()
        x=x+1
        print (x)

print ("done")
