import pandas as pd
import numpy as np
import pdb

def col_fitness(column):
    array_len = len(column)
    array1=[]
    array2=[]
    x1 = []
    x2 = []
    xs = [0,2,4,6]
    for i in range(array_len):
        if column[i] == -1:
            continue
        if i%2 == 0:
            array1.append(column[i])
            x1.append(xs[i//2])
        else:
            array2.append(column[i])
            x2.append(xs[i//2])
        
    xs = [x1,x2]
    for i,x in enumerate(xs):
        xs[i] = np.array(xs[i])
        xs[i] = xs[i][:,np.newaxis]
    arrays = [array1,array2]
    fitness = []
    for i,array in enumerate(arrays):
        if 'NULL' in array:
            fitness.append('NULL')
        else:
            first_point = array[0]
            ys = []
            for point in array:
                y = np.log10((first_point/point - first_point)/(1-first_point))
                ys.append(y)
            ys = np.array(ys)
            (a, _, _, _) = np.linalg.lstsq(xs[i], ys)
            fitness.append(np.log2(1/np.power(10,a[0])))
    return fitness
    

def main():
    data_file = '/Users/lijiang/Downloads/clay_original_results/clay_results_summary.xlsx'
    data = pd.read_excel(data_file,sheet_name=3,index_col=False)
    rows,cols = data.shape
    a = []
    d = []
    for col in range(cols):
        column = data.iloc[:,col]
        fitness_1,fitness_2 = col_fitness(column)
        a.append(fitness_1)
        d.append(fitness_2)
    for i in a:
        print(i)
    for i in d:
        print(i)

    
    
if __name__ == '__main__':
    main()
# data_file = '/Users/lijiang/Downloads/11-07-2019_LL_RCAN-1_adjusted.xlsx'
# data = pd.read_excel(data_file,sheet_name=2,index_col=0,usecols=range(5),nrows = 4)

#data.head()

# fitness = []
# 
# 
# for index, row in data.iterrows():
#     first_point = row[1]
#     xs = []
#     ys = []
#     for j, point in row.iteritems():
#         x = j*2
#         y = np.log10((first_point/point - first_point)/(1-first_point))
#         xs.append(x)
#         ys.append(y)
#     xs = np.array(xs)
#     xs = xs[:,np.newaxis]
#     ys = np.array(ys)
#     #pdb.set_trace()
#     (a, _, _, _) = np.linalg.lstsq(xs, ys)
#     fitness.append(np.log2(1/np.power(10,a[0])))
# pdb.set_trace()
# fitness = np.array(fitness)
# data['fitness'] = fitness