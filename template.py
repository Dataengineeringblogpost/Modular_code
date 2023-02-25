"""
Objective:-Creating automation Script to make basic folder structure or any ML project
"""
import os
from pathlib import Path
import logging
#logger to catch error
logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s:%(levelname)s]:%(message)s"
)
#Creating a folder structure with the help of a template
while True:
    project_name=input("Enter your Project name:- ")
    if project_name!="":
        break
logging.info(f"Creating project by name:{project_name}")
#This is a List of Files
list_of_files = [
    #keep aws creadential
    ".github/workflows/.gitkeep",
    #CI/CD:-Github pipeline
    ".github/workflows/main.yaml",
    f"{project_name}/__init__.py",
    f"{project_name}/components/__init__.py",
    f"{project_name}/entity/__init__.py",
    f"{project_name}/pipeline/__init__.py",
    f"{project_name}/logger/__init__.py",
    f"{project_name}/config.py",
    f"{project_name}/exception.py",
    f"{project_name}/predictor.py",
    f"{project_name}/utils.py",
    f"configs/config.yaml",
    "requirements.txt",
    "setup.py",
    "main.py"
]


for filepath in list_of_files:
    filepath = Path(filepath)
    filedir, filename = os.path.split(filepath)
    #Baciscally checking weather folder exist
    #if Parent Folder does not exist create one here
    if filedir !="":
        os.makedirs(filedir, exist_ok=True)
        logging.info(f"Creating a new directory at : {filedir} for file: {filename}")
    #if exits then open it and create the file
    if (not os.path.exists(filepath)) or (os.path.getsize(filepath) == 0):
        with open(filepath, "w") as f:
            pass
            logging.info(f"Creating a new file: {filename} for path: {filepath}")
    else:
        logging.info(f"file is already present at: {filepath}")