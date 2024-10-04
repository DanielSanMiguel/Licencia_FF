# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

from flask import Flask, request, render_template, jsonify
import os
import requests
from dotenv import load_dotenv

# Cargar las variables de entorno del archivo .env
load_dotenv()

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    # Obtener datos del formulario
    nombre = request.json.get('nombre')
    club = request.json.get('club')
    puesto = request.json.get('puesto')
    email = request.json.get('email')

    # Realizar la solicitud a la API
    try:
        # Enviar la solicitud de licencia
        response = requests.post('https://flyfut.olocip.com/licenses/create', headers={
            'Content-Type': 'application/x-www-form-urlencoded',
            'admin_name': 'flyfut',
            'admin_password': os.getenv('ADMIN_PASSWORD')  # Usar variable de entorno
        }, data={
            'name': nombre,
            'club': club,
            'puesto': puesto,
            'email': email
        })

        response_data = response.json()

        # Enviar a Airtable
        airtable_response = requests.post('https://api.airtable.com/v0/appjPY2KlFg6bpcT1/List_licencias', headers={
            'Authorization': f'Bearer {os.getenv("API_KEY")}',  # Usar variable de entorno
            'Content-Type': 'application/json'
        }, json={
            'records': [{
                'fields': {
                    'Nombre': nombre,
                    'Club': club,
                    'Puesto': puesto,
                    'Email': email,
                    'Licencia': response_data.get('newLicense')
                }
            }]
        })

        return jsonify({'message': 'Licencia solicitada con éxito.'}), 200

    except Exception as e:
        return jsonify({'error': 'Error al solicitar la licencia.'}), 500

if __name__ == '__main__':
    app.run(debug=True)
