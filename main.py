from my_modular_code.logger import logging
from my_modular_code.exception import InsuranceException
import os , sys
from my_modular_code.utils import get_colllection_as_dataframe
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
        # test_logger_and_expetion()
        get_colllection_as_dataframe(database_name=DATABASE_NAME,collection_name=COLLECTION_NAME)
    except Exception as e:
        
        print("Error occoured")