import math

def split_array(arr, splits):
    step = math.ceil(len(arr) / splits)

    return_array = []

    for i in range(0, len(arr), step):
        return_array.append(arr[i:i+step])

    while(len(return_array) < splits):
        return_array.append([])
    
    return return_array