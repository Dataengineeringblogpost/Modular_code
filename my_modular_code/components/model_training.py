from my_modular_code.entity import artifact_entity,config_entity
import os,sys
from my_modular_code.logger import logging
from my_modular_code.exception import InsuranceException
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import RobustScaler
import pandas as pd
import numpy as np
from my_modular_code import utils
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
"""
model define & Trainer
80% accuracy running
65 , 68,60 acc for new model
if the model has an accuracy of 70 and above then only wee would accept it or Reject
Checking foroverfitting and underfitting
"""
class ModelTrainer:
    """
    model_trainer_config:- This will have all the variable for model training like threshold where to store the model path and stuff
    data_transformation_artifact:- Here we have Stored the Transformed data ready for model Creation
    """
    
    
    def __init__(self,model_trainer_config : config_entity.ModelTrainingConfig,data_transformation_artifact : artifact_entity.DataTransformationArtifact):
        try:
            self.model_trainer_config = model_trainer_config
            self.data_transformation_artifact = data_transformation_artifact

        except Exception as e:
            raise InsuranceException(e,sys)
    
    """
    Creating a model trainer object - Similar Linear Regression
    x1 , x2 , x3  = input data
    y = Output data
    """
    def train_model(self,x,y):
        try:
            lr = LinearRegression()
            lr.fit(x,y)
            return lr

        except Exception as e:
            raise InsuranceException(e,sys)
    
    def intiate_model_trainer(self,):
        try:
            #Loading train and test data
            train_arr = utils.load_numpy_array_date(file_path=self.data_transformation_artifact.trasform_train_path)
            test_arr = utils.load_numpy_array_date(file_path=self.data_transformation_artifact.trasform_test_path)

            #Sepate x and y for training and testing
            x_train , y_train = train_arr[:, :-1] , train_arr[: , -1]

            x_test , y_test = test_arr[: , :-1] , test_arr[: , -1]
            print(x_train)

            #Create a simple Linear Algorithium
            model = self.train_model(x_train ,y_train)
            
            #Predict the data for training data
            yhat_train = model.predict(x_train)
            r2_train_score = r2_score(y_true= y_train , y_pred = yhat_train )
            
            #Predict the data for testing data
            yhat_test = model.predict(x_test)
            r2_test_score = r2_score(y_true= y_test , y_pred = yhat_test )

            if r2_test_score  < self.model_trainer_config.expected_accurcy:
                raise Exception(f"""Model is not good as it is not able to give excepted 
                                acuracy: {self.model_trainer_config.expected_accurcy} : model actual score {r2_test_score}""")
            
            diff = abs(r2_train_score-r2_test_score)

            if diff > self.model_trainer_config.overfitting_threshold:
                raise Exception(f"""
                Model is Overftiing {diff} is more than overfitting Threshold  {self.model_trainer_config.overfitting_threshold}
                """)
            
            utils.save_object(file_path=self.model_trainer_config.model_path,obj = model)
            
            model_trainer_artifact = artifact_entity.ModelTrainerArtifact(model_path=self.model_trainer_config.model_path,
                                                                        r2_train_score=r2_train_score,r2_test_score=r2_test_score  )
            return model_trainer_artifact
        
        except Exception as e:
            raise InsuranceException(e,sys)