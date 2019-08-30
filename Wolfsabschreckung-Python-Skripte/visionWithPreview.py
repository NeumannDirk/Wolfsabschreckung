#Autoren: 					Alexander Luft (23945)
#Datum:						30.08.2019
#Dozent: 					Prof. Dr. O. Drögehorn
#Veranstaltung/Semester: 	Future Internet/ Digitales Kulturerbe Anwendungspraktikum /Sommersemester 2019

import requests
import matplotlib.pyplot as plt
from PIL import Image
from io import BytesIO
from picamera import PiCamera
from time import sleep
from wolfdefense import WolfDefense
from state import StateOfPi
import configparser
import io

state = StateOfPi()

# Laden der Konfigurationsdatei
config = configparser.ConfigParser()
config.sections()
config.read('config.ini')


# Festlegen des Schlüssels des Azure-Service-Abonements
subscription_key = config.get('azure','subscription_key')
assert subscription_key

#LED-Leuchtet Blau auf, Skript ist gestartet
state.blink_blue()
sleep(2)

# Festlegung des Azure-Service-Links aus dem Azure-Service-Abonements
vision_base_url = config.get('azure','vision_base_url')

# analyze legt fest, das die Geuploadeten Bilder auf ihren Inhalt Analyziert werden sollen
analyze_url = vision_base_url + "analyze"

# Pfad der zu analysierenden Datei
image_path = config.get('image','image_patch')

# Camera
camera = PiCamera()
# Bildauflösung
camera.resolution = (1800,920)

# Das Skript Öffnet ein Fenster, das den Bildauschschnitt der Kamera darstellt
camera.start_preview(fullscreen=False, window=(100,50,800,1000))

# Startet die Threadklassen lightShow und audioPlayer
wolfdefense = WolfDefense()
#LED-Blinken Grün, Gerät ist bereit um Bidler zu Versenden und zu Analysieren
state.blink_green()
sleep(2)
# --------- Ab hier while -------
# Schleife läuft solange, bis eine Fehler auftritt oder das Programm beendet wird
while True:
    #Stoppen der Soundausgabe und des LED leuchtens 
    wolfdefense.deactivate_defense()
    sleep(2)
	#Kamera nimmt Bild auf
    camera.capture(image_path)

    # Lädt das Bild in ein Byte-Array
    image_data = open(image_path, "rb").read()
    
	#Festlegung des zu Versendenden Headers mit dem Schlüssel
    headers    = {'Ocp-Apim-Subscription-Key': subscription_key,
                  'Content-Type': 'application/octet-stream'}
	# Festlegung der Parameter die als JSON-Werte wieder zurück gegeben werden sollen
    params     = {'visualFeatures': 'Categories,Description,Tags'}
    
	#Versenden des headers, parameter und Bildes an die URL des Azure-Service
    response = requests.post(
        analyze_url, headers=headers, params=params, data=image_data)
    
    try:
        
		#Wartet auf Antwort vom Clouddiesnt
        response.raise_for_status()

		#Sobald eine Antwort vom Clouddienst eintrifft, wird diese in einen JSON-String umgewandelt
        analysis = response.json()
		#Im JSON-String werden die Werte mit dem Key: "tags" in eine Vaiable übergeben
        tags = analysis["tags"]
        for tag in tags:  
            print(tag["name"] + " " + str(tag["confidence"]*100))  
			# sollte ein Name in den Tags Wolf sein und der Wert mit dem dieser ERkannt wurde größer als 70%, wird die Wolfabwehr gestartet, es speilt Musik und das LED-Band leuchtet
            if tag["name"] == "wolf" and (tag["confidence"]*100)>70:
                print("Ich erkenne einen Wolf")
                wolfdefense.activate_defense()
                
        print("---------------------------------")
                
	# Sollte ein Fehler beim Übertragen der Daten an den Clouddienst entstehen, Blinkt das LED Band Gelb und das Programm beeendet sich
    except Exception as e:
        state.blink_yellow()
        sleep(2)