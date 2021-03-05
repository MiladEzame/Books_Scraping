# Book Scraping Project 1 

**Version 1.0.0**


# Project Configuration

## Pull the project from github 
	
	After getting access to the github repository, pull the project with the following command :
	- git clone project_link

## Creating a virtual environment

	Python installation is required for the following process. You can download Python on python.org.
	Python3 includes venv that allows us to create a virtual environment very easily.
	Write the following command line in your windows command prompt to create a new virtual-
	-environment called environment_name :
	- python3 -m venv environment_name
	
	Once you've created the virtual environment, you have to activate it.
	On Windows, type the following command :
	- environment_name\Scripts\activate.bat
	On Unix or MacOS, type the following command:
	- source environment_name/bin/activate
	If you have any difficulties, please refer to this page : https://docs.python.org/3/tutorial/venv.html
	
## Install requirement files

	Once the environment is active, type this in the command prompt : 
	- pip install -r requirements.txt	

## Lauch the script 
	
	There are 3 scripts, each script is explained in the next section. 
	First, open the git bash inside the project folder if you are not in it.
	Before running the script, make sure you are in the virtual environment.
	You can run the scrap_all_categories.py file by using the following command :
	- python scrap_all_categories.py	

## Important information about the differents files 

- scrap_page.py
	
	This script has all the methods to retrieve one product's informations  
	Retrieves all the information about a single book on a specific page

- scrap_category.py
	
	This script retrieves all the information from the scrap_page.py script within its methods 
	Retrieves all the information about all the books of one specific category

- scrap_all_categories.py
	
	This script retrieves all the information from the scrap_category.py within its methods
	Retrieves all the information about all the books of all the categories

## Contributors 

- Milad EZAME <milad.ezame@gmail.com>
- © Milad EZAME - OpenClassrooms 
