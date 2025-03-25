import os
import requests
from flask import Flask, render_template, jsonify

app = Flask(__name__)

# LiveScore API credentials
LIVESCORE_API_KEY = 'ffzVfpbpm1R8Xfgc'
LIVESCORE_API_SECRET = '0kD5SHLJlkljEcjUrSPGi05E1WNZc3cc'

# API endpoints
STANDINGS_URL = f'https://livescore-api.com/api-client/leagues/table.json?competition_id=45&group_id=3420&key={LIVESCORE_API_KEY}&secret={LIVESCORE_API_SECRET}'
LIVESCORES_URL = f'https://livescore-api.com/api-client/matches/live.json?competition_id=45&key={LIVESCORE_API_KEY}&secret={LIVESCORE_API_SECRET}'
FIXTURES_URL = f'https://livescore-api.com/api-client/fixtures/matches.json?competition_id=45&key={LIVESCORE_API_KEY}&secret={LIVESCORE_API_SECRET}'
HISTORY_URL = f'https://livescore-api.com/api-client/scores/history.json?competition_id=45&page=93&key={LIVESCORE_API_KEY}&secret={LIVESCORE_API_SECRET}'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/standings')
def get_standings():
    try:
        response = requests.get(STANDINGS_URL)
        data = response.json()
        
        # If we need additional filtering for stage_id
        if data.get('success') and data.get('data') and data.get('data').get('table'):
            # The API request already includes stage_id=3105, but we can add additional filtering here if needed
            pass
            
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/livescores')
def get_livescores():
    try:
        response = requests.get(LIVESCORES_URL)
        data = response.json()
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


#Actualizar cada lunes
@app.route('/api/fixtures')
def get_fixtures():
    try:
        response = requests.get(FIXTURES_URL)
        data = response.json()
        
        # Verifica que la respuesta tenga el campo "fixtures"
        if data.get("success") and "data" in data and "fixtures" in data["data"]:
            fixtures = data["data"]["fixtures"]
            # Filtra solo los partidos cuyo round sea "13"
            filtered_fixtures = [fixture for fixture in fixtures if fixture.get("round") == "13"]
            data["data"]["fixtures"] = filtered_fixtures
        
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/history')
def get_history():
    try:
        response = requests.get(HISTORY_URL)
        data = response.json()
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/results')
def get_results():
    try:
        # Usamos la misma URL que history pero con página diferente para obtener resultados más recientes
        results_url = f'https://livescore-api.com/api-client/scores/history.json?competition_id=45&page=1&key={LIVESCORE_API_KEY}&secret={LIVESCORE_API_SECRET}'
        response = requests.get(results_url)
        data = response.json()
        return jsonify(data)
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
