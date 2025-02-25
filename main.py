import sqlite3
import time
import requests
import selectorlib
from send_email import send_email

connection = sqlite3.connect('data.db')


URL = 'http://programmer100.pythonanywhere.com/tours/'
"""
Algunas paginas no les agrada el scraping por lo que se pone el header para simular la obtencion"
de la pagina web como si fuera hecha por un buscador"
"""
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}


def scrape(url):
    """Scrape the page source from the URL"""
    response = requests.get(url,headers=HEADERS)
    source = response.text
    return source

def extract(source):
    extractor = selectorlib.Extractor.from_yaml_file('extract.yaml')
    value = extractor.extract(source)['tours']
    return value

def store(extracted):
    row = extracted.split(",")
    row = [item.strip() for item in row]
    cursor = connection.cursor()
    cursor.execute("INSERT INTO events VALUES(?,?,?)", row)
    connection.commit()


def read(extracted):
    row = extracted.split(",")
    row = [item.strip() for item in row]
    band, city, date = row
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM events WHERE band=? AND city=? AND date=?",(band, city, date))
    row = cursor.fetchall()
    return row

if __name__ == '__main__':
    while True:
        scrapped = scrape(URL)
        extracted = extract(scrapped)
        print(extracted)
        if extracted != 'No upcoming tours':
            row = read(extracted)
            if not row:
                message = f"""
                New event was found \n {extracted}
                """
                store(extracted)
                send_email(message)
                print('Email send!')
        time.sleep(5)