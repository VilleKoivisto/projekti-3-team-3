import smtplib
from email.message import EmailMessage
import flask
import psycopg2
import requests
import json

# unix_socket tyyliin tiedot heitetään näin, voi tehdä sitten myöhemmin kun funktio liikahtaa pilveen
# unix_socket = '/cloudsql/{}'.format("tähän:sqln:connection:name")

def hae_tiedot_mid():
    d = {}
    con = None
    try:
        con = psycopg2.connect(database="asdasdasd", user = "asdasdasd", password = "asdasdasd", host = "asdasdasd") # tänne sit host kostaan unix_socket
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
    request_args = request.args

    if request_args and "name" in request_args:
        name = request_args["name"]
    else:
        name = "juukeli"
    return "Haista sinä {} vittu!".format(flask.escape(name))

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

    # haetaan lähettäjän tiedot ("spämmiacco")
    lahettaja_email = "asdasdasd"                # salaisuuksiin myöhemmin
    passu = "asdasdasdsad"                                  # salaisuuksiin myöhemmin
    server.login(lahettaja_email, passu)

    viesti['Subject'] = f"VittuiluAPIlta hyvää huomenta!"
    viesti['From'] = lahettaja_email
    viesti['To'] = sposti

    server.send_message(viesti)
    server.quit()

def looppaa_laheta_mid():
    for i in hae_tiedot_mid():
        haetiedotdict = hae_tiedot_mid()
        nimi = haetiedotdict[i][0]
        sposti = haetiedotdict[i][1]
        emailiohjelma_mid(nimi, sposti)