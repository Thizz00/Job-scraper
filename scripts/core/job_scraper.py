from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor
import requests
import logging

class JobScraper:
    def __init__(self, links):
        self.links = links
        self.df = pd.DataFrame(columns=['Category', 'Link', 'Offer', 'Company name',
                                        'Salary', 'Tech stack', 'Type of work',
                                        'Experience', 'Employment Type', 'Operating mode',
                                        'Job Description', 'Application form', 'Scraping date'])
    def process_job_link(self, link):
        response = requests.get(link)
        try:
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')

                category_classes_to_search = ['font-weight-semi-bold ng-star-inserted',
                                                'MuiBox-root css-11tdt7u', 'css-1wqvamp']
                category_text = 'No data'
                for class_name in category_classes_to_search:
                    category = soup.find_all(class_=class_name)
                    if category:
                        category_text = ', '.join(
                            [i.text.replace('\n', ' ').replace('new', '').strip() for i in category])
                        break
        

                offer_classes_to_search = ['css-vb54bv', 'css-g9dzcj','css-lr4g51', 'font-weight-bold']
                offer_text = 'No data'
                for class_name in offer_classes_to_search:
                    offer = soup.find_all(class_=class_name)
                    if offer:
                        offer_text = ', '.join(
                            [i.text.replace('\n', ' ').strip() for i in offer])
                        break

                name_classes_to_search = ['d-flex flex-grow-1 flex-column mobile-info',
                                            'd-block posting-title__company text-truncate',
                                            'inline-info d-flex align-items-center ng-star-inserted',
                                            'css-dfzd7q', 'css-1yxroko',
                                            'inline-info d-flex align-items-center text-primary ng-star-inserted']
                name_text = 'No data'
                for class_name in name_classes_to_search:
                    name = soup.find_all(class_=class_name)
                    if name:
                        name_text = ', '.join(
                            [i.text.replace('\n', ' ').strip() for i in name])
                        break


                salary_classes_to_search = ['salary ng-star-inserted',
                                                'css-j7qwjs',
                                                'css-1xgztmx']
                salary_text = 'No data'
                for class_name in salary_classes_to_search:
                    salary = soup.find_all(class_=class_name)
                    if salary:
                        salary_text = ', '.join(
                            [i.text.replace('\n', ' ').strip() for i in salary])
                        break


                tech_stack_classes_to_search = [
                    'MuiChip-label MuiChip-labelMedium css-9iedg7',
                    'MuiTypography-root MuiTypography-subtitle2 css-x1xnx3',
                    'tw-btn tw-btn-xs tw-text-sm tw-font-normal tw-text-teal tw-border-2 tw-border-teal tw-whitespace-nowrap ng-star-inserted'
                ]
                tech_stack_text = 'No data'
                for class_name in tech_stack_classes_to_search:
                    tech_stack = soup.find_all(class_=class_name)
                    if tech_stack:
                        tech_stack_text = ', '.join(
                            [i.text.replace('\n', ' ').strip() for i in tech_stack])
                        break


                information_about_the_offer_to_search = [
                        'css-hjfrjb', 'css-8n1acl']
                experience_text = 'No data'
                type_of_work_text = 'No data'
                employment_Type_text = 'No data'
                operating_mode_text = 'No data'
                for class_name in information_about_the_offer_to_search:
                    information_about_the_offer = soup.find_all(class_=class_name)
                    if information_about_the_offer:
                        information_about_the_offer_text = ','.join([i.text.replace('\n', ' ')
                                                                        .replace('Rodzaj pracy', '')
                                                                        .replace('Doświadczenie', '')
                                                                        .replace('Forma zatrudnienia', '')
                                                                        .replace('Tryb pracy', '')
                                                                        .replace('Type of work', '')
                                                                        .replace('Experience', '')
                                                                        .replace('Employment Type', '')
                                                                        .replace('Operating mode', '') for i in information_about_the_offer])
                        information_about_the_offer_text = information_about_the_offer_text.split(
                                ',')
                        experience_text = information_about_the_offer_text[1]
                        type_of_work_text = information_about_the_offer_text[0]
                        employment_Type_text = information_about_the_offer_text[2]
                        operating_mode_text = information_about_the_offer_text[-1]

                if not information_about_the_offer:
                    experience_text = 'No data'
                    operating_mode_text = 'No data'
                    experience = soup.find_all(class_='d-flex align-items-center')
                    if experience:
                        experience_text = ','.join(
                            [i.text.replace('\n', ' ').replace('back to list','').replace('powrót do listy','') for i in experience])
                    operating_mode = soup.find_all(class_='tw-flex tw-items-center tw-w-full')
                    if operating_mode:
                        operating_mode_text = ','.join(
                            [i.text.replace('\n', ' ') for i in operating_mode])
                        
                job_description_classes_to_search = ['tw-overflow-hidden ng-star-inserted',
                                                        'css-ncc6e2', 'MuiBox-root css-n74wde',
                                                        'MuiBox-root css-j1eof']
                job_description_text = 'No data'
                for class_name in job_description_classes_to_search:
                    job_description = soup.find_all(class_=class_name)
                    if job_description:
                        job_description_text = ', '.join(
                            [i.text.replace('\n', ' ').strip() for i in job_description])
                        break


                application_form_classes_to_search = ['MuiBox-root css-v0f58i']
                application_form_text = 'External link'
                for class_name in application_form_classes_to_search:
                    application_form = soup.find_all(class_=class_name)
                    if application_form:
                        application_form_text = 'Form'
                        break

                scraping_date_text = datetime.now().strftime(
                        "%Y-%m-%d %H:%M:%S.%f")[:-4]

                new_row = {'category': category_text,
                            'link': link,
                            'offer': offer_text,
                            'company_name': name_text,
                            'salary': salary_text,
                            'tech_stack': tech_stack_text,
                            'type_of_work': type_of_work_text,
                            'experience': experience_text,
                            'employment_type': employment_Type_text,
                            'operating_mode': operating_mode_text,
                            'job_description': job_description_text,
                            'application_form': application_form_text ,
                            'scraping_date': scraping_date_text}

                logging.info(f'Successful data scraping for a link: {link}')
                return new_row
            else:
                logging.error(f'Failed to data scraping for link: {link}')
                return None
        except requests.RequestException as e:
            logging.error(f'Error data scraping link {link}: {str(e)}')
            return None

    def scrape_jobs(self):
        with ThreadPoolExecutor(max_workers=12) as executor:
            job_rows = list(executor.map(self.process_job_link, self.links))

        job_rows = [row for row in job_rows if row is not None]

        self.df = pd.concat(
            [self.df, pd.DataFrame(job_rows)], ignore_index=True)


