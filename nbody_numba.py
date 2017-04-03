"""
    N-body simulation.
    original script execution time: 1m47.509s
"""
'''
Version_numba script execution time: 0m25.287s
Version_numba with vec_deltas script execution time: 0m144s
Comparing with original version, Version_numba Relative Speedup (R): 5.81x
'''

from itertools import combinations
from numba import jit, int32, float64, int64, vectorize
import numpy as np
import itertools
import timeit


@vectorize([float64(float64, float64)])
def vec_deltas(a, b):
    return a-b


@jit('void(float64, float64[:,:,:], char[:,:], char[:], int32)')
def advance(dt, BODIES, key_pairs, body_names, iterations):
    '''
        advance the system one timestep
    '''
    for _ in range(iterations):

        for (body1, body2) in key_pairs:
            (a, v1, m1) = BODIES[body1]
            (b, v2, m2) = BODIES[body2]
            
            (dx, dy, dz) = vec_deltas(a,b)


            mag = dt * ((dx * dx + dy * dy + dz * dz) ** (-1.5))

            b1 = m1 * mag
            b2 = m2 * mag

            v1[0] -= dx * b2
            v1[1] -= dy * b2
            v1[2] -= dz * b2
            v2[0] += dx * b1
            v2[1] += dy * b1
            v2[2] += dz * b1

        for body in body_names:
            (r, [vx, vy, vz], m) = BODIES[body]
            r[0] += dt * vx
            r[1] += dt * vy
            r[2] += dt * vz

@jit('float64(float64[:,:,:], char[:,:], char[:], float64)')
def report_energy(BODIES, key_pairs, body_names, e):
    '''
        compute the energy and return it so that it can be printed
    '''
    for (body1, body2) in key_pairs:
        (c, v1, m1) = BODIES[body1]
        (d, v2, m2) = BODIES[body2]
        
        (dx, dy, dz) = vec_deltas(c,d)
        
        e -= (m1 * m2) / ((dx * dx + dy * dy + dz * dz) ** 0.5)
        
    for body in body_names:
        (r, [vx, vy, vz], m) = BODIES[body]
        e += m * (vx * vx + vy * vy + vz * vz) / 2.
        
    return e

@jit('void(int32, float64[:,:,:], char[:], float64, float64, float64)')
def offset_momentum(ref, BODIES, body_names, px=0.0, py=0.0, pz=0.0):
    '''
        ref is the body in the center of the system
        offset values from this reference
    '''
    for body in body_names:
        (r, [vx, vy, vz], m) = BODIES[body]
        px -= vx * m
        py -= vy * m
        pz -= vz * m
        
    (r, v, m) = ref
    v[0] = px / m
    v[1] = py / m
    v[2] = pz / m

@jit('void(int32, int32, int32)')
def nbody(loops, reference, iterations):
    '''
        nbody simulation
        loops - number of loops to run
        reference - body at center of system
        iterations - number of timesteps to advance
    '''

    key_pairs, body_names = find_pairs(BODIES)

    # Set up global state
    offset_momentum(BODIES[reference],BODIES, body_names)

    for _ in range(loops):
        advance(0.01, BODIES, key_pairs,body_names, iterations)
        print(report_energy(BODIES, key_pairs,body_names, e=0.0))

if __name__ == '__main__':
    
    def find_pairs(BODIES):
    key_pairs = set()
    for x in itertools.product(BODIES.keys(),BODIES.keys()):
        if x[1] != x[0]:
            key_pairs.add(x)
    key_pairs = set((a, b) if a <= b else (b, a) for a, b in key_pairs)
    body_names = BODIES.keys()
    return key_pairs, body_names
    
    PI = 3.14159265358979323
    SOLAR_MASS = 4 * PI * PI
    DAYS_PER_YEAR = 365.24

    BODIES = {
        'sun': ([0.0, 0.0, 0.0], [0.0, 0.0, 0.0], SOLAR_MASS),

        'jupiter': ([4.84143144246472090e+00,
                     -1.16032004402742839e+00,
                     -1.03622044471123109e-01],
                    [1.66007664274403694e-03 * DAYS_PER_YEAR,
                     7.69901118419740425e-03 * DAYS_PER_YEAR,
                     -6.90460016972063023e-05 * DAYS_PER_YEAR],
                    9.54791938424326609e-04 * SOLAR_MASS),

        'saturn': ([8.34336671824457987e+00,
                    4.12479856412430479e+00,
                    -4.03523417114321381e-01],
                   [-2.76742510726862411e-03 * DAYS_PER_YEAR,
                    4.99852801234917238e-03 * DAYS_PER_YEAR,
                    2.30417297573763929e-05 * DAYS_PER_YEAR],
                   2.85885980666130812e-04 * SOLAR_MASS),

        'uranus': ([1.28943695621391310e+01,
                    -1.51111514016986312e+01,
                    -2.23307578892655734e-01],
                   [2.96460137564761618e-03 * DAYS_PER_YEAR,
                    2.37847173959480950e-03 * DAYS_PER_YEAR,
                    -2.96589568540237556e-05 * DAYS_PER_YEAR],
                   4.36624404335156298e-05 * SOLAR_MASS),

        'neptune': ([1.53796971148509165e+01,
                     -2.59193146099879641e+01,
                     1.79258772950371181e-01],
                    [2.68067772490389322e-03 * DAYS_PER_YEAR,
                     1.62824170038242295e-03 * DAYS_PER_YEAR,
                     -9.51592254519715870e-05 * DAYS_PER_YEAR],
                    5.15138902046611451e-05 * SOLAR_MASS)}
