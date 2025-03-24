"""
The setup.py file is an essential part of packaging and 
distributing Python projects. It is used by setuptools (or distutils in older Python versions) 
to define the configuration of your project, such as its metadata, dependencies, and more
"""
from setuptools import setup, find_packages
from typing import List

def get_requirements() -> List[str]:
    """Reads the requirements.txt file and returns the list of dependencies"""
    requirement_lst: List[str] = []
    try:
        with open('requirements.txt','r') as f:
            #Reads lines from the file
            lines = f.readlines()
            #Process each line
            for line in lines:
                #Remove leading/trailing whitespaces and newline characters
                line = line.strip()
                #Ignore empty lines and -e .
                if line and line != '-e .':
                    requirement_lst.append(line)
    except FileNotFoundError:
        print("No requirements.txt file found")

    return requirement_lst

setup(
    name='NHS_A&E_analysis',
    version='0.0.1',
    author='Adhiraj Banerjee',
    author_email='adhirajbane13@gmail.com',
    packages=find_packages(),
    install_requires=get_requirements()
)