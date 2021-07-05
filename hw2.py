from bs4 import BeautifulSoup as bs
import requests
import csv
import pandas as pd


link = "https://hh.ru/search/vacancy"
headers = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                         "Chrome/88.0.4324.192 Safari/537.36 OPR/74.0.3911.218"}
vacancy = input("Введите название вакансии: ")

def get(link, headers, params):
    r = requests.get(
        link,
        headers=headers,
        params=params)
    return r

def len_pages():
    page = 0
    next_buttom = 0
    link1 = "https://hh.ru/search/vacancy"
    headers1 = {
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/88.0.4324.192 Safari/537.36 OPR/74.0.3911.218"}

    while next_buttom is not None:
        params1 = {'text': vacancy, 'page': page}
        p = requests.get(
            link1,
            headers=headers1,
            params=params1,
        )
        soup1 = bs(p.text, features="html.parser")
        next_buttom = soup1.find("a", {"class": "bloko-button", 'data-qa': 'pager-next'})
        page += 1
    return page


def parse_vacancies_on_page():
    all_vacancies = []
    soup = bs(r.text, features="html.parser")
    vacancies_on_page = soup.find_all("div", {"class": "vacancy-serp-item"})


    vacancy_names = []
    vacancy_salary_min = []
    vacancy_salary_max = []
    vacancy_links = []
    vacancy_site_name = []


    for vacancy in vacancies_on_page:
        vacancy_info_text = vacancy.find("div", {"class": "vacancy-serp-item__info"})

        # Название вакансии
        name_block = vacancy_info_text.find("a", {"class": "bloko-link"})
        if name_block is not None:
            name = name_block.text
        else:
            name = ""
        vacancy_names.append(name)

        # Данные по зп

        vacancy_salary_block = vacancy.find("div", {"class": "vacancy-serp-item__sidebar"})
        if vacancy_salary_block is not None:
            vacancy_salary = vacancy_salary_block.text
        else:
            vacancy_salary = ""

        if len(vacancy_salary) == 0:
            vacancy_salary_min.append(None)
            vacancy_salary_max.append(None)
        elif vacancy_salary.find("-") != -1:
            vacancy_salary_min.append(vacancy_salary.split('-')[0].encode('ascii', 'ignore'))
            vacancy_salary_max.append(
                vacancy_salary.split('-')[1].split("руб")[0].split("USD")[0].encode('ascii', 'ignore'))
        elif vacancy_salary.find("от") != -1:
            vacancy_salary_min.append(
                vacancy_salary.split('от')[1].split("руб")[0].split("USD")[0].encode('ascii', 'ignore'))
            vacancy_salary_max.append(None)
        elif vacancy_salary.find("до") != -1:
            vacancy_salary_min.append(None)
            vacancy_salary_max.append(
                vacancy_salary.split('до')[1].split("руб")[0].split("USD")[0].encode('ascii', 'ignore'))
        else:
            vacancy_salary_min.append(None)
            vacancy_salary_max.append(None)


        # Ссылка на вакансию
        vacancy_link_block = vacancy_info_text.find("a", {"class": "bloko-link"})
        if vacancy_link_block is not None:
            vacancy_link = vacancy_link_block.get("href")
        else:
            vacancy_link = ""
        vacancy_links.append(vacancy_link)

        # Сайт, откуда собрана вакансия
        if len(vacancy_link) == 0:
            vacancy_site = None
        else:
            try:
                vacancy_site = vacancy_link.split('/')[2].split("/")[0]
            except IndexError:
                vacancy_site = None

        vacancy_site_name.append(vacancy_site)

    # Заполнение словарей по каждой вакансии
    for i in range(len(vacancy_names)):
        vacancy = {"name": vacancy_names[i],
                   "salary_from": vacancy_salary_min[i], "salary_to": vacancy_salary_max[i],
                   "vacancy_site": vacancy_site_name[i],
                   "link": vacancy_links[i]
                   }
        all_vacancies.append(vacancy)
    return all_vacancies


page_all = len_pages()
number_page = int(input(f'По вашему запросу найдено {page_all} листов вакансии, '
                        f'напишите число листов для загрузки: '))
if number_page > page_all:
    print('Выбраное число листов превышает максимальное, будет выгружен только первый лист: ')
    number_page = 0

page_p = 0

with open('vacancy_hh.csv', 'w') as csv_file:
    csv_writer = csv.writer(csv_file)

while page_p < page_all:
    params = {'text': vacancy, 'page': page_p}
    r = get(link, headers, params)
    page_p += 1
    parse_vacancies_on_page().append(parse_vacancies_on_page())
    data = parse_vacancies_on_page()
    with open('vacancy_hh.csv', 'a') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(data[0].keys())
        for dict_item in data:
            csv_writer.writerow(dict_item.values())

hh_df = pd.read_csv('vacancy_hh.csv')
print(hh_df)