import os
import requests
import time
from flask import Flask, render_template, jsonify
from datetime import datetime, timedelta
from dotenv import load_dotenv
from api_stats_manager import ApiStatsManager

# Cargar variables de entorno desde el archivo .env
load_dotenv()

app = Flask(__name__)

# LiveScore API credentials
LIVESCORE_API_KEY = os.getenv('LIVESCORE_API_KEY')
LIVESCORE_API_SECRET = os.getenv('LIVESCORE_API_SECRET')

# API endpoints
STANDINGS_URL = f'https://livescore-api.com/api-client/leagues/table.json?competition_id=45&group_id=3420&key={LIVESCORE_API_KEY}&secret={LIVESCORE_API_SECRET}'
LIVESCORES_URL = f'https://livescore-api.com/api-client/matches/live.json?competition_id=45&key={LIVESCORE_API_KEY}&secret={LIVESCORE_API_SECRET}'
FIXTURES_URL = f'https://livescore-api.com/api-client/fixtures/matches.json?competition_id=45&key={LIVESCORE_API_KEY}&secret={LIVESCORE_API_SECRET}'
HISTORY_URL = f'https://livescore-api.com/api-client/scores/history.json?competition_id=45&page=93&key={LIVESCORE_API_KEY}&secret={LIVESCORE_API_SECRET}'
TOPSCORERS_URL = f'https://livescore-api.com/api-client/competitions/topscorers.json?competition_id=45&key={LIVESCORE_API_KEY}&secret={LIVESCORE_API_SECRET}'

# Inicializar el administrador de estadísticas de API
api_stats = ApiStatsManager(history_intervals=48)

# Función para registrar estadísticas de API
def track_api_call(success, response_time):
    api_stats.track_api_call(success, response_time)

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
            
        track_api_call(True, response.elapsed.total_seconds())
        return jsonify(data)
    except Exception as e:
        track_api_call(False, 0)
        return jsonify({'error': str(e)}), 500

@app.route('/api/livescores')
def get_livescores():
    try:
        response = requests.get(LIVESCORES_URL)
        data = response.json()
        track_api_call(True, response.elapsed.total_seconds())
        return jsonify(data)
    except Exception as e:
        track_api_call(False, 0)
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
        
        track_api_call(True, response.elapsed.total_seconds())
        return jsonify(data)
    except Exception as e:
        track_api_call(False, 0)
        return jsonify({'error': str(e)}), 500


@app.route('/api/history')
def get_history():
    try:
        response = requests.get(HISTORY_URL)
        data = response.json()
        track_api_call(True, response.elapsed.total_seconds())
        return jsonify(data)
    except Exception as e:
        track_api_call(False, 0)
        return jsonify({'error': str(e)}), 500

@app.route('/api/results')
def get_results():
    try:
        # Usamos la misma URL que history pero con página diferente para obtener resultados más recientes
        results_url = f'https://livescore-api.com/api-client/scores/history.json?competition_id=45&page=1&key={LIVESCORE_API_KEY}&secret={LIVESCORE_API_SECRET}'
        response = requests.get(results_url)
        data = response.json()
        track_api_call(True, response.elapsed.total_seconds())
        return jsonify(data)
    except Exception as e:
        track_api_call(False, 0)
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/metrics')
def get_metrics():
    try:
        # Obtener datos reales de máximos goleadores
        topscorers_response = requests.get(TOPSCORERS_URL)
        topscorers_data = topscorers_response.json()
        
        # Obtener datos de la tabla de posiciones para extraer información de goles
        standings_response = requests.get(STANDINGS_URL)
        standings_data = standings_response.json()
        
        # Procesar datos de goles por equipo desde la tabla de posiciones
        goals_by_team = []
        if standings_data.get('success') and standings_data.get('data') and standings_data.get('data').get('table'):
            for team in standings_data['data']['table']:
                goals_by_team.append({
                    'team': team['name'],
                    'scored': team['goals_scored'],
                    'conceded': team['goals_conceded']
                })
            
            # Ordenar equipos por goles anotados (de más a menos)
            goals_by_team = sorted(goals_by_team, key=lambda x: int(x['scored']), reverse=True)
        
        # Crear objeto de respuesta con datos reales
        metrics = {
            'top_scorers': topscorers_data.get('data', {}).get('topscorers', []),
            'goals_by_team': goals_by_team
        }
        
        track_api_call(True, topscorers_response.elapsed.total_seconds())
        track_api_call(True, standings_response.elapsed.total_seconds())
        return jsonify({'success': True, 'data': metrics})
    except Exception as e:
        track_api_call(False, 0)
        track_api_call(False, 0)
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/dashboard')
def get_dashboard():
    try:
        # Obtener datos reales de partidos jugados
        total_matches = 0
        
        # Obtener datos de resultados para contar partidos jugados
        results_url = f'https://livescore-api.com/api-client/scores/history.json?competition_id=45&key={LIVESCORE_API_KEY}&secret={LIVESCORE_API_SECRET}'
        results_response = requests.get(results_url)
        results_data = results_response.json()
        
        # Contar partidos de la primera página
        if results_data.get('success') and results_data.get('data') and results_data.get('data').get('match'):
            total_matches += len(results_data['data']['match'])
            
            # Obtener el número total de páginas
            total_pages = results_data.get('data', {}).get('total_pages', 1)
            
            # Si hay más páginas, consultar la última para estimar el total
            if total_pages > 1:
                # Obtener datos de la última página
                last_page_url = f'https://livescore-api.com/api-client/scores/history.json?competition_id=45&page={total_pages}&key={LIVESCORE_API_KEY}&secret={LIVESCORE_API_SECRET}'
                last_page_response = requests.get(last_page_url)
                last_page_data = last_page_response.json()
                
                if last_page_data.get('success') and last_page_data.get('data') and last_page_data.get('data').get('match'):
                    # Calcular el total estimado de partidos
                    matches_per_page = len(results_data['data']['match'])  # Partidos en la primera página
                    last_page_matches = len(last_page_data['data']['match'])  # Partidos en la última página
                    
                    # Estimar el total: (páginas completas * partidos por página) + partidos de la última página
                    total_matches = ((total_pages - 1) * matches_per_page) + last_page_matches
        
        # Obtener datos del dashboard desde el administrador de estadísticas
        dashboard_data = api_stats.get_dashboard_data()
        
        # Agregar el total de partidos
        dashboard_data['total_matches'] = total_matches
        
        # Registrar las llamadas a la API
        track_api_call(True, results_response.elapsed.total_seconds())
        if 'last_page_response' in locals():
            track_api_call(True, last_page_response.elapsed.total_seconds())
        
        return jsonify({'success': True, 'data': dashboard_data})
    except Exception as e:
        track_api_call(False, 0)
        return jsonify({'success': False, 'error': str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
