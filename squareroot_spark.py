from pyspark import SparkContext
from operator import add
import numpy as np


sc = SparkContext("local", "average square root")

# create an RDD comprising all numbers from 1 to 1000
nums = sc.parallelize(range(1, 1001))

# map each number to square root and get the mean
avg_sqrt = nums.map(lambda x: np.sqrt(x)).fold(0, add) / nums.count()

print(avg_sqrt)