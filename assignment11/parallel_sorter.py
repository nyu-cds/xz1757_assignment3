# This program is using MPI, which can sort the data with numbers of processes. 

from mpi4py import MPI 
import numpy as np 

# initialize the communicators 
comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()


def input_length():
	'''
	user input the length of the unsorted data
	'''
	input_check = False
	while input_check == False:
		try:
			user_input = int(input('Input the length of unsorted data set: '))
		except ValueError: # if not integer, value error 
			print('Input must be integer')
			continue
		if user_input <= 1: # lenght of unsorted data should greater than 2
			print('Length of data set should greater than 2')
			continue
		input_check = True

	return user_input

def split_data(data, num_slice):
	'''
	Args:
		data: unsorted data 
        num_slice: number slice you want to split the data, which should consistent with number of processes.
    Returns:
        slice_list: list of list with different range of data
	'''
	bins_data = np.arange(max(data)+1) 
	bins_slice = np.array_split(bins_data, num_slice) # split bins
	slice_list = []
	for i in range(num_slice):
		slice_list.append(list(filter(lambda x: x in bins_slice[i], data))) # filter the data which contains in each bins
	return slice_list

def parallel_sort():
	'''
    Returns:
        sorted_data: when rank is root rank, return list of sorted data
	'''
	if rank == 0:
		length= input_length() # input length of the data
		num_bins = size # number of bins is consistent with size of communicators
		unsorted_data = np.random.randint(low=0, high=length, size=length) # generate random data
		print ('Initial unsorted data is:', unsorted_data)
		slice_list = split_data(unsorted_data, num_bins)
	else:
		slice_list = None

	piece_data = comm.scatter(slice_list, root=0) # scatter piece data to each process
	print('Process {} received piece {} \n'.format(rank, piece_data))
	sorted_piece = comm.gather(np.sort(piece_data), root=0) # process 0 gathers all sorted pieces

	sorted_data = []
	if rank == 0:
		sorted_data = np.concatenate(sorted_piece) # concatenate all orted pieces
		print('Final sorted data is:', sorted_data)
		return sorted_data

if __name__ =='__main__':
	result = parallel_sort()
	




	



