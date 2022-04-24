import sys

from pyspark.ml import Pipeline
from pyspark.ml.classification import RandomForestClassifier
from pyspark.ml.evaluation import MulticlassClassificationEvaluator
from pyspark.ml.feature import VectorAssembler
from pyspark.sql.functions import round
from pyspark.sql import *



TRAINING_DATASET = "TrainingDataset.csv"

if __name__ == '__main__':
    spark = SparkSession\
        .builder\
        .appName("WineTrainingMLModel")\
        .getOrCreate()

    dataset = sys.argv[-1] if len(sys.argv) > 1 else TRAINING_DATASET

    data_frame = spark.read.format("csv").option("header", "true").option("delimiter", ";")\
        .option("inferSchema", "true")\
        .load(dataset)

    data_frame = data_frame.withColumnRenamed('""""quality"""""', "quality")

    train_data, test_data = data_frame.randomSplit([0.8, 0.2])

    features_assembler = VectorAssembler(inputCols=data_frame.columns[:-1], outputCol="features")

    rf_classifier = RandomForestClassifier(labelCol="quality", featuresCol="features", maxDepth=5, maxBins=32,
                                           numTrees=64)

    pipeline = Pipeline(stages=[features_assembler, rf_classifier])

    model = pipeline.fit(train_data)

    predictions = model.transform(test_data)

    predictions = predictions.withColumn("prediction",
                                         round(predictions["prediction"]))

    f1_evaluator = MulticlassClassificationEvaluator(labelCol="quality", predictionCol="prediction",
                                                     metricName="f1")

    f1_score = f1_evaluator.evaluate(predictions)

    model.write().overwrite().save("ta222-njit-spark-ml-model")

    print(f"F1 Score is: {f1_score * 100}%")
