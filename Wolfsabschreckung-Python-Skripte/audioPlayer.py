#Autoren: 					Alexander Luft (23945)
#Datum:						30.08.2019
#Dozent: 					Prof. Dr. O. Drögehorn
#Veranstaltung/Semester: 	Future Internet/ Digitales Kulturerbe Anwendungspraktikum /Sommersemester 2019

import pygame
import random
import threading
from time import sleep

#der Audioplayer spielt im Hintergrund eines laufenden Pythonprogramms Musik durch die pygame Bibliothek ab, durch Semaphore wird der Ablauf des Programm nach dem Start gesteuert 
class AudioPlayer(threading.Thread):
    
	#Konstruktor, der bei der Erstellung des Objektes die Musikdateien die im selbem Ordner liegen wie dieses Skript in eine Playlist lädt
	#außerdem wird ein Switch (Semaphore) durch die übergabe des thread Events erstellt
    def __init__(self):
        threading.Thread.__init__(self)
        pygame.mixer.init()
        self.playlist = list()
        self.playlist.append("artillery.wav")
        self.playlist.append("bear.wav")
        self.playlist.append("cardoor.wav")
        self.playlist.append("carhorn.wav")
        self.playlist.append("rattat.wav")
        self.playlist.append("shotgun.wav")
        
        self.switch = threading.Event()
        random.seed()
        
    # spielt die Musik in der playlist ab und legt die Lautstärke fest, dabei wird immer ein Zufälliges lied durch die random.choice Methode aus der Playlist ausgewählt 
    def playSound(self):
        pygame.mixer.music.load(random.choice(self.playlist))
        pygame.mixer.music.set_volume(1.0)
        pygame.mixer.music.play()
        
            
	# Start-Methode der Threadklasse, in der Schleife wird solange durch das switch.wait gewartet, bis es durch die Methode sound_play freigegeben wird
    def run(self):
        
         while True:
            self.switch.wait()
            self.playSound()
            sleep(3)
            
	# gibt den switch frei
    def sound_play(self):
        self.switch.set()
        
	# blockiert den switch, so das in der run-Methode in der schleife wieder gewartet wird.
    def sound_stop(self):
        self.switch.clear()
    
    
    #destruktor
    def __del__(self):
        print("Destruktor gestartet")