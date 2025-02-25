import requests
import selectorlib
from datetime import datetime
import sqlite3

connection = sqlite3.connect('dataSP.db')


URL = 'http://programmer100.pythonanywhere.com'
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}


def scrape(url):
    """Scrape the page source from the URL"""
    response = requests.get(url,headers=HEADERS)
    source = response.text
    return source

def extract(source):
    extractor = selectorlib.Extractor.from_yaml_file('extract_SP.yaml')
    value = extractor.extract(source)['temperature']
    return value

def store(extracted):
    now = datetime.now().strftime('%y-%m-%d-%H-%M-%S')
    row =[now, str(extracted)]
    date, temp = row
    cursor = connection.cursor()
    cursor.execute("INSERT INTO temperature VALUES(?,?)",(date,temp))
    connection.commit()
    print(row)
if __name__ == '__main__':
    scrapped = scrape(URL)
    extracted = extract(scrapped)
    store(extracted)
    print(extracted)


