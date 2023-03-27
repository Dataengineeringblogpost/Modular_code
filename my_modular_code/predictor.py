import os
from my_modular_code.entity.config_entity import MODEL_FILE_NAME,TARGET_ENCODER_OBJECT_FILE_NAME,TRANSFORMED_OBJECT_FILE_NAME
from glob import glob
from typing import Optional
import os

# Now lets start model validation
"""
Objective:-
* Here we are basically comparing wheather 
our old model with old data was working better or with new data its working better
* When we put next time data then we have to  perform all our steps again
* if our new model is doing better then only we would accept it or else we would reject it(Depends on model acc)

"""

class ModelResolver:
    """
    Here we are putting the steps in this class 
    model_registry :- saved_models directory
    transformer_dir_name :- saving the transformed data
    target_encoder_dir_name:-
    model_dir_name :- mod
    we will get the transformed data then we will encode it then we create a model
    * Our saved model directory would be similar to our artifact directory and each time we run it will assign the folder nname as 0,1,2,3 etch in that folder
    we would havve our data validation transformation and model training and saved model
    """
    def __init__(self,model_registry:str = "saved_models",
                transformer_dir_name="transformer",
                target_encoder_dir_name = "target_encoder",
                model_dir_name = "model"):
        

        self.model_registry=model_registry
        #Creating the saved models directory
        os.makedirs(self.model_registry,exist_ok=True)
        #Creating instances
        self.transformer_dir_name = transformer_dir_name
        self.target_encoder_dir_name=target_encoder_dir_name
        self.model_dir_name=model_dir_name

# 1
    #getting the saved_model directory 
    def get_latest_dir_path(self)->Optional[str]:
        try:
            dir_names = os.listdir(self.model_registry)
            #if the directory has nothing then return None ie its running for the fiirst time
            if len(dir_names)==0:
                return None
            """
            everytime we run saved models
            first time:-0, 
            second time :-1 etc....
            """
            dir_names = list(map(int,dir_names))
            #here we are getting the latesr directory name ie 0,1,2 so 2 would be the last run
            latest_dir_name = max(dir_names)
            #we are creating the path of latest directory
            return os.path.join(self.model_registry,f"{latest_dir_name}")
        except Exception as e:
            raise e

# 2  
   #Getting model from the latest run or  latest directory path

    def get_latest_model_path(self):
        try:
            #calling function latest directory pathj
            latest_dir = self.get_latest_dir_path()
            #if none then we raise exception and say model is not available
            if latest_dir is None:
                raise Exception(f"Model is not available")
            #or else we just return  the model file path
            return os.path.join(latest_dir,self.model_dir_name,MODEL_FILE_NAME)
        except Exception as e:
            raise e
# 3
    #get the transformer data path same logic as above get_latest_model_path
    def get_latest_transformer_path(self):
        try:
            latest_dir = self.get_latest_dir_path()
            if latest_dir is None:
                raise Exception(f"Transformer is not available")
            #getting the transformer data
            return os.path.join(latest_dir,self.transformer_dir_name,TRANSFORMED_OBJECT_FILE_NAME)
        except Exception as e:
            raise e
# 4
    #same logic :- get_latest_model_path
    def get_latest_target_encoder_path(self):
        try:
            latest_dir = self.get_latest_dir_path()
            if latest_dir is None:
                raise Exception(f"Target encoder is not available")
            return os.path.join(latest_dir,self.target_encoder_dir_name,TARGET_ENCODER_OBJECT_FILE_NAME)
        except Exception as e:
            raise e

# 5
    #Creating a folder for saved model with 0,1,2
    def get_latest_save_dir_path(self)->str:
        try:
            latest_dir = self.get_latest_dir_path()
            if latest_dir is None:
                return os.path.join(self.model_registry,f"{0}")
            latest_dir_num = int(os.path.basename(self.get_latest_dir_path()))
            #Saved model with 0,1,2
            return os.path.join(self.model_registry,f"{latest_dir_num+1}")
        except Exception as e:
            raise e
   # 6
   # Here we are saving our new model called as model.pkl
    def get_latest_save_model_path(self):
        try:
            latest_dir = self.get_latest_save_dir_path()
            return os.path.join(latest_dir,self.model_dir_name,MODEL_FILE_NAME)
        except Exception as e:
            raise e
# 7
   # here we are saving our transformed 
    def get_latest_save_transformer_path(self):
        try:
            latest_dir = self.get_latest_save_dir_path()
            return os.path.join(latest_dir,self.transformer_dir_name,TRANSFORMED_OBJECT_FILE_NAME)
        except Exception as e:
            raise e
# 8
    #here we are saving the target encoder
    def get_latest_save_target_encoder_path(self):
        try:
            latest_dir = self.get_latest_save_dir_path()
            return os.path.join(latest_dir,self.target_encoder_dir_name,TARGET_ENCODER_OBJECT_FILE_NAME)
        except Exception as e:
            raise e