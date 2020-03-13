import itertools
import numpy as np

def lowest_std_comb(list_of_values, n):
    """
    When a list is inputted, returns the lowest std calculation of a combination of 3 items
    """
    list_of_std = []
    y = list(itertools.combinations(list_of_values, n))
    #print(y)
    y = [t for t in y if 0 not in t]
    for n in range (0,len(y)):
        x = np.std(y[n])
        list_of_std.append(x)
        #print(list_of_std)
    min_values = np.min(list_of_std)
    #print(min_values)
    index_std = list_of_std.index(min_values)
    #print(index_std)
    #print(y[index_std])
    return y[index_std]


#x = lowest_std_comb([8.1,4.6,7.8,19.5],3)

#print(x)
