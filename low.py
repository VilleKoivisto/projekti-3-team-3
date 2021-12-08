import smtplib
from email.message import EmailMessage
import psycopg2
import requests
import json

# unix_socket tyyliin tiedot heitetään näin, voi tehdä sitten myöhemmin kun funktio liikahtaa pilveen
# unix_socket = '/cloudsql/{}'.format("tähän:sqln:connection:name")

def hae_tiedot_low():
    d = {}
    con = None
    try:
        con = psycopg2.connect(database="asdasdasd", user = "asdasdasd", password = "asdasdasd", host = "asdasdasd") # tänne sit host kostaan unix_socket
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

    # haetaan lähettäjän tiedot ("spämmiacco")
    lahettaja_email = "asdasdasdas"                         # salaisuuksiin myöhemmin
    passu = "asdasdasdasd"                                  # salaisuuksiin myöhemmin
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