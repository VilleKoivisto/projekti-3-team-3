import psycopg2
import requests
import os
import json

salasana = os.environ.get('salasana', 'Specified environment variable is not set.')
host_ip = os.environ.get('host', 'Specified environment variable is not set.')

def vittuilun_lisays(request):
    request_json = request.get_json(silent=True)

    try:
        nimi = request_json['nimi']
        email = request_json['email']
        paikkakunta = request_json['kunta']
        vittuilu_tier = request_json['tier']

        talleta_tiedot(nimi, email, paikkakunta, vittuilu_tier)
        return "200"
    except:
        return "400"

def talleta_tiedot(nimi, email, paikkakunta, vittuilu_tier):
    con = None
    try:
        con = psycopg2.connect(database="vittuilu", user = "postgres", password = salasana, host = host_ip)
        cursor = con.cursor()

        SQL = f"INSERT INTO {vittuilu_tier} (nimi,email, paikkakunta) VALUES(%s,%s,%s);"
        arvot = (nimi, email, paikkakunta)
        
        cursor.execute(SQL, arvot)
        
        con.commit()
        cursor.close()
        return print("Talletus onnistui!")
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if con is not None:
            con.close()