# from distutils.core import setup
from setuptools import find_packages,setup
from typing import List
"""
Setup.py is used to create a central pakage for installation

print() STATEMENTS DOES NOT WORK IN SETUP.PY
We have run requirement.txt file which will let the setup file work 
-e . :- is used for getting editing rights from requirements.txt so that it can  fetcch stuff from setup.py

The 'typing' module in Python provides support for type hints, 
which allow you to specify the expected types of function arguments and return values.
Syntax :-
def function(parameter : datatype)-> output_Datatype:

"""

#Create variable
requriment_file_name = "requirements.txt"
REMOVE_PACKAGE = "-e ."



REMOVE_PACKAGES="-e ."
requirement_file_name="requirements.txt"

#get_requirements()->List[str] :- 
def get_requirements()->List[str]:
    print("Process Started .........")
    with open(requirement_file_name) as requirement_files:
        requirement_list=requirement_files.readlines()
    print("hey",requirement_list)
    requirement_list=[requirement_name.replace("\n","") for requirement_name in requirement_list]
    print(requirement_list)
    if REMOVE_PACKAGES in requirement_list:
        requirement_list.remove(REMOVE_PACKAGES)
    return requirement_list
setup(
    #Name of the Project
    name='my_modular_code',
    #we have change the version with every release
    version='0.0.1',
    
    description='Insurance Industry Level Project',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Karthik Santosh',
    author_email='karthiksantosh2521@gmail.com',
    #find_packages:-is used to find the init file in every subdirectory 
    packages=find_packages(),
    install_requires=get_requirements()
     )
get_requirements()