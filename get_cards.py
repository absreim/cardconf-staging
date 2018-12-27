import requests
import psycopg2
import json
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('start_page', default=1, nargs='?', type=int)
args = parser.parse_args()

BASE_URL = 'https://api.magicthegathering.io/v1/cards'

page = args.start_page
url = BASE_URL
if page > 1:
    url = BASE_URL + '?page={0}'.format(page)

r = requests.get(url)
cards = r.json()['cards']

conn = psycopg2.connect('dbname=cardconf_staging')
cur = conn.cursor()

def insert_rows():
    for card in cards:
        cur.execute('INSERT INTO cards (card) VALUES (%s)',
                    (json.dumps(card),))
    conn.commit()
insert_rows()

while int(r.headers['Count']) != 0:
    page += 1
    url = BASE_URL + '?page={0}'.format(page)
    r = requests.get(url)
    if r.status_code == 403:
        print(('Hit rate limit on page {0}.' 
               'Continue later with that page.').format(page))
        break
    print("Now querying page {0}.".format(page))
    cards = r.json()['cards']
    insert_rows()
    print("Done inserting data for {0}.".format(page))
cur.close()
conn.close()
