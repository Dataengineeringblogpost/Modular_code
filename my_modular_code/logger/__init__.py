"""
Here we are doing some basic settings of the logger file
Fornat date time etc we will be setting
"""

import logging
from datetime import datetime
import os

LOG_DIR="Insurance_log"

CURRENT_TIME_STAMP=f"{datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}"
LOG_FILE_NAME=f"log_{CURRENT_TIME_STAMP}.log"
#if  folder exist the create it
os.makedirs(LOG_DIR,exist_ok=True)
#Create the complete file path
LOG_FILE_DIR=os.path.join(LOG_DIR,LOG_FILE_NAME)
#Create a Logger
logging.basicConfig(
    #file path
    filename=LOG_FILE_DIR,
    #write shld be the file mode
    filemode="w",
    #Format in which the log shld be stored
    format='%(asctime)s %(levelname)s %(name)s %(message)s', 
    #Level of the logger
    level=logging.DEBUG


) 