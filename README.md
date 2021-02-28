# Book Scraping Project 1 

**Version 1.0.0**


## Virtual environment configuration

- Creating a virtual environment

	Python installation is required for the following process. You can download Python on python.org
	Follow this step by step tutorial to create your virtual environment :
	https://uoa-eresearch.github.io/eresearch-cookbook/recipe/2014/11/26/python-virtual-env/

- Install requirement files

	pip install -r requirements.txt
	
- Install git on your local workspace
	
- Pull the project from github 
	
	Create a folder in the path of your choice. 
	Open a git bash in this folder and run the command "git init" to initialize a .git repository.
	After getting access to the github repository, pull the project with the following command :
	"git pull"

- Lauch the script 

	There are 3 scripts, each script is explained in the next section. 
	Run each script after you configured your virtual environment. 
	

## Important information about the differents files 

- script.py
	
	This script has all the methods to retrieve the product's informations  
	It is possible to get all the information about a single book with this script

- script_category.py
	
	This script retrieves all the information from the script.py script within its methods 
	It is possible to get all the information about all the books of a whole category

- script_all_categories.py
	
	This script retrieves all the information from the script_category.py within its methods
	It is possible to get all the information about all the books of all the categories

## Contributors 

- Milad EZAME <milad.ezame@gmail.com>
- © Milad EZAME - OpenClassrooms 