# cloud functions
# entrypoint vittuiluviesti_mid
# runtime python 3.9

import smtplib
from email.message import EmailMessage
import flask
from flask import escape
import functions_framework
import psycopg2
import requests
import json
import os

dbpassu = os.environ.get('DB_PASSWORD', 'Specified environment variable is not set.')
hosti = os.environ.get('host', 'Specified environment variable is not set.')

def hae_tiedot_mid():
    d = {}
    con = None
    try:
        con = psycopg2.connect(database="vittuilu", user = "postgres", password = dbpassu, host = hosti)
        cursor = con.cursor()
        SQL = 'SELECT * FROM medium;'
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

def vittuiluviesti_mid(request):
    request_json = request.get_json(silent=True)
    request_args = request.args

    if request_json and 'name' in request_json:
        name = request_json['name']
    elif request_args and 'name' in request_args:
        name = request_args['name']
    else:
        name = "juukeli"
    return "Haista sinä {} vittu!".format(escape(name))

def vittuiluviesti_mid2(nimi):
    return f"Haista sinä {nimi} vittu!"

def emailiohjelma_mid(nimi, sposti):
    server = smtplib.SMTP('smtp.gmail.com', 587)

    server.ehlo()
    server.starttls()
    server.ehlo()

    viesti = EmailMessage()
    vittuiluviesti = vittuiluviesti_mid2(nimi)
    viesti.set_content(vittuiluviesti)

    emailiossa = os.environ.get('SEND_EMAIL', 'Specified environment variable is not set.')
    emailipassu = os.environ.get('SEND_EMAIL_PW', 'Specified environment variable is not set.')

    # haetaan lähettäjän tiedot ("spämmiacco")
    lahettaja_email = emailiossa
    passu = emailipassu
    server.login(lahettaja_email, passu)

    viesti['Subject'] = f"VittuiluAPIlta hyvää huomenta!"
    viesti['From'] = lahettaja_email
    viesti['To'] = sposti

    server.send_message(viesti)
    server.quit()
    return print("Viesti lähetetty!")

def looppaa_laheta_mid():
    for i in hae_tiedot_mid():
        haetiedotdict = hae_tiedot_mid()
        nimi = haetiedotdict[i][0]
        sposti = haetiedotdict[i][1]
        emailiohjelma_mid(nimi, sposti)
    return print("Funktio onnistui")