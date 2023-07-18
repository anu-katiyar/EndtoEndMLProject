import sys,os
import numpy as np
import pandas as pd
from datetime import datetime
from src.logger import logging
from src.exception import CustomException
from src.components.data_ingestion import DataIngestion, DataIngestionArtifact
from src.utils import read_yaml_file, save_object, save_numpy_array_data
from dataclasses import dataclass
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer

@dataclass
class DataTransformationConfig :
    timestamp = datetime.now().strftime("%m_%d_%Y_%H_%M_%S")
    transformed_object_file_path = os.path.join("artifacts", timestamp, "transformed", "StudPreprocessing.pkl")
    transformed_train_file_path = os.path.join("artifacts", timestamp ,"transformed","stud_train.npy")
    transformed_test_file_path= os.path.join("artifacts", timestamp,"transformed","stud_test.npy")

@dataclass
class DataTransformationArtifact :
    transformed_train_file_path: str
    transformed_test_file_path: str
    transformed_object_file_path: str

class DataTransformation:
    
    def __init__(self, data_ingestion_artifact:DataIngestionArtifact, 
                    data_transformation_config:DataTransformationConfig):
        try:
            self.data_ingestion_artifact = data_ingestion_artifact 
            self.data_transformation_config = data_transformation_config 
            self._schema = read_yaml_file("config\schema.yaml")
        except Exception as e:
            raise CustomException(e, sys)

    def get_transformed_data_object(self):
        try:  
            
            cat_columns = self._schema["categorical_columns"]
            num_columns =  self._schema["numerical_columns"]

            logging.info("Data Transformation: Read categorical features")
            
            num_pipeline = Pipeline(
                steps=[
                    ('imputer', SimpleImputer(strategy ="median")),
                    ('scaler', StandardScaler(with_mean=False)),
                ]
            )
            
            cat_pipeline = Pipeline(
                steps=[
                    ('imputer', SimpleImputer(strategy ="most_frequent")),
                    ('ohetransformer', OneHotEncoder()),
                    ('scaler', StandardScaler(with_mean=False))
                ]
            )

            preprocessor = ColumnTransformer(
                [
                    ('num_pipeline', num_pipeline,num_columns),
                    ('cat_pipeline', cat_pipeline, cat_columns)
                ]
            )
            return preprocessor
        except Exception as e:
         raise CustomException(e, sys)
        
    def initiate_data_transformation(self, ) -> DataTransformationArtifact:
        try:
            # read data from data ingestion artifact
            logging.info("Data Transformation:Reading data from data ingestion artifact")

            train_df = pd.read_csv(self.data_ingestion_artifact.train_file_path)
            test_df = pd.read_csv(self.data_ingestion_artifact.test_file_path)

            logging.info("Data Transformation:Reading data from data ingestion artifact completed successfully")

            preprocessor = self.get_transformed_data_object()
            logging.info("Data Transformation: Fetched Preprocessor object" )

            target_column = self._schema["target_column"]
          
            # get training data features - dependent and independent variables
            input_feature_train_df=train_df.drop(target_column,axis=1)
            target_feature_train_df=train_df[target_column]

            input_feature_test_df=test_df.drop(target_column,axis=1)
            target_feature_test_df=test_df[target_column]

            logging.info("Data Transformation: Applying preprocessor and transform dataframe")

            # get testing data features- dependent and independent variables
            transformed_train_data = preprocessor.fit_transform(input_feature_train_df)
            transformed_test_data = preprocessor.transform(input_feature_test_df)
            
            train_arr = np.c_[transformed_train_data, np.array(target_feature_train_df)]
            test_arr = np.c_[transformed_test_data, np.array(target_feature_test_df)]

            logging.info(f"Data Transformation: Saved Processed Data")

            save_numpy_array_data(self.data_transformation_config.transformed_train_file_path, train_arr)
            save_numpy_array_data(self.data_transformation_config.transformed_test_file_path, test_arr)
            save_object(file_path=self.data_transformation_config.transformed_object_file_path,obj=preprocessor)
            
            data_transform_artifact = DataTransformationArtifact(self.data_transformation_config.transformed_train_file_path,self.data_transformation_config.transformed_test_file_path,self.data_transformation_config.transformed_object_file_path)
            
            return data_transform_artifact
        except Exception as e:
            raise CustomException(e,sys)

if __name__ == "__main__":
    objdataIng=DataIngestion()
    data_ingest_artifact=objdataIng.initiate_data_ingestion()
    data_tranform_config = DataTransformationConfig()
    data_transform_obj = DataTransformation(data_ingest_artifact,data_tranform_config)
    data_transform_artifact=data_transform_obj.initiate_data_transformation()
   