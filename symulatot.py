import string
import time
import random
import sys
import math

class Zdazenie ():
    def __init__ (self, _czas_przybycia, _id_zdazenia, _wielkosc_pakietu):
        
        self.id_zdazenia=_id_zdazenia
        self.czas_przybycia=_czas_przybycia
        self.czas_obslugi = random.expovariate(1/ _wielkosc_pakietu )
        self.czas_rozpoczecia_zdazenia=0
        self.czas_zakonczenia_zdazenia=0
        self.opuznienie = 0
        self.czas_spedzony_w_kolejce = 0
        self.status =0 # 0 stworzone, 1 kolejkowane, 2 w obsłudze 4 zakonczone

    def obsluga_zadania_w_kolejce (self, system):
        self.czas_obslugi = self.czas_obslugi
        self.czas_rozpoczecia_zdazenia=max(self.czas_przybycia, system.czas_zakonczenia_ostatniego_zdazenia)
        self.czas_zakonczenia_zdazenia=self.czas_rozpoczecia_zdazenia + self.czas_obslugi
        self.czas_spedzony_w_kolejce = self.czas_rozpoczecia_zdazenia -self.czas_przybycia
        self.opuznienie = self.czas_spedzony_w_kolejce + self.czas_obslugi


class System():
    def __init__(self, _service_rate):
        self.service_rate= _service_rate
        self.czas_zakonczenia_ostatniego_zdazenia = 0
        self.lista_zdazen = []
        self.kolejka_podsumowanie {}
    
    def obsluga_zdazenia (self, nowe_zdazenie):
        aktualny_czas = nowe_zdazenie.czas_przybycia
        self.czas_zakonczenia_ostatniego_zdazenia = nowe_zdazenie.czas_zakonczenia_zdazenia

        czy_dodano_nowe_zdazenie = False
        zakonczone_zdazenia =[]

        temp_kopia_zdazen_w_systemie =copy.copy(self.lista_zdazen)

        for zdazenie in temp_kopia_zdazen_w_systemie:
            if zdazenie.czas_rozpoczecia_zdazenia <= aktualny_czas and zdazenie.status <2:
                self.kolejka_podsumowanie[aktualny_czas] = len(self.lista_zdazen)
                zdazenie.status=2
                if zdazenie.czas_zakonczenia_zdazenia <= aktualny_czas:
                    zdazenie.status=3
                    self.lista_zdazen.remove(zdazenie)
                    self.kolejka_podsumowanie(aktualny_czas)=len(self.lista_zdazen)
                    zakonczone_zdazenia.append(zdazenie)
            else:
                continue
        elif zdazenie.czas_zakonczenia_zdazenia <= aktualny_czas and zdazenie.status==2:
            zdazenie.status = 3
            self.lista_zdazen.remove(zdazenie)
            self.kolejka_podsumowanie(aktualny_czas)=len(self.lista_zdazen)
            zakonczone_zdazenia.append(zdazenie)
    if not czy_dodano_nowe_zdazenie:
        self.lista_zdazen.append(nowe_zdazenie)
        self.kolejka_podsumowanie(aktualny_czas)=len(self.lista_zdazen)
        nowe_zdazenie.status= 1

def zakonczenie_zdazenia(self):
    temp_kopia_zdazen_w_systemie =copy.copy(self.lista_zdazen)
    aktualny_czas = TOTAL_SIMULATION_TIME

    for zdazenie in temp_kopia_zdazen_w_systemie:
        if zdazenie.status ==2:
            zdazenie.status=3
            self.lista_zdazen.remove(zdazenie)
            self.kolejka_podsumowanie(zdazenie.czas_zakonczenia_zdazenia)=len(self.lista_zdazen)
            if zdazenie.czas_zakonczenia_zdazenia > aktualny_czas:
                aktualny_czas= zdazenie.czas_zakonczenia_zdazenia
        elif zdazenie.status<2:
            self.kolejka_podsumowanie(zdazenie.czas_zakonczenia_zdazenia)= len(self.lista_zdazen)
            zdazenie.status=2

            zdazenie.status=3
            self.lista_zdazen.remove(zdazenie)
            self.kolejka_podsumowanie(zdazenie.czas_zakonczenia_zdazenia) = len (self.lista_zdazen)
            if zdazenie.czas_zakonczenia_zdazenia > aktualny_czas:
                aktualny_czas= zdazenie.czas_zakonczenia_zdazenia
    print (" Czas: " + str(aktualny_czas)  )


class Symulator:
    def __init__ (self, _arrival_rate, _service_rate):
        self.arrival_rate=_arrival_rate
        self.system = System (_service_rate)

    def run (self, _czas_symulacji ):
        print("\nCzas: 0 sec, Symulacja zaczna sie dla λ=" + str(self.arrival_rate))
        aktualny_czas = random.expovariate(self.arrival_rate)
        zdazenie = {}
        zdazenie_id = 1
        
        while  

lista_zdazen=[]
