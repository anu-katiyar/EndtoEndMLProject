import os, sys
from datetime import datetime
from src.exception import CustomException
from src.logger import logging
import pandas as pd
from sklearn.model_selection import train_test_split
from dataclasses import dataclass

@dataclass  
class DataIngestionConfig:
    timestamp = datetime.now().strftime("%m_%d_%Y_%H_%M_%S")
    feature_store_file_path = os.path.join("artifacts",timestamp,'stud.csv')
    train_data_file_path = os.path.join("artifacts",timestamp,'stud_train.csv')
    test_data_file_path = os.path.join("artifacts",timestamp,'stud_test.csv')

@dataclass
class DataIngestionArtifact:
    train_file_path:str
    test_file_path:str

raw_data_path ='notebook\data\stud.csv'
class DataIngestion:
    def __init__(self):
        self.data_ingestion_config = DataIngestionConfig()

    def initiate_data_ingestion(self) -> DataIngestionArtifact:
        logging.info("Data Ingestion initiated")
        try:
            # create feature store folder and store raw data
            logging.info("Data Ingestion: Read dataset as dataframe")
            feature_dirpath = os.path.dirname(self.data_ingestion_config.feature_store_file_path)
            os.makedirs(feature_dirpath, exist_ok=True)

            data = pd.read_csv(raw_data_path)

            data.to_csv(self.data_ingestion_config.feature_store_file_path, header=False, index=False)
            logging.info("Data Ingestion: Train Test data split initialized")
            train_data, test_data = train_test_split(data, test_size=0.3, random_state=42)

            # Export train and test data to CSV file and store under artifactfolder

            train_data.to_csv(self.data_ingestion_config.train_data_file_path, header=False, index=False)
            test_data.to_csv(self.data_ingestion_config.test_data_file_path, header=False, index=False)

            logging.info("Data Ingestion : Train and Test split of data completed successfully")
            data_ingestion_artifact = DataIngestionArtifact(self.data_ingestion_config.train_data_file_path,self.data_ingestion_config.test_data_file_path)
            
            return data_ingestion_artifact
        except Exception as e:
            logging.info("Data Ingestion failed to initiate")
            raise CustomException(e,sys)


if __name__ =='__main__':
    obj = DataIngestion()
    obj.initiate_data_ingestion()