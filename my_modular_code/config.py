import pymongo
import pandas as pd
import numpy as np
import json
import os,sys
from dataclasses import dataclass

@dataclass
class EnvironmentVariable:
    mongo_df_url:str=os.getenv("MONGO_DB_URL")

mongo_var=EnvironmentVariable()
mongo_client=pymongo.MongoClient(mongo_var.mongo_df_url)
TARGET_COLUMN = "expenses"
print(mongo_var.mongo_df_url)