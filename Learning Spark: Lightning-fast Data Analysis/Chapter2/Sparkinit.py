from pyspark import  SparkConf, SparkContext

conf = SparkConf().setMaster("local").setAppName("my app")

sc = SparkContext(conf= conf)

