import os
from dotenv import load_dotenv

load_dotenv('.env')

SCRAP_URL1 = os.getenv('SCRAP_URL1') #justjoint.it all locations url
SCRAP_URL2 = os.getenv('SCRAP_URL2') #rocket jobs all locations url
SCRAP_URL3 = os.getenv('SCRAP_URL3') # nofluffjobs url


def generate_urls(base_url, categories, experience_levels, page_range=None):
    url_list = []

    for category in categories:
        for experience_level in experience_levels:
            if page_range:
                for page in page_range:
                    url = f"{base_url}{
                        category}/{experience_level}?page={page}"
                    url_list.append(url)
            else:
                url = f"{base_url}{category}/{experience_level}"
                url_list.append(url)

    return url_list


def generate_first_urls():
    categories = [
        'javascript'#, 'html', 'php', 'ruby', 'python',
        #'java', 'net', 'scala', 'c', 'mobile', 'testing',
        #'devops', 'admin', 'ux', 'pm', 'game', 'analytics',
        #'security', 'data', 'go', 'support', 'erp', 'architecture', 'other'
    ]
    experience_levels = ['junior'#, 'mid', 'senior', 'c-level']
    ]
    return generate_urls(SCRAP_URL1, categories, experience_levels)


def generate_second_urls():
    categories = [
        'marketing', 'sales', 'finanse', 'inzynieria', 'design',
        'hr', 'logistyka', 'consulting', 'bi-data', 'pm',
        'media', 'support', 'seo', 'prawo', 'inne'
    ]
    experience_levels = [
        'doswiadczenie_staz-junior',
        'doswiadczenie_specjalista-mid',
        'doswiadczenie_starszy-specjalista-senior',
        'doswiadczenie_manager-c-level'
    ]

    return generate_urls(SCRAP_URL2, categories, experience_levels)


def generate_third_urls():
    return [SCRAP_URL3 + f'{i}' for i in range(1, 30)]


def generate_all_urls():
    first_urls = generate_first_urls()
    second_urls = generate_second_urls()
    third_urls = generate_third_urls()

    all_urls = first_urls# + second_urls + third_urls
    return all_urls


URLS = generate_all_urls()