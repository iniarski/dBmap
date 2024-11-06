from machine import ADC, Pin
import machine
from network import WLAN
import time
import ujson

# Konfiguracja ADC i mikrofonu
adc = ADC()              # Inicjalizacja ADC
mic_pin = adc.channel(pin='P13')  # Ustawienie pinu na mikrofonie

wlan = WLAN(mode=WLAN.STA) # Inicjalizacja WiFi

wlan.connect(ssid="ssid", auth=(WLAN.WPA2, 'password')) # Ustawienie ssid i metoda autentykacji

# TODO
# przetestowac predkosci na kampusie, zobaczyc czy nie bedzie trzeba uzyc sieci z wieksza predkoscia. 

while not wlan.isconnected():
    machine.idle()
print("Wifi connected")
print(wlan.ifconfig())

def read_sound_level():
    # Przykład dla 100 odczytów na sekundę
    num_samples = 100
    total = 0

    for _ in range(num_samples):
        sample = mic_pin()  # Odczyt wartości z mikrofonu
        total += sample
        time.sleep(0.01)

    avg_level = total / num_samples  # Obliczanie średniego poziomu
    return avg_level
# TODO
# Dostroic kod aby wyrzucal wartosci w dB, na ten moment to nie wiem w czym to wypluwa.

def save_to_json(data, filename="sound_levels.json"):
    try:
        with open(filename, "w") as file:
            ujson.dump(data, file)
    except Exception as e:
        print("Błąd zapisu do pliku JSON:", e)

# Lista do przechowywania pomiarów
sound_data = []

while True:
    sound_level = read_sound_level()
    print("Poziom dźwięku:", sound_level)
    
    # Dodanie pomiaru do listy
    sound_data.append({
        "timestamp": time.time(),
        "sound_level": sound_level
    })
    
    # Zapis pomiarów do pliku co 10 sekund
    if len(sound_data) >= 10:
        save_to_json(sound_data)
        sound_data = []  # Wyczyść listę po zapisie
    
    time.sleep(1)
# TODO
# Dogadac sie z backendem czy to jest dobra forma

# Funkcja wysylajaca na serwer, prawdopodobnie uzyjemy protokolu mqtt