# 
# A CUDA version to calculate the Mandelbrot set
# set up environment: export NUMBA_ENABLE_CUDASIM=1
#
from numba import cuda
import numpy as np
from pylab import imshow, show
import math

@cuda.jit(device=True)
def mandel(x, y, max_iters):
    '''
    Given the real and imaginary parts of a complex number,
    determine if it is a candidate for membership in the 
    Mandelbrot set given a fixed number of iterations.
    '''
    c = complex(x, y)
    z = 0.0j
    for i in range(max_iters):
        z = z*z + c
        if (z.real*z.real + z.imag*z.imag) >= 4:
            return i

    return max_iters

@cuda.jit
def compute_mandel(min_x, max_x, min_y, max_y, image, iters):
    '''
    This program to work on a GPU using CUDA.
    1. obtain the starting x and y coordinates 
    2. calculate the ending x and y coordinates 
    3. compute the mandel value for each element of the block
    '''
    ### YOUR CODE HERE
    height = image.shape[0]
    width = image.shape[1]

    pixel_size_y = (max_y - min_y) / height
    pixel_size_x = (max_x - min_x) / width
    
    # obtain the starting x and y coordinates 
    x_staring, y_staring = cuda.grid(2)  # x, y order is matter

    # calculate the ending x and y coordinates 
    y_ending = cuda.gridDim.y * cuda.blockDim.y 
    x_ending = cuda.gridDim.x * cuda.blockDim.x
    
    # compute the mandel value for each element of the block
    for x in range(x_staring, width, x_ending):
        real = min_x + x * pixel_size_x
        for y in range(y_staring, height, y_ending):
            imag = min_y + y * pixel_size_y
            image[y, x] = mandel(real, imag, iters)

if __name__ == '__main__':
    image = np.zeros((1024, 1536), dtype = np.uint8)
    blockdim = (32, 8)
    griddim = (32, 16)
    
    image_global_mem = cuda.to_device(image)
    compute_mandel[griddim, blockdim](-2.0, 1.0, -1.0, 1.0, image_global_mem, 20) 
    image_global_mem.copy_to_host()
    imshow(image)
    show()



