from pyspark import pipelines as dp
from pyspark.sql.functions import *
from pyspark.sql.types import *

# Event Hubs configuration
EH_NAMESPACE                    = "stock-market-stream"
EH_NAME                         = "stock-data"


EH_CONN_STR = spark.conf.get("conn_str")

KAFKA_OPTIONS = {
  "kafka.bootstrap.servers"  : f"{EH_NAMESPACE}.servicebus.windows.net:9093",
  "subscribe"                : EH_NAME,
  "kafka.sasl.mechanism"     : "PLAIN",
  "kafka.security.protocol"  : "SASL_SSL",
  "kafka.sasl.jaas.config"   : f"kafkashaded.org.apache.kafka.common.security.plain.PlainLoginModule required username=\"$ConnectionString\" password=\"{EH_CONN_STR}\";",
  "kafka.request.timeout.ms" : 60000,
  "kafka.session.timeout.ms" : 60000,
  "maxOffsetsPerTrigger"     : 1000,
  "failOnDataLoss"           : "true",
  "startingOffsets"          : "earliest"
}
@dp.table()
def stock_market():
    df= spark.readStream.format("kafka")\
                .options(**KAFKA_OPTIONS)\
                .load()

    df= df.withColumn("values", (col("value").cast("string")))
            
    return df
