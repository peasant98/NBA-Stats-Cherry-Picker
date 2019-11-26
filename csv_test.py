import csv
import numpy as np

with open('dict.csv', 'w', newline="") as csv_file: 
    my_dict = {1: np.array([1,2,3]), 2:[1,2,3,4]}
    writer = csv.writer(csv_file)
    for key, value in my_dict.items():
       writer.writerow([key, value])


with open('dict.csv') as csv_file:
    reader = csv.reader(csv_file)
    mydict = dict(reader)
    print(my_dict)