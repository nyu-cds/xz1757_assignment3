from mpi4py import MPI

# obtains MPI.COMM_WORLD communicator
comm = MPI.COMM_WORLD
# rank of the process within the communicator
rank = comm.Get_rank()

# processes with odd rank print “Goodbye”
if rank % 2 == 0: # check if ranks is even
	print ("Hello from process %d" %rank)

# processes with even rank print “Hello”
if rank % 2 == 1: # check if rank is odd
	print ("Goodbye from process %d" %rank) 

