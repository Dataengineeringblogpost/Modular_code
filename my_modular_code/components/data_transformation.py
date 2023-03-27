"""
Objective:-
Missing value imputation
Outlier Handling
Handling Imbalanced Dataset
Converting Categorical to Numerical columns

"""
from my_modular_code.entity import artifact_entity,config_entity
import os,sys
from my_modular_code.logger import logging
from my_modular_code.exception import InsuranceException
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import RobustScaler
import pandas as pd
import numpy as np
from my_modular_code.logger import logging
from sklearn.preprocessing import LabelEncoder
from my_modular_code import utils
from my_modular_code.config import TARGET_COLUMN
"""
Missing values impute
Outlier handling
Imbalanced data handling
Convert Categorical data into numerical data
"""

class DataTransformation:
    def __init__(self,data_transformation_config:config_entity.DataTransformationConfig,data_ingestion_artifact:artifact_entity.DataIngestionArtifact):
        try:
            self.data_transformation_config=data_transformation_config
            self.data_ingestion_artifact=data_ingestion_artifact
        except Exception as e:
            raise InsuranceException(e,sys)
        

    """
    Objective:- here we are creating a pipeline in the pipeline
      we are using Simple imputer to fill missing value
      we use Robust scaler we use to scale the values in and also remove the outliers
      """

    @classmethod
    def get_data_transformer_object(cls)->Pipeline:
        try:
            #Creating a Simple imputer object
            simple_imputer=SimpleImputer(strategy="constant",fill_value=0)

            #Creating a Robust scalar
            robust_scalar=RobustScaler()
            pipeline=Pipeline(
                steps=[ ("Imputer",simple_imputer),
                ("RobustScalar",robust_scalar)
                ]
            )
            return pipeline

        except Exception as e:
            raise InsuranceException(e,sys)
        
    """
    Objective:- in this function we are going to read the csv file
    seprate x and y for train and test dataset
    convert categorical to numerical
    impute missing value scale the values and remove outlier using pipeline
    concat x and y together

    """
    def intiate_data_transformation(self,)->artifact_entity.DataIngestionArtifact:
        try:
            logging.info("Starting Data Transformation")
            logging.info("Creating the train and test Dataframe")
            train_df=pd.read_csv(self.data_ingestion_artifact.train_file_path)
            test_df=pd.read_csv(self.data_ingestion_artifact.test_file_path)
            logging.info("Seprate X And Y Data for train and test")
            
            input_feature_train_df=train_df.drop(TARGET_COLUMN,axis=1)
            input_feature_test_df=test_df.drop(TARGET_COLUMN,axis=1)
            target_feature_train_df=train_df[TARGET_COLUMN]
            target_feature_test_df=test_df[TARGET_COLUMN]
            logging.info("Label encoding the categorical variable for converting all the column to the numerical")
            label_encoder=LabelEncoder()
            #Fit data
            target_feature_train_arr=target_feature_train_df.squeeze()
            target_feature_test_arr=target_feature_test_df.squeeze()
            for col in input_feature_train_df.columns:
                if input_feature_test_df[col].dtypes == "O":
                    input_feature_train_df[col]=label_encoder.fit_transform(input_feature_train_df[col])
                    input_feature_test_df[col]=label_encoder.fit_transform(input_feature_test_df[col])
                else:
                    input_feature_train_df[col]=input_feature_train_df[col]
                    input_feature_test_df[col]=input_feature_test_df[col]
            #Calling the above function
            transformation_pipeline=DataTransformation.get_data_transformer_object()
            logging.info("Imputing the missing values and dealing with outliers")
            transformation_pipeline.fit(input_feature_train_df)
            input_feature_train_arr=transformation_pipeline.transform(input_feature_train_df)
            input_feature_test_arr=transformation_pipeline.transform(input_feature_test_df)
            
            #concat with x and y together
            train_arr=np.c_[input_feature_train_arr,target_feature_train_arr]
            test_arr=np.c_[input_feature_test_arr,target_feature_test_arr]

            utils.save_numpy_array_data(file_path=self.data_transformation_config.transform_object_train_path,array=train_arr)
            utils.save_numpy_array_data(file_path=self.data_transformation_config.transform_object_test_path,array=test_arr)
            utils.save_object(file_path=self.data_transformation_config.transform_object_path,obj=transformation_pipeline)
            utils.save_object(file_path=self.data_transformation_config.target_encoder_path,obj=label_encoder)
            data_transformation_artifact = artifact_entity.DataTransformationArtifact(
                trasform_object_path=self.data_transformation_config.transform_object_path,
               trasform_train_path=self.data_transformation_config.transform_object_train_path,
               trasform_test_path=self.data_transformation_config.transform_object_test_path
            )
            logging.info("Storing the output")
            logging.info("end of data transformation")
            return data_transformation_artifact



        except Exception as e:
            raise InsuranceException(e,sys)
        
        