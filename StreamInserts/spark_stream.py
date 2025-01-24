from logger import logger
from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col, udf
from pyspark.sql.types import StructType, StructField, StringType
from CassandraInitialization import CassandraInit
import uuid

class SparkStreaming:
    spark=None
    def __init__(self):
        try:
            self.spark = SparkSession.builder \
                .appName('SparkDataStreaming') \
                .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.4")\
                .config('spark.cassandra.connection.host', 'cassandra') \
                .config("spark.cassandra.connection.port", "9042")\
                .getOrCreate()

            # self.spark.sparkContext.setLogLevel("ERROR")
            logger.info("Spark connection created successfully!")
        except Exception as e:
            logger.error(f"Couldn't create the spark session due to exception {e}")

    def get_spark_connection(self):
        return self.spark


    def readStreamFromKafka(self):
        spark_df = None
        try:
            spark_df = self.spark.readStream \
                .format('kafka') \
                .option('kafka.bootstrap.servers', 'broker:29092') \
                .option('subscribe', 'users') \
                .option('startingOffsets', 'earliest') \
                .option('maxOffsetsPerTrigger', 100)\
                .load()
            logger.info("kafka dataframe created successfully")
        except Exception as e:
            logger.warning(f"kafka dataframe could not be created because: {e}")

        return spark_df

    def kafkaDfSchemaConstruct(self,df):
        schema = StructType([
            StructField("id", StringType(), False),
            StructField("first_name", StringType(), False),
            StructField("last_name", StringType(), False),
            StructField("gender", StringType(), False),
            StructField("address", StringType(), False),
            StructField("zipcode", StringType(), False),
            StructField("email", StringType(), False),
            StructField("username", StringType(), False),
            StructField("registered", StringType(), False),
            StructField("phone", StringType(), False),
            StructField("image", StringType(), False)
        ])

        if df is not None:

            df = df.selectExpr("CAST(value AS STRING)") \
                .select(from_json(col('value'), schema).alias('data')).select("data.*")

            uuid_udf = udf(lambda: str(uuid.uuid4()))

            df_with_id = df.withColumn("id", uuid_udf())

            df_columns_renamed = df_with_id.withColumnRenamed("zipcode", "post_code") \
                .withColumnRenamed("registered", "registered_date")\
                .withColumnRenamed("image","picture")
        return df_columns_renamed


if __name__ == "__main__":
    # create spark connection
    spark= SparkStreaming()
    spark_connection=spark.get_spark_connection()
    print(spark_connection)
    cassandra_load=None
    cassandra = CassandraInit()
    session = cassandra.getSession()
    if session is not None:
        cassandra.create_keyspace()
        cassandra.create_table()
    if spark_connection is not None:
        # connect to kafka with spark connection
        df = spark.readStreamFromKafka()
        df = spark.kafkaDfSchemaConstruct(df)
        logger.info("Streaming is being started...")
        if df is not None:
            cassandra_load = df.writeStream.format("org.apache.spark.sql.cassandra") \
                .option('checkpointLocation', '/tmp/checkpoint') \
                .option('keyspace', 'spark_streams') \
                .option('table', 'created_users') \
                .start()
            cassandra_load.awaitTermination()
            # df_console=df.writeStream \
            #     .format("console")  \
            #     .start()
            # df_console.awaitTermination()
