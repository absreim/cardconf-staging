import requests
import psycopg2

URL = 'https://api.magicthegathering.io/v1/subtypes'

r = requests.get(URL)
subtypes = r.json()['subtypes']

conn = psycopg2.connect("dbname=cardconf_staging")
cur = conn.cursor()
for subtype in subtypes:
    cur.execute('INSERT INTO subtypes (name) VALUES (%s)', (subtype,))
conn.commit()
cur.close()
conn.close()