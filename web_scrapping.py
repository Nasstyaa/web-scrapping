import requests
from bs4 import BeautifulSoup
import lxml
from fake_headers import Headers
from pprint import pprint
import json

url = 'https://spb.hh.ru/search/vacancy?text=python&area=1&area=2'

def get_headers():
  return Headers(browser="firefox", os="win").generate()

r = requests.get(url, headers=get_headers()).text
soup = BeautifulSoup(r, 'lxml')
vacancies_content = soup.find(id='a11y-main-content')
list_vacancies = vacancies_content.find_all('div', class_='vacancy-serp-item__layout')

vacancies_parsed = []
for vacancy in list_vacancies:
  vacancy_link = vacancy.find('a', class_='serp-item__title')['href']
  company_name = vacancy.find('a', {'data-qa': 'vacancy-serp__vacancy-employer'}).text
  vacancy_location = vacancy.find('div', {'data-qa': 'vacancy-serp__vacancy-address'}).text.split(' ')
  vacancy_html = requests.get(vacancy_link, headers=get_headers()).text

  if 'Москва' in vacancy_location or 'Санкт-Петербург' in vacancy_location:
    vacancy_discription = BeautifulSoup(vacancy_html, "html5lib").find('div', {'data-qa': 'vacancy-description'}).text.split(' ')
    #print(vacancy_discription)
    if 'Django' in vacancy_discription or 'Flask' in vacancy_discription:
       vacancy_salary = BeautifulSoup(vacancy_html, "html5lib").find('div', {'data-qa': 'vacancy-salary'}).text
       company_name = BeautifulSoup(vacancy_html, "html5lib").find('a', {'data-qa': 'vacancy-company-name'}).text
       vacancies_parsed.append({
               'vacancy_link': vacancy_link,
               'vacancy_salary': vacancy_salary,
               'company_name': company_name,
               'vacancy_location': vacancy_location
           })

with open ('web_scrapping.json', 'w', encoding = 'utf-8') as f:
    f.write(json.dumps(vacancies_parsed, indent=2, ensure_ascii=False))
