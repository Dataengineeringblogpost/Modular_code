"""
1)Data type
2)unwanted data finding
3)Data Cleaning
"""

import pandas as pd
from my_modular_code.entity import config_entity
from my_modular_code.entity import artifact_entity
from my_modular_code.exception import InsuranceException
from my_modular_code import utils
from typing import Optional
from my_modular_code.logger import logging
import sys,os
from scipy.stats import ks_2samp
from my_modular_code.config import TARGET_COLUMN
import numpy as np
import yaml
from  my_modular_code import utils


#Creating a classs DataValidation
class DataValidation:
    """
    Creating a constructor 
    data_validation_config:-we have stored the name of the database and collection the project dir training testing normal dataset file path and also small stuff like test_size here.
    data_validation_artifact:-Here we store the updated train test file path

    """
    def __init__(self,data_validation_config:config_entity.DataValidationConfig,data_validation_artifact:artifact_entity.DataIngestionArtifact):
        try:
            logging.info("Data Validation started")
            self.data_validation_config=data_validation_config        
            self.data_validation_artifact=data_validation_artifact
            self.validation_error=dict()
        except Exception as e:
            raise InsuranceException(e,sys)
        
    

    """This function is used to drop the columns with missing values if it crosses the threshold
    df :-normal dataframe ie the training and testing dataset
    report_key_name:-The key at which we have to store our output of the drop_missing_column as in which columns are left and stuff
    """
    def drop_missing_values_columns(self,df:pd.DataFrame,report_key_name):
        try:
            threshold=self.data_validation_config.missingthreshold
            print(df)
            null_report=df.isna().sum()/df.shape[0]
            logging.info("")
            drop_columns_name=null_report[null_report>threshold].index
            self.validation_error[report_key_name]=list(drop_columns_name)
            df.drop(list(drop_columns_name),axis=1,inplace=True)
            if len(df.columns)==0:
                return None
            else:
                return df
        
        except Exception as e:
            raise InsuranceException(e,sys)
        
    """
    objective:-here we are checking wheather the dataset has all the columns as the base dataset
    base_df:-main dataset
    current_df:-Which is mostly the  train and test dataset
    report_key_name:-Explained
    """
    def is_required_column_exists(self,base_df:pd.DataFrame,current_df:pd.DataFrame,report_key_name:str):
        try:
            base_colums=base_df
            current_colums=current_df

            missing_columns=[]
            for base_column in base_colums:
                if base_column not in current_colums:
                    logging.info(f"Columns:")
                    missing_columns.append(base_colums)
            if len(missing_columns)>0:
                self.validation_error[report_key_name]=missing_columns
                return False
            return True

        except Exception as e:
            raise InsuranceException(e,sys)
        
    """Here we are checking wheather two  columns follow the same distribution or not ie our base and train test dataset
    we are checking this basically to check wheather it has the same data or not
    """
    def data_drift(self,base_df:pd.DataFrame,current_df:pd.DataFrame,report_key_name):
        try:
            drift_report=dict()
            base_columns=base_df.columns
            current_colums=current_df.columns
            for base_column in base_columns:
                base_data,current_data=base_df[base_column],current_df[base_column]
                same_distribution=ks_2samp(base_data,current_data)
                if same_distribution.pvalue > 0.05:
                    drift_report[base_column]={
                        "pvalues":float(same_distribution.pvalue),
                        "same_distributor":True
                    }
                else:
                    drift_report[base_column]={
                        "pvalues":float(same_distribution.pvalue),
                        "same_distributor":False
                    }
            self.validation_error[report_key_name]=drift_report
        except Exception as e:
            raise InsuranceException(e,sys)
    
    """
    Here we are going to call all the function made above one by one lets see the flow:-
    first we reading the datasets
    we replace the na values to np.nan values
    we drop the missing columns having a spefic threshold
    same we do for the train and test dataset
    here we convert all the columns into float except the target columns(Function from utils)
    then we check whaeather the daaset has the same columns or not
    if all columns are same then we check wheather the distribution is same or not
    then we write all the data in our yaml  file
    

    """
    def data_initiate_data_Validation(self):
        try:
            # print(self.data_validation_config.base_file_path)
            base_df=pd.read_csv(self.data_validation_config.base_file_path)
            
            base_df=base_df.replace(to_replace="na",value=np.NAN)
           
            base_df=self.drop_missing_values_columns(df=base_df,report_key_name="missing_value_within_the_base_dataset")
            print(self.data_validation_artifact)
            print(self.data_validation_artifact.train_file_path)
            train_df=pd.read_csv(self.data_validation_artifact.train_file_path)
            print(train_df)
            train_df=self.drop_missing_values_columns(df=train_df,report_key_name="missing_value_within_the_train_dataset")
            
            test_df=pd.read_csv(self.data_validation_artifact.test_file_path)
            test_df=self.drop_missing_values_columns(df=test_df,report_key_name="missing_value_within_the_test_dataset")
            logging.info("test")
            print(test_df)
            exclude_column=[TARGET_COLUMN]
            base_df=utils.convert_column_float(df=base_df,exclude_columns=exclude_column)
            train_df=utils.convert_column_float(df=train_df,exclude_columns=exclude_column)
            test_df=utils.convert_column_float(df=test_df,exclude_columns=exclude_column)
            train_df_column_status=self.is_required_column_exists(base_df=base_df,current_df=train_df,report_key_name="missing_columns_within_train")
            test_df_column_status=self.is_required_column_exists(base_df=base_df,current_df=test_df,report_key_name="missing_columns_within_test")
            if train_df_column_status:
                self.data_drift(base_df=base_df,current_df=train_df,report_key_name="data_drift_within_train_dataset")            
            if test_df_column_status:
                self.data_drift(base_df=base_df,current_df=test_df,report_key_name="data_drift_within_test_dataset")
            utils.write_yaml_file(file_path=self.data_validation_config.report_file_path,data=self.validation_error)
            data_validation_artifact=artifact_entity.DataValidationArtifact(self.data_validation_config.report_file_path)
            return data_validation_artifact
        except Exception as e:
            raise InsuranceException(e,sys)