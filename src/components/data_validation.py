from datetime import datetime
from dataclasses import dataclass
import os, sys
from src.components.data_ingestion import DataIngestion, DataIngestionArtifact
from src.utils import write_yaml_file
from src.entity.entity_config import TrainingPipelineConfig
from src.exception import CustomException
from src.logger import logging
import pandas as pd
from pandas import DataFrame
from scipy.stats import ks_2samp

@dataclass
class DataValidationConfig:
    valid_data_file_path = os.path.join("artifacts", "validation","ValidDataFile.csv")
    invalid_data_file_path = os.path.join("artifacts","validation","InValidDataFile.csv")
    drift_report_file_path = os.path.join("artifacts", "validation","driftreport.yaml")

@dataclass
class DataValidationArtifact:
    validation_status:bool
    valid_train_file_path:str
    valid_test_file_path:str
    invalid_train_file_path:str
    invalid_test_file_path:str
    drift_report_file_path:str


class DataValidation:
    def __init__(self, data_ingestion_artifact: DataIngestionArtifact, train_piplineConfig:TrainingPipelineConfig, data_validation_config: DataValidationConfig):
        self.data_ingestion_artifact = data_ingestion_artifact
        self.train_pipline_config = train_piplineConfig
        self.data_validation_config = data_validation_config
        timestamp = train_piplineConfig.timestamp
      

    def check_data_drift(self, basedf:DataFrame, currentdf:DataFrame, threshold = 0.5):
        status=True
        report ={}
        for column in basedf.columns:
            d1 = basedf[column]
            d2  = currentdf[column]
            is_same_dist = ks_2samp(d1,d2)
          
            if threshold<=is_same_dist.pvalue:
                is_found=False
            else:
                is_found = True 
                status=False
            report.update({column:{
                "p_value":float(is_same_dist.pvalue),
                "drift_status":is_found
                
                }})
        drift_report_file_path = self.data_validation_config.drift_report_file_path
            
        #Create directory
        dir_path = os.path.dirname(drift_report_file_path)
        os.makedirs(dir_path,exist_ok=True)
        write_yaml_file(file_path=drift_report_file_path,content=report,)
        return status

    def initiate_data_validation(self)-> DataValidationArtifact:
         # read data from data ingestion artifact
        logging.info("Data Validation:Reading data from data ingestion artifact")

        train_df = pd.read_csv(self.data_ingestion_artifact.train_file_path)
        test_df = pd.read_csv(self.data_ingestion_artifact.test_file_path)

        logging.info("Data Validation:Read data from data ingestion artifact")

        #check for data drift
        has_data_drift = self.check_data_drift(train_df, test_df)

        logging.info("Data Validation:Checking for data drift")

        data_validation_artifact = DataValidationArtifact(
                validation_status=True,
                valid_train_file_path=self.data_ingestion_artifact.train_file_path,
                valid_test_file_path=self.data_ingestion_artifact.test_file_path,
                invalid_train_file_path=None,
                invalid_test_file_path=None,
                drift_report_file_path=self.data_validation_config.drift_report_file_path,
            )

        return data_validation_artifact 