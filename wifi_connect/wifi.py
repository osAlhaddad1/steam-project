import network
import time
# Wi-Fi Configuratie: vul je Wi-Fi SSID en wachtwoord in
SSID = 'Lotwifi'
PASSWORD = 'Wachtwoord?'


# Verbinden met Wi-Fi
def connect_wifi():
    wlan = network.WLAN(network.STA_IF)  # Maak gebruik van de stationmodus (STA)
    wlan.active(True)  # Activeer de Wi-Fi
    wlan.disconnect()  # Zorg dat er geen eerdere verbindingen actief zijn
    wlan.connect(SSID, PASSWORD)  # Maak verbinding met het netwerk

    max_retries = 20
    retries = 0

    while not wlan.isconnected() and retries < max_retries:
        retries += 1
        print(f"Connecting to Wi-Fi... Retry {retries} of {max_retries}")
        time.sleep(1)  # Wacht 1 seconde tussen pogingen

    if wlan.isconnected():
        ip = wlan.ifconfig()[0]  # Haal het IP-adres op
        print("Connected to Wi-Fi!")
        print(f"IP Address: {ip}")
        return True
    else:
        print("Failed to connect to Wi-Fi.")
        return False