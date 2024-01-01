from bs4 import BeautifulSoup
import requests

def check(link):
    response = requests.get(link)
    try:
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            tech_stack_classes_to_search = [
                                                'MuiChip-label MuiChip-labelMedium css-9iedg7',
                                                'MuiTypography-root MuiTypography-subtitle2 css-x1xnx3',
                                                'tw-mb-0 tw-flex tw-flex-wrap ng-star-inserted']
            tech_stack_text = 'No data'
            for class_name in tech_stack_classes_to_search:
                tech_stack = soup.find_all(
                    ['ul', 'span', 'h6'], class_=class_name)
                if tech_stack:
                    tech_stack_text = ','.join(
                        [i.text.replace('\n', ' ') for i in tech_stack])
                    break
            print(tech_stack_text)
    except Exception as e:
        print(e)

links = ['https://justjoin.it/offers/sigma-it-poland-solutions-architect','https://rocketjobs.pl/oferta/takeda-erp-platform-owner-supply-chain-lodz-252366','https://nofluffjobs.com/pl/job/fullstack-developer-knowit-remote-1']

for i in links:
    check(i)