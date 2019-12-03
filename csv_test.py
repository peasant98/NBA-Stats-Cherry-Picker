import csv
import numpy as np
from multiprocessing import Process, Value, Array, Manager
import ast

with open('dict.csv', 'w', newline="") as csv_file:
    manager = Manager()
    non_legends_dict = manager.dict() 
    non_legends_dict[1] = [ '2011-12', '2011-12', '2011-12', '2011-12', '2011-12'
                             '2011-12', '2011-12', '2011-12', '2011-12', '2011-12']
    non_legends_dict[2] = [14,24,34]

    writer = csv.writer(csv_file)
    for key, value in non_legends_dict.items():
       writer.writerow([key, value])


with open('non_legends_dict.csv') as csv_file:
    reader = csv.reader(csv_file)
    mydict = dict(reader)
    print(mydict)
    x = mydict['2804']
    print(str(x))
    res = (x.strip('][').split(' '))
    m = [eval(r) for r in res]
    print(m)

