<img src="https://img.shields.io/badge/Python-FFD43B?style=for-the-badge&logo=python&logoColor=blue"/> <img src="https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white"/> <img src="https://img.shields.io/badge/MySQL-005C84?style=for-the-badge&logo=mysql&logoColor=white"/> <img src="https://img.shields.io/badge/MongoDB-4EA94B?style=for-the-badge&logo=mongodb&logoColor=white"/>



# Job scraper with resume checker 🚀

## A brief description:

The application allows you to scrape data from the three largest platforms related to job ads.
In addition, it has the ability to match those offers which are most similar to the user's cv.




## Run Locally

Clone the project

```bash
  git clone https://github.com/Thizz00/Job-scraper.git
```

## Installation

Install requirements

```bash
  pip install requirements.txt
```

## Structuring a repository

```
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
```


## Environment Variables

To run this project, you will need to add the following environment variables to your .env file

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
## Streamlit dashboard

```bash
  streamlit run main.py
```

## Running a job and displaying data using streamlit

![App Screenshot](/screenshots/streamlitapp.png)

## Task scheduler Windows


Downloading job offer data using the windows scheduler:

In **run_scraper.ps1** set **$currentLocation** to the full path for the directory where the project is placed.

1. Open Task Scheduler by going to **Start**->**Control Panel**->**Administrative Tools**->**Task Scheduler**.
   
2. Under Trigger leave it on Daily and press **repeat the task every**.

3. For Start a Program select **'powershell'** and add arguments full path to **run_scraper.ps1**.

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

## License

This project is licensed under the [MIT License](LICENSE).

## Author

- [@Thizz00](https://github.com/Thizz00)

