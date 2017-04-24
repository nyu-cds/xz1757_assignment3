# This is a testing script.

import numpy as np
import unittest
from mpi4py import MPI
from parallel_sorter import *

# initialize the communicators
comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

# set up unittest test framework
class TestSplit(unittest.TestCase):

	def set(self):
		pass

	def test_split(self): 
		'''
		testing if split function correct split data to different slices
		'''
		test1 = split_data([3,5,7,4,6,7,11,9,2,8,3,2], 4)
		valid1 = [[2,2], [3,5,4,3], [7,6,7,8], [11, 9]] # true answer
		self.assertEqual(test1,valid1)

		test2 = split_data([1,2,3,4,5], 5)
		valid2 = [[1], [2], [3], [4],[5]] # true answer
		self.assertEqual(test2,valid2)

	def test_parallel_sort(self):
		'''
		testing if parallel_sort function sort the unsorted data in parallel
		'''
		sorted_data = parallel_sort()
		if rank == 0:
			test1 = np.asarray(sorted_data)
			valid1 = np.asarray(sorted(sorted_data)) # true answer
			self.assertTrue(test1.all() == valid1.all())
		else:
			self.assertEqual(sorted_data, None)

if __name__ == '__main__':
	unittest.main()


