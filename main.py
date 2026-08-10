from dynaconf import Dynaconf
from pyspark.sql import SparkSession
from pyspark.sql.functions import udf, call_udf
from pyspark.sql.types import StringType
from urllib.request import urlopen, Request

settings = Dynaconf(settings_files=['settings.yml'], environments=True)

# 0. Initialize Spark Session
spark = SparkSession.builder \
    .appName('StructuredNetworkWordCount') \
    .config(map=settings.get('spark_config', {})) \
    .getOrCreate()
spark.sparkContext.setLogLevel('ERROR')


# 1. Create and register the UDF, needs to be done after 0. if using @udf
# https://www.databricks.com/blog/introducing-arrow-udfs-pyspark-faster-leaner-replacement-pandas-udfs
@udf(returnType=StringType())  # Assumes spark.sql.execution.pythonUDF.arrow.enabled==true
# @udf(returnType=StringType(), useArrow=True)  # Explicitly set it
def call_some_url(url):
    """
    Call some url, horribly slow when used in a Spark Streaming job

    :param url: The url to call
    :return: Response of the call
    """
    return urlopen(Request(
        url=url,
        headers={'User-Agent': 'curl/7.54.1'}
    )).read().decode('utf-8').strip()


# Register UDF
spark.udf.register('call_some_url', call_some_url)

# 2. Create DataFrame representing the stream of incoming lines from port 9999
lines = spark.readStream \
    .format('socket') \
    .option('host', 'localhost') \
    .option('port', 9999) \
    .load()

# 3. Transform data: Call the url read from the socket
responses = lines.select(call_udf('call_some_url', 'value').alias('response'))

# 4. Generate running response count
response_counts = responses.groupBy('response').count()

# 5. Start running the query that prints the running counts to the console
# https://spark.apache.org/docs/latest/streaming/getting-started.html
query = response_counts.writeStream \
    .outputMode('complete') \
    .format('console') \
    .start()

query.awaitTermination()
