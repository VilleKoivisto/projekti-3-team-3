# cloud functions
# entrypoint looppaa_laheta_mid
# runtime python 3.9

import smtplib
from email.message import EmailMessage
import flask
# from flask import escape
# import functions_framework
import psycopg2
import requests
import json
import os

dbpassu = os.environ.get('DB_PASSWORD', 'Specified environment variable is not set.')
hosti = os.environ.get('host', 'Specified environment variable is not set.')

def hae_tiedot_high():
    d = {}
    con = None
    try:
        con = psycopg2.connect(database="vittuilu", user = "postgres", password = dbpassu, host = hosti)
        cursor = con.cursor()
        SQL = 'SELECT * FROM high;'
        cursor.execute(SQL)
        results = cursor.fetchall()
        for result in results:
            numid = [result][0][0]
            d[numid] = [result][0][1], [result][0][2], [result][0][3]
        cursor.close()
        return d
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if con is not None:
            con.close()

def vittuiluviesti_high(request):
    request_json = request.get_json(silent=True)
    request_args = request.args

    if request_json == None or request_args == None:
        name = "juukeli"
        paikkakunta = "Turku"
    elif 'name' and 'paikkakunta' in request_json:
        name = request_json['name']
        paikkakunta = request_json['paikkakunta']
    elif 'name' and 'paikkakunta' in request_args:
        name = request_args['name']
        paikkakunta = request_args['paikkakunta']

    zippikoodi = ""
    haeapi = os.environ.get('OWEATHER_API', 'Specified environment variable is not set.')
    api_key = haeapi
    if paikkakunta == "Helsinki":
        zippikoodi = "00100"
    elif paikkakunta == "Tampere":
        zippikoodi = "33100"
    elif paikkakunta == "Turku":
        zippikoodi = "20100"
    elif paikkakunta == "Espoo":
        zippikoodi = "02100"
    elif paikkakunta == "Oulu":
        zippikoodi = "90100"
    
    # suomisää
    countrykoodi = "fi"
    url = "https://api.openweathermap.org/data/2.5/weather?zip=%s,%s&appid=%s&units=metric" % (zippikoodi, countrykoodi, api_key)
    
    response = requests.get(url)
    data = json.loads(response.text)
    asteet_paikkakunta = data['main']['temp_max']

    # phuket sää
    countrykoodi = "th"
    zippikoodi = "83000"
    url = "https://api.openweathermap.org/data/2.5/weather?zip=%s,%s&appid=%s&units=metric" % (zippikoodi, countrykoodi, api_key)
    
    response = requests.get(url)
    data = json.loads(response.text)
    asteet_phuket = data['main']['temp_max']

    vittuiluviesti = f"{name}! Ei saatana mikä nimi. Perkele, että mä vihaan tommosia tyyppejä. Tajuatko sä, että olis vähän parempi, jos aikoo menestyä elämässä, että älykkyysosamäärä ois hivenen suurempi kuin kengännumero? Idiootti! Paskahousu!\n\nSää paikkakunnalla {paikkakunta}: {asteet_paikkakunta}\nSää paikkakunnalla Phuket, Thaimaa: {asteet_phuket}\n"
    return vittuiluviesti

def vittuiluviesti_high2(nimi, paikkakunta):
        zippikoodi = ""
        haeapi = os.environ.get('OWEATHER_API', 'Specified environment variable is not set.')
        api_key = haeapi
        if paikkakunta == "Helsinki":
            zippikoodi = "00100"
        elif paikkakunta == "Tampere":
            zippikoodi = "33100"
        elif paikkakunta == "Turku":
            zippikoodi = "20100"
        elif paikkakunta == "Espoo":
            zippikoodi = "02100"
        elif paikkakunta == "Oulu":
            zippikoodi = "90100"
        
        # suomisää
        countrykoodi = "fi"
        url = "https://api.openweathermap.org/data/2.5/weather?zip=%s,%s&appid=%s&units=metric" % (zippikoodi, countrykoodi, api_key)
        
        response = requests.get(url)
        data = json.loads(response.text)
        asteet_paikkakunta = data['main']['temp_max']

        # phuket sää
        countrykoodi = "th"
        zippikoodi = "83000"
        url = "https://api.openweathermap.org/data/2.5/weather?zip=%s,%s&appid=%s&units=metric" % (zippikoodi, countrykoodi, api_key)
        
        response = requests.get(url)
        data = json.loads(response.text)
        asteet_phuket = data['main']['temp_max']

        # viestin teko
        vittuiluviesti = f"{nimi}! Ei saatana mikä nimi. Perkele, että mä vihaan tommosia tyyppejä. Tajuatko sä että olis vähän parempi, jos aikoo menestyä elämässä, jos älykkyysosamäärä ois hivenen suurempi kuin kengännumero? Idiootti! Paskahousu!\n\nSää paikkakunnalla {paikkakunta}: {asteet_paikkakunta}\nSää paikkakunnalla Phuket, Thaimaa: {asteet_phuket}\n"
        return vittuiluviesti

def emailiohjelma_high(nimi, paikkakunta, sposti):
    server = smtplib.SMTP('smtp.gmail.com', 587)

    server.ehlo()
    server.starttls()
    server.ehlo()

    viesti = EmailMessage()
    vittuiluviesti = vittuiluviesti_high2(nimi, paikkakunta)
    viesti.set_content(vittuiluviesti)

    # haetaan lähettäjän tiedot ("spämmiacco")
    lahettaja_email = "asdasdasdsad"                # salaisuuksiin myöhemmin
    passu = "asdasdasd"                                  # salaisuuksiin myöhemmin
    server.login(lahettaja_email, passu)

    viesti['Subject'] = f"VittuiluAPIlta hyvää huomenta!"
    viesti['From'] = lahettaja_email
    viesti['To'] = sposti

    server.send_message(viesti)
    server.quit()

def looppaa_laheta_high():
    for i in hae_tiedot_high():
        haetiedotdict = hae_tiedot_high()
        nimi = haetiedotdict[i][0]
        sposti = haetiedotdict[i][1]
        paikkakunta = haetiedotdict[i][2]
        emailiohjelma_high(nimi, paikkakunta, sposti)