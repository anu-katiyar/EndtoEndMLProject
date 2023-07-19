
from src.exception import CustomException
from src.logger import logging
from datetime import datetime
from dataclasses import dataclass
from src.components.data_ingestion import DataIngestion, DataIngestionConfig, DataIngestionArtifact
from src.components.data_validation import DataValidation, DataValidationConfig, DataValidationArtifact
from src.components.data_transformation import DataTransformation, DataTransformationConfig, DataTransformationArtifact
from src.components.model_trainer import ModelTrainer, ModelTrainerConfig
from src.entity.entity_config import TrainingPipelineConfig

class TrainPipeline:
    is_pipeline_running: bool = False

    def __init__(self):
        self.train_pipeline_config = TrainingPipelineConfig()

    def runPipeline(self):
        
        self.is_pipeline_running = True
        data_ingestion_obj = DataIngestion()
        data_ingestion_artifact = data_ingestion_obj.initiate_data_ingestion()
        data_validation_config = DataValidationConfig()
        data_validation_obj = DataValidation(data_ingestion_artifact, self.train_pipeline_config,data_validation_config)
        data_validation_artifact = data_validation_obj.initiate_data_validation()
        data_transformation_config = DataTransformationConfig()
        data_transformation_artifact = DataTransformation(data_ingestion_artifact,data_transformation_config).initiate_data_transformation()
        model_trainer_config = ModelTrainerConfig()
        score = ModelTrainer(model_trainer_config, data_transformation_artifact).initiate_model_trainer()
        self.is_pipeline_running =False


if __name__ == '__main__':
    tp = TrainPipeline()
    tp.runPipeline()