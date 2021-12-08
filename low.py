import smtplib
from email.message import EmailMessage
import psycopg2
import requests
import json
import os

dbpassu = os.environ['DB_PASSWORD']

def hae_tiedot_low():
    d = {}
    con = None
    try:
        con = psycopg2.connect(database="vittuilu", user = "postgres", password = dbpassu, host = "34.88.209.126")
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

def vittuiluviesti_low(request):
    return "Haista vittu!"

def vittuiluviesti_low2():
    return "Haista vittu!"

def emailiohjelma_low(sposti):
    server = smtplib.SMTP('smtp.gmail.com', 587)

    server.ehlo()
    server.starttls()
    server.ehlo()

    viesti = EmailMessage()
    vittuiluviesti = vittuiluviesti_low2()
    viesti.set_content(vittuiluviesti)

    # haetaan lähettäjän tiedot envistä ("spämmiacco")
    emailiossa = os.environ['SEND_EMAIL']
    emailipassu = os.environ['SEND_EMAIL_PW']

    lahettaja_email = emailiossa
    passu = emailipassu
    server.login(lahettaja_email, passu)

    viesti['Subject'] = f"VittuiluAPIlta hyvää huomenta!"
    viesti['From'] = lahettaja_email
    viesti['To'] = sposti

    server.send_message(viesti)
    server.quit()

def looppaa_laheta_low():
    for i in hae_tiedot_low():
        haetiedotdict = hae_tiedot_low()
        nimi = haetiedotdict[i][0]
        sposti = haetiedotdict[i][1]
        emailiohjelma_low(sposti)