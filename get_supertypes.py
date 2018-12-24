import requests
import psycopg2

URL = 'https://api.magicthegathering.io/v1/supertypes'

r = requests.get(URL)
supertypes = r.json()['supertypes']

conn = psycopg2.connect("dbname=cardconf_staging")
cur = conn.cursor()
for supertype in supertypes:
    cur.execute('INSERT INTO supertypes (name) VALUES (%s)', (supertype,))
conn.commit()
cur.close()
conn.close()