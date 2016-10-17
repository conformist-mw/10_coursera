import re
import requests
from lxml import etree
from bs4 import BeautifulSoup
from openpyxl import Workbook
import json
import random
import argparse


def get_courses_list():
    url = 'https://www.coursera.org/sitemap~www~courses.xml'
    xml = requests.get(url)
    root = etree.fromstring(xml.content)
    links = [link.text for link in root.iter('{*}loc') if 'learn' in link.text]
    random.shuffle(links)
    return links[:20]


def get_content(url):
    html = requests.get(url).content
    return BeautifulSoup(html, 'lxml')


def get_title(soup):
    title = soup.find('div', {'class': 'title'})
    return title.text if title else None


def get_lang(soup):
    table = soup.find('table', {'class': 'basic-info-table'})
    trs = table.findAll('tr')
    for tr in trs:
        if re.search(r'Lang', tr.text):
            key, value = [td.text.split()[0] for td in tr.findAll('td')]
            return value.rstrip(',')


def get_date(soup):
    script = soup.find('script', {'type': 'application/ld+json'})
    if script and re.search(r'startDate', script.text):
        return json.loads(script.text)['hasCourseInstance'][0]['startDate']


def get_weeks(soup):
    return len(soup.findAll('div', {'class': 'week'}))


def get_rate(soup):
    rate = soup.find('div', {'class': 'ratings-text'})
    return rate.text if rate else None


def get_course_info(url):
    soup = get_content(url)
    course = [
        get_title(soup),
        get_lang(soup),
        get_date(soup),
        get_weeks(soup),
        get_rate(soup),
        url
    ]
    return course


def output_courses_info_to_xlsx(filepath, courses_info):
    headers = ['Title', 'Language', 'Start Date',
               'Weeks amount', 'Course Rate', 'URL']
    wb = Workbook()
    ws = wb.active
    ws.title = 'coursera'
    for j, col in enumerate(headers, 1):
        ws.cell(row=1, column=j).value = col
    for num, course in enumerate(courses_info, 2):
        for i, val in enumerate(course, 1):
            if i == 6:
                ws.cell(row=num, column=i).value = 'more details →'
                ws.cell(row=num, column=i).hyperlink = val
            else:
                ws.cell(row=num, column=i).value = val
    wb.save(filename=filepath)
    print('Данные записаны в файл: {}'.format(filepath))
    return True


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Скрипт собирает информацию о разных курсах на Курсере')
    parser.add_argument('filepath', help='укажите файл в формате xlsx')
    args = parser.parse_args()
    links = get_courses_list()
    lists = [get_course_info(link) for link in links]
    output_courses_info_to_xlsx(args.filepath, lists)
