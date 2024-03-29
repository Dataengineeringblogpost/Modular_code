import pandas as pd
import numpy as np
import sys
import os
from my_modular_code.exception import InsuranceException
from my_modular_code.logger import logging
from my_modular_code.config import mongo_client
import yaml
import dill
"""
Objective:-Here we are converting the collection (Mongo DB Table) to a DataFrame
"""
def get_colllection_as_dataframe(database_name:str,collection_name:str):
    try:

        logging.info(f"Read data from the database{database_name} and collection {collection_name}")
        #Reading Table to DataFrame
        #Mongo client is kept in config ----> stored in env
        df=pd.DataFrame(mongo_client[database_name][collection_name].find())
        logging.info(f"find coloumns {df.columns}")

        #Droping the _id column if it exists 
        if "_id" in df.columns:
            logging.info(f"Dropping columns :_id")
            df=df.drop("_id",axis = 1)
        
        #Rows and Columns
        df_shape = df.shape
        logging.info(f"Rows:- {df_shape[0]} and Columns:- {df_shape[1]}")
        
        return df
    
    except Exception as e:
       

        raise InsuranceException(e,sys)
    
"""
Here we are converting our normal columns to float except the categorical columns and the exclude_colums

"""
def convert_column_float(df:pd.DataFrame,exclude_columns=list):
    try:
        for column in df.columns:
            if column not in exclude_columns:
                if df[column].dtypes!="O":
                    df[column]=df[column].astype("float")
        return df            

    except Exception as e:
       

        raise InsuranceException(e,sys)
    
"""
Here we are creating a yaml file and we are passing our data as dictionary and file path to store our data dict
"""
def write_yaml_file(file_path,data:dict):
        try:
            file_dir=os.path.dirname(file_path)
            print(file_dir)
            os.makedirs(file_dir,exist_ok=True)

            with open(file_path,"w") as file_write:
                yaml.dump(data,file_write)
        except Exception as e:
            raise InsuranceException(e,sys)

def save_object(file_path,obj)->None:
    try:
        os.makedirs(os.path.dirname((file_path)),exist_ok=True)
        with open(file_path,"wb") as file_obj:
            dill.dump(obj,file_obj)


    except Exception as e:
        raise InsuranceException(e,sys)
        
def load_object(file_path,obj):
    try:
        if not os.path.exists(file_path):
            raise Exception(f"the file:{file_path} is not available ")
        with open(file_path,"rb") as file_obj:
            dill.open(obj,file_path)
    except Exception as e:
         raise InsuranceException(e,sys)
    
def save_numpy_array_data(file_path,array):
    try:
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path,exist_ok=True)
        with open(file_path,"wb") as file_obj:
            np.save(file_obj,array)
    except Exception as e:
         raise InsuranceException(e,sys)
    

"""

"""
def load_numpy_array_date(file_path)->np.array:
    try:
        with open(file_path,"rb") as file_obj:
            return np.load(file_obj)
    except Exception as e:
        raise InsuranceException(e,sys)