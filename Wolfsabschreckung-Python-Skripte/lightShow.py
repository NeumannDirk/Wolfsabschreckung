#Autoren: 					Alexander Luft (23945)
#Datum:						30.08.2019
#Dozent: 					Prof. Dr. O. Drögehorn
#Veranstaltung/Semester: 	Future Internet/ Digitales Kulturerbe Anwendungspraktikum /Sommersemester 2019

import time
import random
import RPi.GPIO as GPIO
import threading
from time import sleep

 

# Import the WS2801 module.

import Adafruit_WS2801

import Adafruit_GPIO.SPI as SPI

#Die LightBand-Klasse läuft als Thread im Hintergrund eines laufenden Pythonprogramms, dabei wird mit Semaphore der Ablauf des Programmes nach dem Start gesteuert
class LightBand(threading.Thread):


    def __init__(self):
        threading.Thread.__init__(self)
		
		
        self.PIXEL_COUNT = 32	#Anzahl der LEDS auf dem Lichtband
		
        self.SPI_PORT   = 0
        self.SPI_DEVICE = 0
		#Erstellen eines Objektes, das die RGB LEDS des Lichtbandes ansteuern kann, dafür muss die Anzahl der LEDs auf dem Lichtband übergeben werden, genauso wie der SD und der CK Pin Anschluss, diese werden durch das SPI.SpiDev vom Programm selbst ermittelt
        self.pixels = Adafruit_WS2801.WS2801Pixels(self.PIXEL_COUNT, spi=SPI.SpiDev(self.SPI_PORT, self.SPI_DEVICE), gpio=GPIO)
        self.blink_color_list = list()
        self.set_blink_color_list()
		
		#Initialisierung eins Switch (Semaphore) durch die übergabe des thread Events
        self.switch = threading.Event()
    
	#Lässt das LED-Band in einer Festgelegten Farbe (color) für eine Gewisse Anzahl (blink_times) mit Pausen (wait) Leuchten
    def blink_color(self,pixels, blink_times=5, wait=0.5, color=(255,0,0)):

        for i in range(blink_times):

            # blink two times, then wait

            pixels.clear()

            for j in range(2):

                for k in range(pixels.count()):

					# festlegung der Farbe in der die LEDs aufleuchten
                    pixels.set_pixel(k, Adafruit_WS2801.RGB_to_color( color[0], color[1], color[2] ))

                pixels.show()

                time.sleep(0.08)

				# die LEDs erlischen
                pixels.clear()

				# die LEDs leuchten
                pixels.show()

                time.sleep(0.08)

            time.sleep(wait)
        
    # Setzt 6 Farben fest, in der das Lichtband Blinken kann    
    def set_blink_color_list(self):
        self.blink_color_list.append((self.pixels, 4, (255, 0, 0)))
        self.blink_color_list.append((self.pixels, 4, (0, 255, 0)))
        self.blink_color_list.append((self.pixels, 4, (0, 0, 255)))
        self.blink_color_list.append((self.pixels, 4, (139, 0, 139)))
        self.blink_color_list.append((self.pixels, 4, (255, 215, 0)))
        self.blink_color_list.append((self.pixels, 4, (255, 140, 0)))
        
	# lässt das Lichtband Leuchten, dabei werden zufällige Farben aus der Liste ausgeählt
    def activate_blink_color(self):
        random.seed()
        list = random.choice(self.blink_color_list)
        self.blink_color(list[0],blink_times = list[1],color = list[2])
        self.pixels.clear()
        
	# Start-Methode der Threadklasse, in der Schleife wird solange durch das switch.wait gewartet, bis es durch die Methode light_play freigegeben wird
    def run(self):
        while True:
            self.switch.wait()
            self.activate_blink_color()
            sleep(2)
      
	# gibt den switch frei
    def light_play(self):
        self.switch.set()
     
	# blockiert den switch, so das in der run-Methode in der schleife wieder gewartet wird.
    def light_stop(self):
        self.switch.clear()
        
	#destruktor
    def __del__(self):
        print("Destruktor gestartet")

