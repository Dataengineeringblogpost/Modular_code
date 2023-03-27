from my_modular_code.logger import logging
from my_modular_code.exception import InsuranceException
import os , sys
from my_modular_code.utils import get_colllection_as_dataframe
from my_modular_code.entity.config_entity import DataIngestionConfig
from my_modular_code.entity import config_entity
from my_modular_code.components.data_ingestion import DataIngestion
from my_modular_code.components.data_validation import DataValidation
from my_modular_code.components.data_transformation import DataTransformation
from my_modular_code.components.model_training import ModelTrainer
from my_modular_code.components.model_evaluation import ModelEvaluation
"""

This is a basic main file with basic exception handling 

"""

def test_logger_and_expetion():
    try:
        
        logging.info("Starting the test logger")
        result=3/'a'
        
        # logging.info("Ending point")
    except Exception as e:
        logging.debug(str(e))
        """
        e:-Exception
        sys:-System info where you get information of the exception
        """
        raise InsuranceException(e,sys)
if __name__=="__main__":
    try :
        DATABASE_NAME="INSURANNCE"
        COLLECTION_NAME="INSURANCE_PROJECT"
        training_pipeline_config=config_entity.TrainingPipelineConfig()
        data_ingestion_config = config_entity.DataIngestionConfig(training_pipeline_config)
        print(data_ingestion_config.to_dict())
        data_ingestion=DataIngestion(data_ingestion_config)
        data_ingestion_artifact=data_ingestion.intitate_data_ingestion()
        #Data Validation
        data_validation_config=config_entity.DataValidationConfig(training_pipeline_config)
        
        data_validation=DataValidation(data_validation_config,data_ingestion_artifact)
        data_validation_artifact=data_validation.data_initiate_data_Validation()
        #Data Transformation
        
        data_transformation_config = config_entity.DataTransformationConfig(training_pipeline_config
                                                                       )
        print(data_transformation_config)
        
        data_transformation=DataTransformation(data_transformation_config,data_ingestion_artifact)
        data_transformation_artifact=data_transformation.intiate_data_transformation()

        # Model Training
        model_trainer_config = config_entity.ModelTrainingConfig(training_pipeline_config=training_pipeline_config)
        model_trainer = ModelTrainer(model_trainer_config = model_trainer_config ,
                                     data_transformation_artifact=data_transformation_artifact)
        model_trainer_artifact = model_trainer.intiate_model_trainer()

        #Model Evaluation
        model_eval_config = config_entity.ModelEvaluationConfig(training_pipeline_config=training_pipeline_config)
        model_eval = ModelEvaluation(model_eval_config=model_eval_config,
                                     data_ingestion_artifact=data_ingestion_artifact,
                                     data_transformation_artifact=data_transformation_artifact,
                                     model_training_artifact=model_trainer_artifact)
        model_eval_artifact= model_eval.intiate_model_evaluation()
        


    except Exception as e:
        logging.debug(str(e))
        print("Error occoured")