#Autoren: 					Alexander Luft (23945)
#Datum:						30.08.2019
#Dozent: 					Prof. Dr. O. Drögehorn
#Veranstaltung/Semester: 	Future Internet/ Digitales Kulturerbe Anwendungspraktikum /Sommersemester 2019


from lightShow import LightBand
from audioPlayer import AudioPlayer

# Diese Klasse Kapselt die beiden Thread-Klassen die für die Wiedergabe von Musik und dem erleuchten des LED-Bandes zuständig sind
class WolfDefense(object):
    
	# Erstellung der Thread-Klassen im Konstruktor 
    def __init__(self):
        self.audio = AudioPlayer()
        self.light = LightBand()
        
	# Aktivierung der Abwehrmaßnahmen
    def activate_defense(self):
        
		# Sollte der Thread schon laufen, wird nurnoch das Semaphore freigegeben, ansonsten wird der Thread gestartet und der Semaphore wird freigegeben 
        if self.audio.is_alive() is True:
            self.audio.sound_play()
        else:
            self.audio.start()
            self.audio.sound_play()
     
        if self.light.is_alive() is True:
            self.light.light_play()
        else:
            self.light.start()
            self.light.light_play()
        
	# Wen nder Thread läuft, wird druch diese MEthode das Semaphore wieder blockiert
    def deactivate_defense(self):
        if self.audio.is_alive() is True:
            self.audio.sound_stop()
            
        if self.audio.is_alive() is True:
            self.light.light_stop()