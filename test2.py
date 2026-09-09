def quick_sort(arr):
    if len(arr) <=1:
        return arr
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quick_sort(left) + middle + quick_sort(right)

arr = [i for i in range(10000, 0, -1)]
import time
start_time = time.time()
quick_sort(arr)
print(f"temps avec quick sort: {time.time() - start_time:.6f} secondes")

# start_time = time.time()
# arr.sort()
# print(f"temps avec sort: {time.time() - start_time:.6f} secondes")


def selection_sort(liste):
    n = len(arr)
    for i in range(n):
        min_idx = i
        for j in range(i + 1, n):
            if arr[j] < arr[min_idx]:
                min_idx = j
        arr[i], arr[min_idx] = arr[min_idx], arr[i]
    return arr

import time 
arr = [i for i in range(10000, 0, -1)]
start_time = time.time()
selection_sort(arr)
print(f"temps avec selection sort: {time.time() - start_time:.6f} secondes")
        
        

    
            
