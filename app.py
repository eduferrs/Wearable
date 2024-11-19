from flask import Flask, request, jsonify, render_template
import json

app = Flask(__name__)

latest_coordinates = {"lat": None, "lng": None}
led_states = {"led1": "off", "led2": "off"}

#Rota para receber as coordenadas
@app.route('/api/coordenadas', methods=['POST'])
def receive_coordinates():
    global latest_coordinates
    data = request.get_json()
    if data:
        latest_coordinates["lat"] = data.get("lat")
        latest_coordinates["lng"] = data.get("lng")
        print("Dados recebidos:", latest_coordinates)
        return jsonify({"status": "success"}), 200
    else:
        print("Erro: Dados não recebidos corretamente.")
        return jsonify({"status": "fail", "error": "Invalid data"}), 400

#Rota para as últimas coordenadas
@app.route('/api/latest_coordinates', methods=['GET'])
def get_latest_coordinates():
    return jsonify(latest_coordinates)

#Rota para controlar o LED1
@app.route('/api/led1', methods=['POST'])
def control_led1():
    state = request.json.get("state", "off")
    led_states["led1"] = state
    return jsonify({"status": "success", "led1": state}), 200

#Rota para controlar o LED2
@app.route('/api/led2', methods=['POST'])
def control_led2():
    state = request.json.get("state", "off")
    led_states["led2"] = state
    return jsonify({"status": "success", "led2": state}), 200

#Rota para fornecer o estado dos LEDs
@app.route('/api/led_states', methods=['GET'])
def get_led_states():
    return jsonify(led_states)

#Rota da página
@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
