import requests
import psycopg2

URL = 'https://api.magicthegathering.io/v1/formats'

r = requests.get(URL)
formats = r.json()['formats']

conn = psycopg2.connect("dbname=cardconf_staging")
cur = conn.cursor()
for format in formats:
    cur.execute('INSERT INTO formats (name) VALUES (%s)', (format,))
conn.commit()
cur.close()
conn.close()