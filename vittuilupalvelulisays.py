import psycopg2
import requests
import os
import json

salasana = "juukeli"
host_ip = "34.88.209.126"

def vittuilun_lisays():
    # 1) otetaan HTTP-pyyntö sisään ja puretaan muuttujiin:

    # puretaan http-pyyntö
    request_json = request.get_json(silent=True)

    # käsitellään POST
    if request_json is None:
        print("Nyt meni argumentit päin vittua")
    if 'nimi' or 'email' or 'kunta' or 'tier' not in 
    nimi = request_json["nimi"]
    email = request_json["email"]
    paikkakunta = request_json["kunta"]
    vittuilu_tier = request_json["tier"]
    
    talleta_tiedot(nimi, email, paikkakunta, vittuilu_tier)
    
    
    # # käsitellään GET
    # elif request.args: #args metodi katsoo, onko url:n mukana tullut argumentteja
    #     return "400"

    
    # # jos bodyssä ei jsonia:
    # else:
    #     print("400: jotain meni pieleen") 
    #     return "400" 
                       
  
    # 2) viedään muuttujien tieto tietokantakyselyyn ja tehdään "kysely" -> isketään tiedot kantaan

def talleta_tiedot(nimi, email, paikkakunta, vittuilu_tier):
    con = None
    try:
        con = psycopg2.connect(database="vittuilu", user = "postgres", password = salasana, host = host_ip)
        cursor = con.cursor()

        SQL = f"INSERT INTO {vittuilu_tier}(nimi,email, paikkakunta) VALUES(%s,%s,%s);"
        arvot = (nimi, email, paikkakunta)
        
        cursor.execute(SQL, arvot)
        
        con.commit()
        cursor.close()

        return print("Käsittely onnistui!")
        
    except (Exception, psycopg2.DatabaseError) as error:
        print("Nyt meni päin vittua SQL talletus.")
        
    finally:
        if con is not None:
            con.close()

data = {"nimi":"Herbert",
        "email":"asdasd@adasdas.fi",
        "kunta":"Espoo",
        "tier":"low"}
data2 = json.dumps(data)

vittuilun_lisays()