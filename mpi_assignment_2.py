from mpi4py import MPI
import numpy as np


# obtains MPI.COMM_WORLD communicator
comm = MPI.COMM_WORLD
# rank of the process within the communicator
rank = comm.Get_rank()
# obtains the size of communicator
size = comm.Get_size()
# initialize num
num = np.ones(1)

if rank == 0:
	input_check = False
	# take a user input which is an integer less than 100
	while input_check == False:
		try:
			user_input = int(input('Input an integer less than 100: '))
		except ValueError: # if not integer, value error 
			print('Input must be integer')
			continue
		if user_input >= 100: # if input greater than 100, value error 
			print('Input must less than 100')
			continue
		input_check = True

	num = user_input * num
	comm.Send(num, dest = 1) # send result to process 1 
	comm.Recv(num, source = size - 1) # recieve result from last process
	result = num # save the recieve number as result
	print ("Result is %d" %result)

# if the process is the last rank
elif rank == size-1: 
	comm.Recv(num, source = rank - 1) # recieve result from last process 
	comm.Send(num, dest = 0) # send result to process 0 
# if process i ranks is between 0 and last ranks
else:
	comm.Recv(num, source = rank - 1) # recieve result from last process
	num = num * (rank+1) # process i sends the value to process i+1 which multiplies it by i+1
	comm.Send(num, dest = rank+1) # process i send result to next rank process 



