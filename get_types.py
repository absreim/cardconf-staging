import requests
import psycopg2

URL = 'https://api.magicthegathering.io/v1/types'

r = requests.get(URL)
types = r.json()['types']

conn = psycopg2.connect("dbname=cardconf_staging")
cur = conn.cursor()
for type in types:
    cur.execute('INSERT INTO types (name) VALUES (%s)', (type,))
conn.commit()
cur.close()
conn.close()