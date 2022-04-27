import h5py
import sys
import numpy as np

try:
    f = h5py.File(sys.argv[1])
    print(list(f))
except:
    print("Corrupted")

# a = np.linspace(0, 100, 100)
# b = np.linspace(100, 200, 100)
# h5f = h5py.File("test.hdf5", 'w')

# h5f.create_dataset("test123", data=a)
# h5f.create_dataset("test1234", data=b)