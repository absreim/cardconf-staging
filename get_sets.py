import requests
import psycopg2

URL = 'https://api.magicthegathering.io/v1/sets'

r = requests.get(URL)
sets = r.json()['sets']

conn = psycopg2.connect("dbname=cardconf_staging")
cur = conn.cursor()
for set in sets:
    magic_cards_info_field = ''
    if 'magicCardsInfoCode' in set:
        magic_cards_info_field = set['magicCardsInfoCode']
    block_field = ''
    if 'block' in set:
        block_field = set['block']
    mkm_id_field = None
    if 'mkm_id' in set:
        mkm_id_field = set['mkm_id']
    mkm_name_field = None
    if 'mkm_name' in set:
        mkm_name_field = set['mkm_name']
    cur.execute(('INSERT INTO sets (code, name, type, border, mkm_id,'
                 'mkm_name, release_date, magic_cards_info_code,'
                 'block) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)'),
                (set['code'], set['name'], set['type'], set['border'],
                 mkm_id_field, mkm_name_field, set['releaseDate'],
                 magic_cards_info_field, block_field))
conn.commit()
cur.close()
conn.close()