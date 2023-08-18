import pandas as pd
import numpy as np
import pdb
import os
data_file = os.path.join('/Users','lijiang','Dropbox (GaTech)','research','ddPCR results','per_generation_fitness/trial_sep_2020.xlsx')
data = pd.read_excel(data_file,sheet_name=4,index_col=0,usecols=range(6),nrows = 7)

#data.head()

fitness = []


for index, row in data.iterrows():
    first_point = row[1]
    xs = []
    ys = []
    for j, point in row.iteritems():
        x = j*2
        y = np.log10((first_point/point - first_point)/(1-first_point))
        xs.append(x)
        ys.append(y)
    xs = np.array(xs)
    xs = xs[:,np.newaxis]
    ys = np.array(ys)
    (a, _, _, _) = np.linalg.lstsq(xs, ys)
    fitness.append(np.log2(1/np.power(10,a[0])))
for f in fitness:
    print(f)
pdb.set_trace()
fitness = np.array(fitness)
data['fitness'] = fitness






'''
for sample in master_data:
    first_point = master_data[sample][0]
    xs = []
    ys = []
    for i in range(0,len(master_data[sample])):
        point = master_data[sample][i]
        x = i*2
        try:
            y = math.log((first_point/point - first_point)/(1-first_point), 10)
        except ZeroDivisionError:
            y = math.log((first_point/0.0001 - first_point)/(1-first_point), 10)
            Error_sample_list.append(sample)
        xs.append(x)
        ys.append(y)
    xs = np.array(xs)
    xs = xs[:,np.newaxis]
    ys = np.array(ys)
    a, _, _, _ = np.linalg.lstsq(xs, ys)
    final_data[sample] = math.log((1/pow(10,a)),2)
'''