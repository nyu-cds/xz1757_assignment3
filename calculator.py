# -----------------------------------------------------------------------------
# calculator.py
# ----------------------------------------------------------------------------- 
'''
## Original ##
Timer unit: 1e-06 s
Total time: 3.35723 s
Line #      Hits         Time  Per Hit   % Time  Line Contents
==============================================================
    44                                           @profile
    45                                           def hypotenuse(x,y):
    46                                               """
    47                                               Return sqrt(x**2 + y**2) for two arrays, a and b.
    48                                               x and y must be two-dimensional arrays of the same shape.
    49                                               """
    50         1       857058 857058.0     25.5      xx = multiply(x,x)
    51         1       861610 861610.0     25.7      yy = multiply(y,y)
    52         1       865372 865372.0     25.8      zz = add(xx, yy)
    53         1       773190 773190.0     23.0      return sqrt(zz)

## Optimized ##
Total time: 0.023696 s
Line #      Hits         Time  Per Hit   % Time  Line Contents
==============================================================
    59                                           @profile
    60                                           def hypotenuse(x,y):
    61                                               """
    62                                               Return sqrt(x**2 + y**2) for two arrays, a and b.
    63                                               x and y must be two-dimensional arrays of the same shape.
    64                                               """
    65         1         5001   5001.0     21.1      xx = multiply(x,x)
    66         1         5474   5474.0     23.1      yy = multiply(y,y)
    67         1         5890   5890.0     24.9      zz = add(xx, yy)
    68         1         7331   7331.0     30.9      return sqrt(zz)
'''
'''
Relative Speedup = 141.67x
'''


import numpy as np

def add(x,y):
    """
    Add two arrays using a Python loop.
    x and y must be two-dimensional arrays of the same shape.
    """
    
    z = np.add(x,y)
    
    return z


def multiply(x,y):
    """
    Multiply two arrays using a Python loop.
    x and y must be two-dimensional arrays of the same shape.
    """
    
    z = np.multiply(x,y)

    return z

def sqrt(x):
    """
    Take the square root of the elements of an arrays using a Python loop.
    """
    z = np.sqrt(x)
    return z

@profile
def hypotenuse(x,y):
    """
    Return sqrt(x**2 + y**2) for two arrays, a and b.
    x and y must be two-dimensional arrays of the same shape.
    """
    xx = multiply(x,x)
    yy = multiply(y,y)
    zz = add(xx, yy)
    return sqrt(zz)