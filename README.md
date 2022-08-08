# Tabeasy
An automated tabulation website for mock trial tournaments available at [tabeasy.org](https://tabeasy.org/).
Currently in use for Peer Potential Mock Trial (PPMT) 2022, the largest Chinese high school mock trial tournament. 

## Installation 
1. clone this repo
```
git@github.com:carlguo866/tabeasy.git
```
2. Create a conda environment using the .yaml file in project root and activate it:
```
conda env create -f env-mac.yaml 
conda activate tabeasy
```
3. Setup PostgresSQL: install PostgresSQL and setup the database to match tabeasy.settings.DATABASES:
4. Make migrations and run server
```
python manage.py migrate
python manage.py runserver
```
