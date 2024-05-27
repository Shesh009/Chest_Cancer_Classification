from cnnClassifier.pipeline.stage_04_model_evaluation import ModelEvaluationPipeline
from src.cnnClassifier import logger
from src.cnnClassifier.pipeline.stage_01_data_ingestion import DataIngestionTrainingPipeline
from src.cnnClassifier.pipeline.stage_02_prepare_base_model import PrepareBaseModelTrainingPipeline
from src.cnnClassifier.pipeline.stage_03_model_trainer import ModelTrainingPipeline

logger.info("New Logging Started")

STAGE_NAME="Data Ingestion Stage"

try:
    logger.info(f">>>> stage {STAGE_NAME} started <<<<")
    obj=DataIngestionTrainingPipeline()
    obj.main()
    logger.info(f">>>> stage {STAGE_NAME} completed <<<<")
except Exception as e:
        logger.exception(e)
        raise e

STAGE_NAME="Prepare Base Model"

try:
        logger.info(f">>>> stage {STAGE_NAME} started <<<<")
        obj=PrepareBaseModelTrainingPipeline()
        obj.main()
        logger.info(f">>>> stage {STAGE_NAME} completed <<<<")
except Exception as e:
        logger.exception(e)
        raise e

STAGE_NAME="Training"

try:
        logger.info(f">>>> stage {STAGE_NAME} started <<<<")
        obj=ModelTrainingPipeline()
        obj.main()
        logger.info(f">>>> stage {STAGE_NAME} completed <<<<")
except Exception as e:
        logger.exception(e)
        raise e

STAGE_NAME="Model Evaluation"

try:
        logger.info(f">>>> stage {STAGE_NAME} started <<<<")
        obj=ModelEvaluationPipeline()
        obj.main()
        logger.info(f">>>> stage {STAGE_NAME} completed <<<<")
except Exception as e:
        logger.exception(e)
        raise e

logger.info("Logging Completed")