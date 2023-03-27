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
from my_modular_code.predictor import ModelResolver
class ModelEvaluation:
    def __init__(self,model_eval_config : config_entity.ModelTrainingConfig,
                 data_ingestion_artifact : artifact_entity.DataIngestionArtifact,
                 data_transformation_artifact : artifact_entity.DataTransformationArtifact,
                 model_training_artifact : artifact_entity.ModelTrainerArtifact):
        try:
            self.model_eval_config = model_eval_config
            self.data_ingestion_artifact = data_ingestion_artifact
            self.data_transformation_artifact = data_transformation_artifact
            self.model_training_artifact = model_training_artifact
            self.model_resolver = ModelResolver()
        except Exception as e:
            raise InsuranceException(e,sys)
    
    def intiate_model_evaluation(self)->artifact_entity.ModelEvaluationArtifact:
        try:
            latest_dir_path = self.model_resolver.get_latest_dir_path()
            if latest_dir_path==None:
                model_eval_artifact = artifact_entity.ModelEvaluationArtifact(is_model_accepted=True,improved_accurcy=None)
                
                return  model_eval_artifact
        except Exception as e:
            raise InsuranceException(e,sys)