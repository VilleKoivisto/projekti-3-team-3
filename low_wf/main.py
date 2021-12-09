# cloud functions
# entrypoint looppaa_laheta_low
# runtime python 3.9

import smtplib
from email.message import EmailMessage
import psycopg2
import requests
import json
import os

dbpassu = os.environ.get('DB_PASSWORD', 'Specified environment variable is not set.')
hosti = os.environ.get('host', 'Specified environment variable is not set.')

def hae_tiedot_low():
    d = {}
    con = None
    try:
        con = psycopg2.connect(database="vittuilu", user = "postgres", password = dbpassu, host = hosti)
        cursor = con.cursor()
        SQL = 'SELECT * FROM low;'
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

def vittuiluviesti_low():
    return "Haista vittu!"

def vittuiluviesti_low2():
    return "Haista vittu!"

def emailiohjelma_low(sposti):
    server = smtplib.SMTP('smtp.office365.com', 587)

    server.ehlo()
    server.starttls()
    server.ehlo()

    viesti = EmailMessage()
    vittuiluviesti = vittuiluviesti_low2()
    viesti.set_content(vittuiluviesti)

    emailiossa = os.environ.get('SEND_EMAIL', 'Specified environment variable is not set.')
    emailipassu = os.environ.get('SEND_EMAIL_PW', 'Specified environment variable is not set.')

    # haetaan lähettäjän tiedot ("spämmiacco")
    lahettaja_email = emailiossa                         # salaisuuksiin myöhemmin
    passu = emailipassu                                  # salaisuuksiin myöhemmin
    server.login(lahettaja_email, passu)

    viesti['Subject'] = f"VittuiluAPIlta hyvää huomenta!"
    viesti['From'] = lahettaja_email
    viesti['To'] = sposti

    server.send_message(viesti)
    server.quit()
    return print("Viesti lähetetty!")

def looppaa_laheta_low(request):
    for i in hae_tiedot_low():
        haetiedotdict = hae_tiedot_low()
        nimi = haetiedotdict[i][0]
        sposti = haetiedotdict[i][1]
        emailiohjelma_low(sposti)
    return print("Funktio onnistui")