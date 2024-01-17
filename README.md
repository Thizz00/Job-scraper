
# Job scraper with resume checker

## A brief description of what this project does:

The application allows you to scrape data from the three largest platforms related to job ads.
In addition, it has the ability to match those offers which are most similar to the user's cv.




## Run Locally

Clone the project

```bash
  git clone https://github.com/Thizz00/Job-scraper-0.0.1.git
```

## Installation

Install requirements

```bash
  pip install requirements.txt
```

## Structuring a repository

Job-scraper
├───CV
├───logs
├───pages
├───screenshots
├───scripts
│   ├───core
│   └───resume_checker
├───src
│   ├───config
│   ├───database
│   ├───logs_configure
│   ├───models
│   └───schemas
└───tests



## Environment Variables

To run this project, you will need to add the following environment variables to your .env file

`STR_LINK1` - address of the first page for job search

`STR_LINK2` - address of the second page for job search

`STR_LINK3` - address of the third page for job search

`SCRAP_URL1` - address of the first page for job search with all categories

`SCRAP_URL2` - address of the second page for job search with all categories

`SCRAP_URL3` - address of the third page for job search with all categories

`DATABASE_URL` - The connection URL to the Mysql database 

`DATABASE_URL_LOGS` - The connection URL to the Mongo database 

## Connection with database

### Mysql connection

```Python
from sqlalchemy.ext.declarative import declarative_base
from dotenv import load_dotenv
import os

load_dotenv('.env')
DATABASE_URL = os.getenv('DATABASE_URL')

Base = declarative_base()
```

### Mongodb connection

```Python
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv
import os

load_dotenv('.env')

DATABASE_URL_LOGS = os.getenv('DATABASE_URL_LOGS')

client = MongoClient(DATABASE_URL_LOGS, server_api=ServerApi('1'))

mongo_db = client['Logs']
log_collection = mongo_db['Logs_scraper']
```
## Running a job and displaying data using streamlit

```bash
  streamlit run main.py
```

![App Screenshot](/screenshots/streamlitapp.png)

## Command-Line option and argument parsing

If all you need is to display the scraped data in the database then:


```bash
  python scripts/main_nostreamlit.py --job main_job_scraper
```

if you need data scraping every so often:

```bash
  python scripts/main_nostreamlit.py --job job_scraper_scheduler --interval 90
```
    
If all you need is to display the scraped data in the database  and additionally extract those data that match your cv:

```bash
  python scripts/main_nostreamlit.py --job main_job_scraper --match main_resume_matcher
```
    
## Additional information

**CV** in pdf form should be placed in the **CV folder**.

Logs are automatically saved in folder **Logs/logs.txt** as well as after connecting **mongodb** database **Logs.Logs_sraper**
## A chart showing the application design

![App Screenshot](/screenshots/app.png)


## Authors

- [@Thizz00](https://github.com/Thizz00)

