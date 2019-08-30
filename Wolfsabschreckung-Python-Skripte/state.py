#Autoren: 					Alexander Luft (23945)
#Datum:						30.08.2019
#Dozent: 					Prof. Dr. O. Drögehorn
#Veranstaltung/Semester: 	Future Internet/ Digitales Kulturerbe Anwendungspraktikum /Sommersemester 2019

import time
import RPi.GPIO as GPIO
import threading
from time import sleep
import pygame

 

# Import the WS2801 module.

import Adafruit_WS2801

import Adafruit_GPIO.SPI as SPI

# Statuswiedergabe des Python-Programms durch aufleuchten des Lichtbandes in verscheidenen Farben
class StateOfPi(object):

    def __init__(self):
        
        self.PIXEL_COUNT = 32  #Anzahl der LEDS auf dem Lichtband

        self.SPI_PORT   = 0
        self.SPI_DEVICE = 0
		#Erstellen eines Objektes, das die RGB LEDS des Lichtbandes ansteuern kann, dafür muss die Anzahl der LEDs auf dem Lichtband übergeben werden, genauso wie der SD und der CK Pin Anschluss, diese werden durch das SPI.SpiDev vom Programm selbst ermittelt
        self.pixels = Adafruit_WS2801.WS2801Pixels(self.PIXEL_COUNT, spi=SPI.SpiDev(self.SPI_PORT, self.SPI_DEVICE), gpio=GPIO)
    
	
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
            
	# LED-Band blinkt in der Farbe des Methodennamens
    def blink_blue(self):
        self.blink_color(self.pixels, blink_times = 1, color=(255, 0, 0))
        
    def blink_yellow(self):
        self.blink_color(self.pixels, blink_times = 1, color=(0, 255, 255))
        
    def blink_green(self):
        self.blink_color(self.pixels, blink_times = 1, color=(0, 255, 0))
        
    def blink_red(self):
        self.blink_color(self.pixels, blink_times = 1, color=(0, 0, 255))
        
        