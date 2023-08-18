import pandas as pd
import numpy as np
import pdb

def col_fitness(column):
    #Get the number of rows in the column (Fitness)
    array_len = len(column)
    #Array to store treated
    array1=[]
    #Array to store untreated
    array2=[]
    x1 = []
    x2 = []
    xs = [0,2,4,6]
    #Iterate through the column doing nothing clearly helpful
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
        #For each element in XS, convert it to a numpy array and then convert it to a column vector
        xs[i] = np.array(xs[i])
        xs[i] = xs[i][:,np.newaxis]
    arrays = [array1,array2]
    fitness = []
    for i,array in enumerate(arrays):
        if 'NULL' in array:
            fitness.append('NULL')
        else:
            #Get allele frequency for the G1 in conditon (Array 1 - DMSO, Array 2 - Treated)
            first_point = array[0]
            ys = []
            #Iterate eq 2 from Zhao
            for point in array:
                y = np.log10((first_point/point - first_point)/(1-first_point))
                ys.append(y)
            ##Iterate eq 3 from Zhao
            #Convert ys to a numpy array
            ys = np.array(ys)
            #Get the least squares solution for the linear regression for one coulmn save as a tuple
            (a, _, _, _) = np.linalg.lstsq(xs[i], ys)
            #Use the first array form LSS regersiion to calculate fitness
            #Use the log2 of the inverse of 10 to the power of the first element of the tuple
            #Append the fitness to the fitness array
            fitness.append(np.log2(1/np.power(10,a[0])))
    return fitness
    
def process_sheet(data):
    rows, cols = data.shape
    a = []
    d = []
    for col in range(cols):
        column = data.iloc[:, col]
        fitness_1, fitness_2 = col_fitness(column)
        a.append(fitness_1)
        d.append(fitness_2)
    return pd.DataFrame({'Fitness_A': a, 'Fitness_D': d})

def main():
    data_file = 'claytest.xlsx'  #change file name for input
    output_file = 'fitness_output.xlsx'  # New Excel file for output
    data = pd.read_excel(data_file, sheet_name=1, index_col=False)
    rows, cols = data.shape
    a = []
    d = []
    for col in range(cols):
        column = data.iloc[:, col]
        fitness_1, fitness_2 = col_fitness(column)
        a.append(fitness_1)
        d.append(fitness_2)

    # Create a new DataFrame for the fitness values with swapped columns and headers
    fitness_data = pd.DataFrame({'Fitness_D': a, 'Fitness_A': d})  # Swapped columns and headers

    # Save the new DataFrame to an Excel file
    fitness_data.to_excel(output_file, index=False)

if __name__ == '__main__':
    main()