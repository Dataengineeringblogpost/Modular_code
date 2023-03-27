"""
Objective:-

"""
from my_modular_code.exception import InsuranceException
import os
import sys
from datetime import datetime
from my_modular_code.logger import logging

File_name="insureance.csv"
Train_File_Name="train.csv"
Test_File_Name="test.csv"
TRANSFORMED_OBJECT_FILE_NAME="transformer.pkl"
TARGET_ENCODER_OBJECT_FILE_NAME = "target_encoder.pkl"
MODEL_FILE_NAME = "model.pkl"
class TrainingPipelineConfig:
    def __init__(self) :
        try:
            self.artifact_dir=os.path.join(os.getcwd(),"artifact",f"{datetime.now().strftime('%m$d%Y_%H%M%S')}")
        except Exception as e:
            raise InsuranceException(e,sys)
class DataIngestionConfig:
    def __init__(self,training_pipeline_config:TrainingPipelineConfig):
        try:
            self.database_name = "INSURANNCE"
            self.collection_name = "INSURANCE_PROJECT"
            self.data_ingestion_dir = os.path.join(training_pipeline_config.artifact_dir,"data_ingestion")
            self.feature_store_file_name = os.path.join(self.data_ingestion_dir,"feature_store",File_name)
            self.train_file_path=os.path.join(self.data_ingestion_dir,"dataset",Train_File_Name)
            self.test_file_path=os.path.join(self.data_ingestion_dir,"dataset",Test_File_Name)
            self.test_size=0.2
        
        except Exception as e:
            raise InsuranceException(e,sys)
        
    
    def to_dict(self):
        try:
            return self.__dict__
        except Exception as e:
            raise InsuranceException(e,sys)
    

class DataValidationConfig:
    def __init__(self,training_pipeline_config:TrainingPipelineConfig):

        self.data_validation_dir=os.path.join(training_pipeline_config.artifact_dir,"data_validation")
        self.report_file_path=os.path.join(self.data_validation_dir, "report.yaml")
        self.missingthreshold:float = 0.2
        # self.base_file_path=os.path.join("insureance.csv")
        self.base_file_path=os.path.join("insurance.csv")
        

class DataTransformationConfig:
    def __init__(self,training_pipeline_config:TrainingPipelineConfig):
        
        #Creating a Folder name 'data_transformation'  in artifact folder
        self.data_transformation_dir=os.path.join(training_pipeline_config.artifact_dir,"data_transformation")
        #Storing the transformed file object in a directory 
        
        self.transform_object_path=os.path.join(self.data_transformation_dir,"transformer",TRANSFORMED_OBJECT_FILE_NAME)
        #Storing the training transformed file object in a directory in tar file
       
        self.transform_object_train_path=os.path.join(self.data_transformation_dir,"transformed",Train_File_Name.replace("csv","npz"))
        #Storing the testing transformed file object in a directory in tar file
        self.transform_object_test_path=os.path.join(self.data_transformation_dir,"transformed",Test_File_Name.replace("csv","npz"))
        self.target_encoder_path = os.path.join(self.data_transformation_dir,"target_encoder",TARGET_ENCODER_OBJECT_FILE_NAME)

class ModelTrainingConfig:
    def __init__(self,training_pipeline_config:TrainingPipelineConfig):
        #Creating a Folder name 'model_trainer'  in artifact folder
        self.model_trainer_dir=os.path.join(training_pipeline_config.artifact_dir,"model_trainer")
        #Creating a File inside the model dir to save the model Object
        self.model_path=os.path.join(self.model_trainer_dir,"model",MODEL_FILE_NAME)
        #Setting a threshold for the Model Accurcy
        self.expected_accurcy  = 0.6
        #Setting  threshold for overfitting
        self.overfitting_threshold = 0.3

class ModelEvaluationConfig:
    def __init__(self,training_pipeline_config:TrainingPipelineConfig):
        self.change_threshold = 0.01
