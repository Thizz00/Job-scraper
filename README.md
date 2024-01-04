
# Job scraper with resume checker

A brief description of what this project does:

The application allows you to scrape data from the three largest platforms related to job ads.
In addition, it has the ability to match those offers which are most similar to the user's cv.




## Installation

Install requirements

```bash
  pip install requirements.txt
```
If all you need is to display the scraped data in the database then:

```bash
  python main.py --job main_job_scraper
```

if you need data scraping every so often:

```bash
  python main.py --job job_scraper_scheduler --interval 90
```
    
If all you need is to display the scraped data in the database  and additionally extract those data that match your cv:

```bash
  python main.py --job main_job_scraper --match main_resume_matcher
```
    
## A chart showing the application design:

![App Screenshot](/screenshots/app.png)

