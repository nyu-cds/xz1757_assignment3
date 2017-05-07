from pyspark import SparkContext
from operator import mul


sc = SparkContext("local", "product")

# create an RDD comprising all numbers from 1 to 1000
nums = sc.parallelize(range(1, 1001))

# calculates the product of all the numbers from 1 to 1000
product_result = nums.fold(1, mul)

print(product_result)
