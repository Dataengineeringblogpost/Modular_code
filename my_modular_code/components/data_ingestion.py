import pandas as pd
import numpy as np
import os ,sys
from my_modular_code.entity import config_entity
from my_modular_code.entity import artifact_entity
from my_modular_code.exception import InsuranceException
from my_modular_code import utils
from my_modular_code.logger import logging
from sklearn.model_selection import train_test_split
# data divide:-train ,test and validaate
class DataIngestion:
    def __init__(self,data_ingestion_config):
        try:
            self.data_ingestion_config=data_ingestion_config
        except Exception as e:
            raise InsuranceException(e,sys)
    def intitate_data_ingestion(self)->artifact_entity.DataIngestionArtifact:
        try:
            logging.info(f"Export Collection data as pandas as DataFrame")
            df:pd.DataFrame = utils.get_colllection_as_dataframe(

                database_name=self.data_ingestion_config.database_name,
                collection_name=self.data_ingestion_config.collection_name
            )
            logging.info(f"Save data into future store")
            #Replace na with NAN
            df.replace(to_replace="na",value=np.NAN, inplace=True)
            feature_store_dir=os.path.dirname(self.data_ingestion_config.feature_store_file_name)
            os.makedirs(feature_store_dir,exist_ok=True)
            logging.info("Save df to feature store folder")
            df.to_csv(path_or_buf=self.data_ingestion_config.feature_store_file_name)
            train_df , test_df = train_test_split(df,test_size=self.data_ingestion_config.test_size,random_state=10)
            logging.info("Create dataset directory folder")
            dataset_dir=os.path.dirname(self.data_ingestion_config.train_file_path)
            os.makedirs(dataset_dir,exist_ok=True)
            logging.info("Save dataset to feature selection store")
            train_df.to_csv(path_or_buf=self.data_ingestion_config.train_file_path,index=False,header=True)
            test_df.to_csv(path_or_buf=self.data_ingestion_config.test_file_path,index=False,header=True)
            data_ingestion_artifact= artifact_entity.DataIngestionArtifact(
                feature_store_file_path=self.data_ingestion_config.feature_store_file_name,
                train_file_path=self.data_ingestion_config.train_file_path,
                test_file_path=self.data_ingestion_config.test_file_path
            )
            logging.info("END")
        except Exception as e:
            raise InsuranceException(e,sys)