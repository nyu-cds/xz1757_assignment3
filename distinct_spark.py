from pyspark import SparkContext
from operator import add # Required for reduceByKey
import re

# remove any non-words and split lines into separate words
# finally, convert all words to lowercase
def splitter(line):
    line = re.sub(r'^\W+|\W+$', '', line)
    return map(str.lower, re.split(r'\W+', line))

if __name__ == '__main__':
	sc = SparkContext("local", "distinct words counts")
	
	text = sc.textFile('pg2701.txt')
	words = text.flatMap(splitter)
	words_mapped = words.map(lambda x: (x,1))

	# count the number of distince words
	distinct_words_counts = words_mapped.keys().distinct().count()
	print(distinct_words_counts)