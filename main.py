from my_modular_code.logger import logging
from my_modular_code.exception import InsuranceException
import os , sys
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
        test_logger_and_expetion()
    except Exception as e:
        
        print("Error occoured")