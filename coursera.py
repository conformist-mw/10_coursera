import re
import requests
from lxml import etree
from bs4 import BeautifulSoup
from openpyxl import Workbook
import json
import random
# "https://www.coursera.org/api/courses.v1?q=slug&slug=courseName&fields=upcomingSessionStartDate"
# undocumented api field. remove 3 lasts symbols to get unix timestamp


def get_courses_list():
    url = 'https://www.coursera.org/sitemap~www~courses.xml'
    xml = requests.get(url)
    root = etree.fromstring(xml.content)
    links = [link.text for link in root.iter('{*}loc') if 'learn' in link.text]
    random.shuffle(links)
    return links[:1]


def get_course_info(url):
    data = {'User': 'None', 'weeks': 'None', 'start': 'None'}
    html = requests.get(url).content
    soup = BeautifulSoup(html, 'lxml')
    data['title'] = soup.find('div', {'class': 'title'}).text
    table = soup.find('table', {'class': 'basic-info-table'})
    trs = table.findAll('tr')
    for tr in trs:
        if re.search(r'Lang|Rating', tr.text):
            key, value = [td.text.split()[0] for td in tr.findAll('td')]
            data[key] = value
    script = soup.find('script', {'type': 'application/ld+json'})
    if script and re.search(r'startDate', script.text):
        data['start'] = json.loads(script.text)['hasCourseInstance'][
            0]['startDate']
    data['weeks'] = len(soup.findAll('div', {'class': 'week'}))
    datalist = [data['title'], data['Language'], data[
        'weeks'], data['start'], data['User'], url]
    return datalist


def output_courses_info_to_xlsx(filepath, courses_info):
    wb = Workbook()
    ws = wb.active
    ws.title = 'coursera'
    for num, course in enumerate(courses_info, 1):
        for i, val in enumerate(course, 1):
            if i == 6:
                ws.cell(row=num, column=i).value = 'more details →'
                ws.cell(row=num, column=i).hyperlink = val
            else:
                ws.cell(row=num, column=i).value = val
    wb.save(filename=filepath)


links = get_courses_list()
lists = [get_course_info(link) for link in links]
output_courses_info_to_xlsx('test.xlsx', lists)
