import pymongo
import pandas as pd
import json
import pymongo
client = pymongo.MongoClient("mongodb+srv://karthikproject01:UCRFZ5aHwvWScMlO@cluster0.xhpfrw8.mongodb.net/?retryWrites=true&w=majority")
Data_file=r"C:\Users\karth\OneDrive\Documents\ML_COURSE\ML_ALGO\Project\Project_modular\Modular_code\insurance.csv"
DATABASE_NAME="INSURANNCE"
COLLECTION_NAME="INSURANCE_PROJECT"

if __name__=="__main__":
    df=pd.read_csv(Data_file)
    shape=df.shape
    print("Rows:-",shape[0],"columns:-",shape[1])
    df.reset_index(drop=True,inplace=True)
    json_record=list(json.loads(df.T.to_json()).values())
    #insert into the DATABASE
    client[DATABASE_NAME][COLLECTION_NAME].insert_many(json_record)