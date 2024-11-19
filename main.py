import machine
import network
import json
from time import sleep, time
from micropyGPS import MicropyGPS
import urequests

led1 = machine.Pin(21, machine.Pin.OUT)
led2 = machine.Pin(18, machine.Pin.OUT)

def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect('NOME_DA_REDE', 'SENHA')                   ##############
    while not wlan.isconnected():
        sleep(1)
    print('Conectado ao Wi-Fi:', wlan.ifconfig())

gps = MicropyGPS()

#Leitura e envio dos dados do gps
def update_gps_data():
    gps_serial = machine.UART(2, baudrate=9600, tx=17, rx=16)
    start_time = time()
    timeout = 3

    while time() - start_time < timeout:
        if gps_serial.any():
            data = gps_serial.read()
            for byte in data:
                gps.update(chr(byte))
                if gps.valid:
                    lat = gps.latitude[0] + gps.latitude[1] / 60.0
                    lon = gps.longitude[0] + gps.longitude[1] / 60.0
                    if gps.latitude[2] == 'S':
                        lat = -lat
                    if gps.longitude[2] == 'W':
                        lon = -lon
                    send_coordinates(lat, lon)
                    return
        sleep(0.1)


def send_coordinates(lat, lon):
    url = 'ENDERECO_SERVIDOR/api/coordenadas'                       #################
    headers = {'Content-Type': 'application/json'}
    data = json.dumps({'lat': lat, 'lng': lon})
    try:
        response = urequests.post(url, data=data, headers=headers, timeout=20)
        print("Resposta do servidor:", response.text)
        response.close()
    except Exception as e:
        print("Erro ao enviar dados:", e)
    sleep(2)

#Obter estado e controlar leds
def update_leds():
    url = 'ENDERECO_SERVIDOR/api/led_states'                        #################
    try:
        response = urequests.get(url)
        led_states = response.json()
        response.close()
        print("Estado dos LEDs:", led_states)
        
        if led_states.get("led1") == "on":
            for _ in range(3):  
                led1.value(1)
                sleep(0.5)
                led1.value(0)
                sleep(0.5)
        else:
            led1.value(0)

        if led_states.get("led2") == "on":
            for _ in range(3):  
                led2.value(1)
                sleep(0.5)
                led2.value(0)
                sleep(0.5)
        else:
            led2.value(0)

    except Exception as e:
        print("Erro ao atualizar LEDs:", e)
    sleep(0.5)


connect_wifi()
while True:
    update_leds()     
    update_gps_data()  
    sleep(1)           
