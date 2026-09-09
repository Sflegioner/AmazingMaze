liste1 = [i for i in range(1000000)]
def chercher_liste(val):
    return val in liste1

import time
start_time = time.time()
chercher_liste(999999)
print(f"temps avec liste: {time.time() - start_time:.6f} secondes")


ensemble1 = set(i for i in range(1000000))

def chercher_ensemble(val):
    return val in ensemble1

start_time = time.time()
chercher_ensemble(999999)
print(f"temps avec ensemble: {time.time() - start_time:.6f} secondes")


