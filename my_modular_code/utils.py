import pandas as pd
import numpy as np
import sys
import os
from my_modular_code.exception import InsuranceException
from my_modular_code.logger import logging
from my_modular_code.config import mongo_client


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