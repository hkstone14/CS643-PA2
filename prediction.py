import sys

from pyspark.ml import PipelineModel
from pyspark.ml.evaluation import MulticlassClassificationEvaluator
from pyspark.sql.functions import round
from pyspark.sql import *

VALIDATION_DATASET = "ValidationDataset.csv"


if __name__ == '__main__':
    spark = SparkSession\
        .builder\
        .appName("WinePredictionMLModel")\
        .getOrCreate()

    dataset = sys.argv[-1] if len(sys.argv) > 1 else VALIDATION_DATASET

    data_frame = spark.read.format("csv").option("header", "true").option("delimiter", ";")\
        .option("inferSchema", "true")\
        .load(dataset)

    data_frame = data_frame.withColumnRenamed('""""quality"""""', "quality")

    pipeline = PipelineModel.load("ta222-njit-spark-ml-model")

    predictions = pipeline.transform(data_frame)

    predictions = predictions.withColumn("prediction",
                                         round(predictions["prediction"]))

    f1_evaluator = MulticlassClassificationEvaluator(labelCol="quality", predictionCol="prediction",
                                                     metricName="f1")

    f1_score = f1_evaluator.evaluate(predictions)

    print(f"F1 Score is: {f1_score*100}%")
