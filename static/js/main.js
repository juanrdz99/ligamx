// Función para crear los gráficos del dashboard
function createDashboardCharts(dashboardData) {
    console.log('Creando gráficos con datos:', dashboardData);
    
    // Obtener los datos de las últimas 12 horas para una visualización más relevante
    const hours = dashboardData.hours.slice(-12);
    const apiTrend = {
        calls: dashboardData.api_trend.calls.slice(-12),
        success_rate: dashboardData.api_trend.success_rate.slice(-12),
        response_time: dashboardData.api_trend.response_time.slice(-12),
        errors: dashboardData.api_trend.errors.slice(-12)
    };
    
    console.log('Datos procesados para gráficas:', { hours, apiTrend });
    
    // Configuración para mostrar solo algunas etiquetas en el eje X cuando hay muchas horas
    const skipLabels = Math.ceil(hours.length / 6); // Mostrar aproximadamente 6 etiquetas
    
    // Función para determinar si mostrar una etiqueta basada en su índice
    const skipLabelsCallback = function(value, index) {
        return index % skipLabels === 0 ? hours[index] : '';
    };
    
    // Destruir gráficas existentes si existen para evitar problemas de duplicación
    if (window.callsChart) {
        window.callsChart.destroy();
        window.callsChart = null;
    }
    if (window.successRateChart) {
        window.successRateChart.destroy();
        window.successRateChart = null;
    }
    if (window.responseTimeChart) {
        window.responseTimeChart.destroy();
        window.responseTimeChart = null;
    }
    if (window.errorsChart) {
        window.errorsChart.destroy();
        window.errorsChart = null;
    }
    
    try {
        // Gráfico de Llamadas API
        const callsChartElement = document.getElementById('calls-chart');
        if (!callsChartElement) {
            console.error('No se encontró el elemento canvas para el gráfico de llamadas API');
            return;
        }
        
        const callsCtx = callsChartElement.getContext('2d');
        window.callsChart = new Chart(callsCtx, {
            type: 'line',
            data: {
                labels: hours,
                datasets: [{
                    label: 'Llamadas API',
                    data: apiTrend.calls,
                    backgroundColor: 'rgba(54, 162, 235, 0.2)',
                    borderColor: 'rgba(54, 162, 235, 1)',
                    borderWidth: 2,
                    tension: 0.4,
                    pointRadius: 3,
                    pointHoverRadius: 6,
                    fill: true
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                animation: {
                    duration: 1000,
                    easing: 'easeOutQuart'
                },
                scales: {
                    x: {
                        title: {
                            display: true,
                            text: 'últimas 12 horas',
                            font: {
                                weight: 'bold'
                            }
                        },
                        ticks: {
                            callback: skipLabelsCallback,
                            font: {
                                size: 10
                            }
                        },
                        grid: {
                            display: false
                        }
                    },
                    y: {
                        beginAtZero: true,
                        title: {
                            display: true,
                            text: 'Número de llamadas',
                            font: {
                                weight: 'bold'
                            }
                        },
                        ticks: {
                            precision: 0
                        }
                    }
                },
                plugins: {
                    legend: {
                        display: true,
                        position: 'top'
                    },
                    tooltip: {
                        callbacks: {
                            title: function(context) {
                                return 'Hora: ' + context[0].label;
                            },
                            label: function(context) {
                                return 'Llamadas: ' + context.raw;
                            }
                        },
                        backgroundColor: 'rgba(0, 0, 0, 0.7)',
                        padding: 10,
                        cornerRadius: 6
                    }
                }
            }
        });
        console.log('Gráfico de llamadas API creado exitosamente');
        
        // Gráfico de Tasa de Éxito
        const successRateCtx = document.getElementById('success-rate-chart').getContext('2d');
        window.successRateChart = new Chart(successRateCtx, {
            type: 'bar',
            data: {
                labels: hours,
                datasets: [{
                    label: 'Tasa de Éxito (%)',
                    data: apiTrend.success_rate,
                    backgroundColor: 'rgba(75, 192, 192, 0.2)',
                    borderColor: 'rgba(75, 192, 192, 1)',
                    borderWidth: 2
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                animation: {
                    duration: 1000,
                    easing: 'easeOutQuart'
                },
                scales: {
                    x: {
                        title: {
                            display: true,
                            text: 'últimas 12 horas',
                            font: {
                                weight: 'bold'
                            }
                        },
                        ticks: {
                            callback: skipLabelsCallback,
                            font: {
                                size: 10
                            }
                        },
                        grid: {
                            display: false
                        }
                    },
                    y: {
                        beginAtZero: true,
                        max: 100,
                        title: {
                            display: true,
                            text: 'Porcentaje',
                            font: {
                                weight: 'bold'
                            }
                        }
                    }
                },
                plugins: {
                    legend: {
                        display: true,
                        position: 'top'
                    },
                    tooltip: {
                        callbacks: {
                            title: function(context) {
                                return 'Hora: ' + context[0].label;
                            },
                            label: function(context) {
                                return 'Tasa de éxito: ' + context.raw.toFixed(1) + '%';
                            }
                        },
                        backgroundColor: 'rgba(0, 0, 0, 0.7)',
                        padding: 10,
                        cornerRadius: 6
                    }
                }
            }
        });
        
        // Gráfico de Tiempo de Respuesta
        const responseTimeCtx = document.getElementById('response-time-chart').getContext('2d');
        window.responseTimeChart = new Chart(responseTimeCtx, {
            type: 'line',
            data: {
                labels: hours,
                datasets: [{
                    label: 'Tiempo de Respuesta (ms)',
                    data: apiTrend.response_time.map(time => time * 1000), // Convertir a milisegundos
                    backgroundColor: 'rgba(255, 206, 86, 0.2)',
                    borderColor: 'rgba(255, 206, 86, 1)',
                    borderWidth: 2,
                    tension: 0.4,
                    pointRadius: 3,
                    pointHoverRadius: 6,
                    fill: true
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                animation: {
                    duration: 1000,
                    easing: 'easeOutQuart'
                },
                scales: {
                    x: {
                        title: {
                            display: true,
                            text: 'últimas 12 horas',
                            font: {
                                weight: 'bold'
                            }
                        },
                        ticks: {
                            callback: skipLabelsCallback,
                            font: {
                                size: 10
                            }
                        },
                        grid: {
                            display: false
                        }
                    },
                    y: {
                        beginAtZero: true,
                        title: {
                            display: true,
                            text: 'Milisegundos',
                            font: {
                                weight: 'bold'
                            }
                        }
                    }
                },
                plugins: {
                    legend: {
                        display: true,
                        position: 'top'
                    },
                    tooltip: {
                        callbacks: {
                            title: function(context) {
                                return 'Hora: ' + context[0].label;
                            },
                            label: function(context) {
                                return 'Tiempo: ' + context.raw.toFixed(1) + ' ms';
                            }
                        },
                        backgroundColor: 'rgba(0, 0, 0, 0.7)',
                        padding: 10,
                        cornerRadius: 6
                    }
                }
            }
        });
        
        // Gráfico de Errores
        const errorsCtx = document.getElementById('errors-chart').getContext('2d');
        window.errorsChart = new Chart(errorsCtx, {
            type: 'bar',
            data: {
                labels: hours,
                datasets: [{
                    label: 'Errores',
                    data: apiTrend.errors,
                    backgroundColor: 'rgba(255, 99, 132, 0.2)',
                    borderColor: 'rgba(255, 99, 132, 1)',
                    borderWidth: 2
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                animation: {
                    duration: 1000,
                    easing: 'easeOutQuart'
                },
                scales: {
                    x: {
                        title: {
                            display: true,
                            text: 'últimas 12 horas',
                            font: {
                                weight: 'bold'
                            }
                        },
                        ticks: {
                            callback: skipLabelsCallback,
                            font: {
                                size: 10
                            }
                        },
                        grid: {
                            display: false
                        }
                    },
                    y: {
                        beginAtZero: true,
                        title: {
                            display: true,
                            text: 'Número de errores',
                            font: {
                                weight: 'bold'
                            }
                        },
                        ticks: {
                            precision: 0
                        }
                    }
                },
                plugins: {
                    legend: {
                        display: true,
                        position: 'top'
                    },
                    tooltip: {
                        callbacks: {
                            title: function(context) {
                                return 'Hora: ' + context[0].label;
                            },
                            label: function(context) {
                                return 'Errores: ' + context.raw;
                            }
                        },
                        backgroundColor: 'rgba(0, 0, 0, 0.7)',
                        padding: 10,
                        cornerRadius: 6
                    }
                }
            }
        });
    } catch (error) {
        console.error('Error creando gráficos:', error);
    }
} // Agregar la llave de cierre faltante aquí

// Helper function to format date with 6 hours subtracted
function formatDate(dateString) {
    if (!dateString || dateString === 'Sin fecha') return 'Fecha no disponible';
    
    const options = { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' };
    try {
        const date = new Date(dateString);
        // Restar 6 horas a la fecha
        date.setHours(date.getHours() - 6);
        return date.toLocaleDateString('es-MX', options);
    } catch (e) {
        return dateString;
    }
}

// Helper function to format time
function formatTime(timeString) {
    if (!timeString) return '';
    
    const timeParts = timeString.split(':');
    if (timeParts.length < 2) return timeString;
    
    let hours = parseInt(timeParts[0]);
    const minutes = parseInt(timeParts[1]);
    
    // Ajustar a zona horaria de Ciudad de México (UTC-6)
    hours = (hours - 6 + 24) % 24;
    
    // Convertir a formato 12 horas
    const formattedTime = `${hours % 12 || 12}:${minutes.toString().padStart(2, '0')} ${hours < 12 ? 'AM' : 'PM'}`;
    
    return formattedTime;
}

// Función para obtener el logo de un equipo usando el mapeo global
function getTeamLogo(teamName) {
    // Manejar casos especiales primero
    if (teamName.includes('Juárez') || teamName.includes('Juarez')) {
        return `<img src="/static/img/logos/juarez.png" alt="${teamName}" class="team-logo" onerror="this.style.display='none'">`;  
    } else if (teamName.includes('Guadalajara') || teamName.includes('Chivas')) {
        return `<img src="/static/img/logos/guadalajara.png" alt="${teamName}" class="team-logo" onerror="this.style.display='none'">`;  
    } else if (teamName.includes('América') || teamName.includes('America')) {
        return `<img src="/static/img/logos/america.png" alt="${teamName}" class="team-logo" onerror="this.style.display='none'">`;  
    } else if (teamName.includes('Querétaro') || teamName.includes('Queretaro')) {
        return `<img src="/static/img/logos/queretaro.png" alt="${teamName}" class="team-logo" onerror="this.style.display='none'">`;  
    }
    
    // Usamos el mismo mapeo que se usa en displayStandings
    const logoFileName = window.teamLogoMap[teamName] || teamName.toLowerCase().replace(/ /g, '');
    const logoPath = `/static/img/logos/${logoFileName}.png`;
    return `<img src="${logoPath}" alt="${teamName}" class="team-logo" onerror="this.style.display='none'">`;  
}

// Ejecutar cuando el documento esté listo
document.addEventListener('DOMContentLoaded', function() {
    // Cargar el contenido inicial
    loadInitialContent();
    
    // Agregar event listeners para los clicks en las pestañas
    document.getElementById('standings-tab').addEventListener('click', function() {
        loadStandings();
    });
    
    document.getElementById('fixtures-tab').addEventListener('click', function() {
        loadFixtures();
    });
    
    document.getElementById('history-tab').addEventListener('click', function() {
        loadHistory();
    });
    
    document.getElementById('metrics-tab').addEventListener('click', function() {
        loadMetrics();
    });
    
    document.getElementById('dashboard-tab').addEventListener('click', function() {
        loadDashboard();
    });
});

// Function to load standings data
function loadStandings() {
    fetch('/api/standings')
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}, Text: ${response.statusText}`);
            }
            return response.json();
        })
        .then(data => {
            if (data.success && data.data && data.data.table) {
                displayStandings(data.data.table);
            } else {
                console.error('API error:', data);
                showError('standings-body', `No se pudieron cargar los datos de la tabla. ${data.error || ''}`);
            }
        })
        .catch(error => {
            console.error('Error fetching standings:', error.toString());
            showError('standings-body', 'Error al cargar los datos. Por favor, intente más tarde.');
        });
}

// Function to display standings data
function displayStandings(tableData) {
    const tableBody = document.getElementById('standings-body');
    tableBody.innerHTML = '';
    
    // Mapeo de nombres de equipos a nombres de archivo de logo
    // Hacemos que el mapeo sea accesible globalmente
    window.teamLogoMap = {
        'América': 'america',
        'America': 'america',
        'Club America': 'america',
        'León': 'leon',
        'Leon': 'leon',
        'Club Leon': 'leon',
        'Tigres UANL': 'tigres',
        'Tigres': 'tigres',
        'Toluca': 'toluca',
        'Deportivo Toluca': 'toluca',
        'Cruz Azul': 'cruzazul',
        'Necaxa': 'necaxa',
        'Club Necaxa': 'necaxa',
        'Pachuca': 'pachuca',
        'CF Pachuca': 'pachuca',
        'Monterrey': 'monterrey',
        'CF Monterrey': 'monterrey',
        'Juárez': 'juarez',
        'Juarez': 'juarez',
        'FC Juárez': 'juarez',
        'Guadalajara': 'guadalajara',
        'Chivas': 'guadalajara',
        'CD Guadalajara': 'guadalajara',
        'Pumas UNAM': 'pumas',
        'Pumas': 'pumas',
        'Mazatlán': 'mazatlan',
        'Mazatlan': 'mazatlan',
        'FC Mazatlan': 'mazatlan',
        'Atlas': 'atlas',
        'Atlas FC': 'atlas',
        'Querétaro': 'queretaro',
        'Queretaro': 'queretaro',
        'Atlético San Luis': 'atleticosl',
        'Atletico San Luis': 'atleticosl',
        'San Luis': 'atleticosl',
        'Puebla': 'puebla',
        'Club Puebla': 'puebla',
        'Santos Laguna': 'santos',
        'Santos': 'santos',
        'Tijuana': 'tijuana',
        'Club Tijuana': 'tijuana',
        'Xolos': 'tijuana'
    };
    
    tableData.forEach((team, index) => {
        const row = document.createElement('tr');
        
        // Agregar color de fondo según la posición
        let positionClass = '';
        if (index < 4) positionClass = 'bg-liguilla'; 
        else if (index < 12) positionClass = 'bg-repechaje'; 
        
        // Obtener el nombre del logo usando el mapeo
        let logoFileName = window.teamLogoMap[team.name] || team.name.toLowerCase().replace(/ /g, '');
        const logoPath = `/static/img/logos/${logoFileName}.png`;
        
        row.innerHTML = `
            <td class="${positionClass}">${team.rank}</td>
            <td>
                <img src="${logoPath}" alt="${team.name}" class="team-logo" onerror="this.style.display='none'">
                <span class="team-name">${team.name}</span>
            </td>
            <td>${team.matches}</td>
            <td>${team.won}</td>
            <td>${team.drawn}</td>
            <td>${team.lost}</td>
            <td>${team.goals_scored}</td>
            <td>${team.goals_conceded}</td>
            <td>${team.goal_diff}</td>
            <td class="fw-bold">${team.points}</td>
        `;
        
        tableBody.appendChild(row);
    });
}

// Function to load fixtures
function loadFixtures() {
    const container = document.getElementById('fixtures-container');
    container.innerHTML = '<div class="text-center"><div class="loading-spinner"></div><p>Cargando próximos partidos...</p></div>';
    
    fetch('/api/fixtures')
        .then(response => response.json())
        .then(data => {
            if (data.success && data.data.fixtures) {
                displayMatches(data.data.fixtures, 'fixtures-container', 'próximos');
            } else {
                container.innerHTML = '<div class="alert alert-info">No hay próximos partidos programados.</div>';
            }
        })
        .catch(error => {
            console.error('Error fetching fixtures:', error);
            container.innerHTML = '<div class="alert alert-danger">Error al cargar los datos. Por favor, intente más tarde.</div>';
        });
}

// Function to load match history
function loadHistory() {
    const container = document.getElementById('history-container');
    container.innerHTML = '<div class="text-center"><div class="loading-spinner"></div><p>Cargando resultados...</p></div>';
    
    fetch('/api/history')
        .then(response => response.json())
        .then(data => {
            if (data.success && data.data.match) {
                displayMatches(data.data.match, 'history-container', 'resultados');
            } else {
                container.innerHTML = '<div class="alert alert-info">No hay resultados disponibles.</div>';
            }
        })
        .catch(error => {
            console.error('Error fetching history:', error);
            container.innerHTML = '<div class="alert alert-danger">Error al cargar los datos. Por favor, intente más tarde.</div>';
        });
}

// Nueva función para cargar resultados recientes
function loadResults() {
    const container = document.getElementById('history-container');
    container.innerHTML = '<div class="text-center"><div class="loading-spinner"></div><p>Cargando resultados recientes...</p></div>';
    
    fetch('/api/results')
        .then(response => response.json())
        .then(data => {
            if (data.success && data.data.fixtures && data.data.fixtures.length > 0) {
                displayMatches(data.data.fixtures, 'history-container', 'resultados');
            } else {
                loadHistory();
            }
        })
        .catch(error => {
            console.error('Error fetching recent results:', error);
            loadHistory();
        });
}

// Function to display matches (used for live, fixtures, and history)
function displayMatches(matches, containerId, type) {
    const container = document.getElementById(containerId);
    container.innerHTML = '';
    
    if (!matches || matches.length === 0) {
        container.innerHTML = `<div class="alert alert-info">No hay ${type} disponibles.</div>`;
        return;
    }
    
    // Agrupar partidos por fecha
    const matchesByDate = {};
    matches.forEach(match => {
        let date = match.date || 'Sin fecha';
        
        // Caso especial: Si es el partido Santos Laguna vs Atlético San Luis, mover a domingo
        if ((match.home_name === 'Santos Laguna' && match.away_name === 'Atlético San Luis') ||
            (match.home_name === 'Santos Laguna' && match.away_name === 'Atletico San Luis') ||
            (match.away_name === 'Santos Laguna' && match.home_name === 'Atlético San Luis') ||
            (match.away_name === 'Santos Laguna' && match.home_name === 'Atletico San Luis')) {
            
            // Convertir la fecha a objeto Date
            const matchDate = new Date(date);
            
            // Si no es domingo (0 es domingo en JavaScript)
            if (matchDate.getDay() !== 0) {
                // Calcular cuántos días hay que sumar para llegar al próximo domingo
                const daysToAdd = (7 - matchDate.getDay()) % 7;
                matchDate.setDate(matchDate.getDate() + daysToAdd);
                
                // Actualizar la fecha
                date = matchDate.toISOString().split('T')[0];
            }
        }
        
        if (!matchesByDate[date]) {
            matchesByDate[date] = [];
        }
        matchesByDate[date].push(match);
    });
    
    // Crear tarjetas de partidos agrupados por fecha
    for (const date in matchesByDate) {
        const dateHeader = document.createElement('h4');
        dateHeader.className = 'mt-4 mb-3';
        dateHeader.textContent = formatDate(date);
        container.appendChild(dateHeader);
        
        const matchesGroup = document.createElement('div');
        matchesGroup.className = 'row';
        
        matchesByDate[date].forEach(match => {
            const matchCard = document.createElement('div');
            matchCard.className = 'col-md-6 col-lg-4 mb-3';
            
            let statusClass = 'status-upcoming';
            let statusText = 'Programado';
            let scoreDisplay = '-';
            
            // Determinar el estado del partido y el marcador a mostrar
            if (match.status === 'IN PLAY' || match.status === 'LIVE') {
                statusClass = 'status-live';
                statusText = 'En Vivo';
                scoreDisplay = match.score || '-';
            } else if (match.status === 'FINISHED' || match.ft_score) {
                statusClass = 'status-finished';
                statusText = 'Finalizado';
                scoreDisplay = match.ft_score || match.score || '-';
            }
            
            // Formatear la hora del partido
            const matchTime = match.time ? formatTime(match.time) : '';
            
            matchCard.innerHTML = `
                <div class="match-card p-3 text-center">
                    <!-- Encabezado con estado -->
                    <div class="d-flex justify-content-between align-items-center mb-2">
                        <span class="badge bg-success">${statusText}</span>
                    </div>
                    
                    <!-- Contenedor de equipos y marcador -->
                    <div class="match-teams-container">
                        <!-- Equipo local -->
                        <div class="team-container">
                            <div class="team-logo-container mb-2">
                                ${getTeamLogo(match.home_name)}
                            </div>
                            <div class="team-name fw-bold">${match.home_name}</div>
                        </div>
                        
                        <!-- Marcador -->
                        <div class="score-container">
                            <div class="score fw-bold">${scoreDisplay}</div>
                            <div class="match-time small text-muted">${matchTime}</div>
                        </div>
                        
                        <!-- Equipo visitante -->
                        <div class="team-container">
                            <div class="team-logo-container mb-2">
                                ${getTeamLogo(match.away_name)}
                            </div>
                            <div class="team-name fw-bold">${match.away_name}</div>
                        </div>
                    </div>
                    
                    <!-- Estadio (opcional) -->
                    ${match.location 
                        ? `<div class="mt-2 small text-muted"><i class="fas fa-map-marker-alt"></i> ${match.location}</div>` 
                        : ''
                    }
                </div>
            `;
            
            matchesGroup.appendChild(matchCard);
        });
        
        container.appendChild(matchesGroup);
    }
}

// Function to show error messages
function showError(elementId, message) {
    const element = document.getElementById(elementId);
    if (element) {
        if (element.tagName === 'TBODY') {
            element.innerHTML = `<tr><td colspan="10" class="text-center text-danger">${message}</td></tr>`;
        } else {
            element.innerHTML = `<div class="alert alert-danger">${message}</div>`;
        }

    }   
}

// Función para cargar métricas de la Liga MX
function loadMetrics() {
    const container = document.getElementById('metrics-container');
    container.innerHTML = '<div class="text-center"><div class="loading-spinner"></div><p>Cargando métricas...</p></div>';
    
    fetch('/api/metrics')
        .then(response => response.json())
        .then(data => {
            if (data.success && data.data) {
                displayMetrics(data.data);
            } else {
                container.innerHTML = '<div class="alert alert-info">No hay métricas disponibles.</div>';
            }
        })
        .catch(error => {
            console.error('Error fetching metrics:', error);
            container.innerHTML = '<div class="alert alert-danger">Error al cargar los datos. Por favor, intente más tarde.</div>';
        });
}

// Función para mostrar métricas
function displayMetrics(metricsData) {
    const container = document.getElementById('metrics-container');
    container.innerHTML = '';
    
    // Crear contenedor para la sección de goleadores y goles por equipo
    const topSection = document.createElement('div');
    topSection.className = 'row';
    
    // Mostrar máximos goleadores
    if (metricsData.top_scorers && metricsData.top_scorers.length > 0) {
        const scorersSection = document.createElement('div');
        scorersSection.className = 'col-md-6 metrics-section mb-5';
        
        const scorersTitle = document.createElement('h4');
        scorersTitle.innerHTML = '<i class="fas fa-futbol"></i> Goleadores';
        scorersSection.appendChild(scorersTitle);
        
        // Crear gráfico de barras para goleadores
        const scorersChartContainer = document.createElement('div');
        scorersChartContainer.className = 'chart-container';
        scorersChartContainer.style.height = '300px';
        scorersSection.appendChild(scorersChartContainer);
        
        const scorersList = document.createElement('div');
        scorersList.className = 'list-group mt-3';
        
        // Limitar a los primeros 10 goleadores
        const topScorers = metricsData.top_scorers.slice(0, 10);
        
        // Preparar datos para el gráfico
        const scorerLabels = [];
        const scorerData = [];
        const scorerColors = [];
        
        // Función para generar colores aleatorios
        const generateRandomColor = () => {
            const colors = [
                '#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0', '#9966FF',
                '#FF9F40', '#8AC249', '#EA5F89', '#00BFFF', '#9370DB'
            ];
            return colors[Math.floor(Math.random() * colors.length)];
        };
        
        topScorers.forEach((scorer, index) => {
            // Obtener el nombre del jugador y el equipo
            const playerName = scorer.name || (scorer.player && scorer.player.name ? scorer.player.name : scorer.player);
            const teamName = scorer.team_name || (scorer.team && scorer.team.name ? scorer.team.name : scorer.team);
            const goals = scorer.goals || 0;
            
            // Agregar datos para el gráfico
            scorerLabels.push(playerName);
            scorerData.push(goals);
            scorerColors.push(generateRandomColor());
            
            const scorerItem = document.createElement('div');
            scorerItem.className = 'list-group-item d-flex justify-content-between align-items-center';
            
            scorerItem.innerHTML = `
                <div>
                    <span class="badge bg-primary rounded-pill me-2">${index + 1}</span>
                    <strong>${playerName}</strong>
                    <small class="text-muted">${teamName}</small>
                </div>
                <span class="badge bg-secondary rounded-pill">${goals} goles</span>
            `;
            
            scorersList.appendChild(scorerItem);
        });
        
        // Crear el gráfico de goleadores
        if (typeof Chart !== 'undefined' && scorerLabels.length > 0) {
            const canvas = document.createElement('canvas');
            scorersChartContainer.appendChild(canvas);
            
            new Chart(canvas, {
                type: 'bar',
                data: {
                    labels: scorerLabels,
                    datasets: [{
                        label: 'Goles',
                        data: scorerData,
                        backgroundColor: scorerColors,
                        borderColor: scorerColors,
                        borderWidth: 1
                    }]
                },
                options: {
                    indexAxis: 'y',  
                    responsive: true,
                    maintainAspectRatio: false,
                    scales: {
                        x: {
                            beginAtZero: true,
                            title: {
                                display: true,
                                text: 'Goles'
                            }
                        }
                    },
                    plugins: {
                        legend: {
                            display: false
                        }
                    }
                }
            });
        }
        
        scorersSection.appendChild(scorersList);
        topSection.appendChild(scorersSection);
    }
    
    // Mostrar goles por equipo
    if (metricsData.goals_by_team && metricsData.goals_by_team.length > 0) {
        const goalsSection = document.createElement('div');
        goalsSection.className = 'col-md-6 metrics-section mb-5';
        
        const goalsTitle = document.createElement('h4');
        goalsTitle.innerHTML = '<i class="fas fa-chart-bar"></i> Goles por Equipo';
        goalsSection.appendChild(goalsTitle);
        
        // Crear gráfico de barras para goles por equipo
        const chartContainer = document.createElement('div');
        chartContainer.className = 'chart-container';
        chartContainer.style.height = '300px';
        goalsSection.appendChild(chartContainer);
        
        // Crear tabla de goles por equipo
        const goalsTable = document.createElement('div');
        goalsTable.className = 'table-responsive mt-3';
        goalsTable.innerHTML = `
            <table class="table table-striped table-hover">
                <thead>
                    <tr>
                        <th>Equipo</th>
                        <th class="text-center">GF</th>
                        <th class="text-center">GC</th>
                        <th class="text-center">Dif</th>
                    </tr>
                </thead>
                <tbody id="goals-by-team-body">
                </tbody>
            </table>
        `;
        
        goalsSection.appendChild(goalsTable);
        topSection.appendChild(goalsSection);
        
        // Agregar ambas secciones al contenedor principal
        container.appendChild(topSection);
        
        // Llenar la tabla de goles por equipo
        const goalsTableBody = document.getElementById('goals-by-team-body');
        
        // Limitar a los primeros 10 equipos
        const topTeams = metricsData.goals_by_team.slice(0, 6);
        
        topTeams.forEach(team => {
            // Calcular el total correctamente (asegurarse de que sean números)
            const goalsScored = parseInt(team.scored) || 0;
            const goalsConceded = parseInt(team.conceded) || 0;
            const totalGoals = goalsScored - goalsConceded;
            
            const row = document.createElement('tr');
            
            // Obtener el logo del equipo
            const teamLogo = getTeamLogo(team.team);
            
            row.innerHTML = `
                <td>
                    ${teamLogo}
                    <span class="ms-2">${team.team}</span>
                </td>
                <td class="text-success fw-bold text-center">${goalsScored}</td>
                <td class="text-danger fw-bold text-center">${goalsConceded}</td>
                <td class="text-center fw-bold">${totalGoals > 0 ? '+' + totalGoals : totalGoals}</td>
            `;
            
            goalsTableBody.appendChild(row);
        });
        
        // Crear datos para el gráfico
        const labels = topTeams.map(team => team.team);
        const goalsScored = topTeams.map(team => team.scored);
        const goalsConceded = topTeams.map(team => team.conceded);
        
        // Crear el gráfico usando Chart.js (asumiendo que está incluido)
        // Si Chart.js no está incluido, agregar el script
        if (typeof Chart === 'undefined') {
            const scriptTag = document.createElement('script');
            scriptTag.src = 'https://cdn.jsdelivr.net/npm/chart.js';
            scriptTag.onload = function() {
                createGoalsChart(chartContainer, labels, goalsScored, goalsConceded);
            };
            document.head.appendChild(scriptTag);
        } else {
            createGoalsChart(chartContainer, labels, goalsScored, goalsConceded);
        }
    } else {
        container.innerHTML = '<div class="alert alert-info">No hay datos de goles por equipo disponibles.</div>';
    }
}

// Función para crear el gráfico de goles por equipo
function createGoalsChart(container, labels, goalsScored, goalsConceded) {
    const canvas = document.createElement('canvas');
    container.appendChild(canvas);
    
    new Chart(canvas, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [
                {
                    label: 'Goles Anotados',
                    data: goalsScored,
                    backgroundColor: '#9370DB', // Morado para goles anotados
                    borderColor: '#8A2BE2',
                    borderWidth: 1
                },
                {
                    label: 'Goles Recibidos',
                    data: goalsConceded,
                    backgroundColor: '#87CEFA', // Azul claro para goles recibidos
                    borderColor: '#1E90FF',
                    borderWidth: 1
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                x: {
                    stacked: false,
                    ticks: {
                        autoSkip: false,
                        maxRotation: 90,
                        minRotation: 45
                    }
                },
                y: {
                    stacked: false,
                    beginAtZero: true,
                    title: {
                        display: true,
                        text: 'Número de Goles'
                    }
                }
            },
            plugins: {
                title: {
                    display: true,
                    text: 'Top 6 Equipos por Goles'
                },
                legend: {
                    position: 'top'
                }
            }
        }
    });
}

// Función para cargar el dashboard
function loadDashboard() {
    const container = document.getElementById('dashboard-container');
    container.innerHTML = '<div class="text-center"><div class="loading-spinner"></div><p>Cargando dashboard...</p></div>';
    
    fetch('/api/dashboard')
        .then(response => response.json())
        .then(data => {
            if (data.success && data.data) {
                displayDashboard(data.data);
            } else {
                container.innerHTML = '<div class="alert alert-info">No hay datos disponibles para el dashboard.</div>';
            }
        })
        .catch(error => {
            console.error('Error fetching dashboard:', error);
            container.innerHTML = '<div class="alert alert-danger">Error al cargar los datos. Por favor, intente más tarde.</div>';
        });
}

// Función para mostrar el dashboard
function displayDashboard(dashboardData) {
    const container = document.getElementById('dashboard-container');
    container.innerHTML = '';
    
    // Crear el contenedor principal del dashboard
    const dashboardMain = document.createElement('div');
    dashboardMain.className = 'dashboard-container';
    
    // Sección de tarjetas de estadísticas
    const statsCards = document.createElement('div');
    statsCards.className = 'dashboard-stats-cards';
    statsCards.innerHTML = `
        <div class="card mb-4">
            <div class="card-header bg-primary text-white">
                <h4 class="mb-0">Monitoreo del Sistema</h4>
            </div>
            <div class="card-body">
                <div class="row">
                    <!-- Tarjeta de Llamadas API -->
                    <div class="col-md-4 mb-3">
                        <div class="stats-card">
                            <div class="stats-icon bg-primary">
                                <i class="fas fa-server"></i>
                            </div>
                            <div class="stats-info">
                                <h2>${dashboardData.api_stats.calls}</h2>
                                <p>Llamadas API Totales</p>
                            </div>
                        </div>
                    </div>
                    
                    <!-- Tarjeta de Tasa de Éxito -->
                    <div class="col-md-4 mb-3">
                        <div class="stats-card">
                            <div class="stats-icon bg-success">
                                <i class="fas fa-check-circle"></i>
                            </div>
                            <div class="stats-info">
                                <h2>${dashboardData.api_stats.success_rate}%</h2>
                                <p>Tasa de Éxito</p>
                            </div>
                        </div>
                    </div>
                    
                    <!-- Tarjeta de Tiempo de Respuesta -->
                    <div class="col-md-4 mb-3">
                        <div class="stats-card">
                            <div class="stats-icon bg-warning">
                                <i class="fas fa-clock"></i>
                            </div>
                            <div class="stats-info">
                                <h2>${dashboardData.api_stats.response_time.toFixed(4)}ms</h2>
                                <p>Tiempo de Respuesta Promedio</p>
                            </div>
                        </div>
                    </div>
                    
                    <!-- Tarjeta de Errores -->
                    <div class="col-md-4 mb-3">
                        <div class="stats-card">
                            <div class="stats-icon bg-danger">
                                <i class="fas fa-exclamation-triangle"></i>
                            </div>
                            <div class="stats-info">
                                <h2>${dashboardData.api_stats.errors}</h2>
                                <p>Errores Totales</p>
                            </div>
                        </div>
                    </div>
                    
                    <!-- Tarjeta de Tiempo Activo -->
                    <div class="col-md-4 mb-3">
                        <div class="stats-card">
                            <div class="stats-icon bg-info">
                                <i class="fas fa-hourglass-half"></i>
                            </div>
                            <div class="stats-info">
                                <h2>${Math.floor(dashboardData.api_stats.uptime / 60)}m</h2>
                                <p>Tiempo Activo</p>
                            </div>
                        </div>
                    </div>
                    
                    <!-- Tarjeta de Partidos Totales -->
                    <div class="col-md-4 mb-3">
                        <div class="stats-card">
                            <div class="stats-icon bg-secondary">
                                <i class="fas fa-futbol"></i>
                            </div>
                            <div class="stats-info">
                                <h2>${dashboardData.total_matches || 'N/A'}</h2>
                                <p>Partidos Totales</p>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    `;
    
    dashboardMain.appendChild(statsCards);
    
    // Sección de gráficos
    const chartsSection = document.createElement('div');
    chartsSection.className = 'row';
    
    // Gráfico de Llamadas API
    const callsChartDiv = document.createElement('div');
    callsChartDiv.className = 'col-md-6 mb-4';
    callsChartDiv.innerHTML = `
        <div class="card">
            <div class="card-header bg-dark text-white">
                <h5 class="mb-0">Llamadas API (48 horas)</h5>
            </div>
            <div class="card-body">
                <canvas id="calls-chart" height="250"></canvas>
            </div>
        </div>
    `;
    
    // Gráfico de Tasa de Éxito
    const successRateChartDiv = document.createElement('div');
    successRateChartDiv.className = 'col-md-6 mb-4';
    successRateChartDiv.innerHTML = `
        <div class="card">
            <div class="card-header bg-dark text-white">
                <h5 class="mb-0">Tasa de Éxito (%) (48 horas)</h5>
            </div>
            <div class="card-body">
                <canvas id="success-rate-chart" height="250"></canvas>
            </div>
        </div>
    `;
    
    // Gráfico de Tiempo de Respuesta
    const responseTimeChartDiv = document.createElement('div');
    responseTimeChartDiv.className = 'col-md-6 mb-4';
    responseTimeChartDiv.innerHTML = `
        <div class="card">
            <div class="card-header bg-dark text-white">
                <h5 class="mb-0">Tiempo de Respuesta (ms) (48 horas)</h5>
            </div>
            <div class="card-body">
                <canvas id="response-time-chart" height="250"></canvas>
            </div>
        </div>
    `;
    
    // Gráfico de Errores
    const errorsChartDiv = document.createElement('div');
    errorsChartDiv.className = 'col-md-6 mb-4';
    errorsChartDiv.innerHTML = `
        <div class="card">
            <div class="card-header bg-dark text-white">
                <h5 class="mb-0">Número de Errores (48 horas)</h5>
            </div>
            <div class="card-body">
                <canvas id="errors-chart" height="250"></canvas>
            </div>
        </div>
    `;
    
    chartsSection.appendChild(callsChartDiv);
    chartsSection.appendChild(successRateChartDiv);
    chartsSection.appendChild(responseTimeChartDiv);
    chartsSection.appendChild(errorsChartDiv);
    
    dashboardMain.appendChild(chartsSection);
    container.appendChild(dashboardMain);
    
    // Crear los gráficos con Chart.js
    createDashboardCharts(dashboardData);
}

// Función para crear los gráficos del dashboard
function createDashboardCharts(dashboardData) {
    const hours = dashboardData.hours;
    const apiTrend = dashboardData.api_trend;
    
    // Configuración para mostrar solo algunas etiquetas en el eje X cuando hay muchas horas
    const skipLabels = Math.ceil(hours.length / 12); // Mostrar aproximadamente 12 etiquetas
    
    // Función para determinar si mostrar una etiqueta basada en su índice
    const skipLabelsCallback = function(value, index) {
        return index % skipLabels === 0 ? hours[index] : '';
    };
    
    // Gráfico de Llamadas API
    const callsCtx = document.getElementById('calls-chart').getContext('2d');
    new Chart(callsCtx, {
        type: 'line',
        data: {
            labels: hours,
            datasets: [{
                label: 'Llamadas API',
                data: apiTrend.calls,
                backgroundColor: 'rgba(54, 162, 235, 0.2)',
                borderColor: 'rgba(54, 162, 235, 1)',
                borderWidth: 2,
                tension: 0.4,
                pointRadius: 2,
                pointHoverRadius: 5
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                x: {
                    title: {
                        display: true,
                        text: 'Horas'
                    },
                    ticks: {
                        callback: skipLabelsCallback
                    }
                },
                y: {
                    beginAtZero: true,
                    title: {
                        display: true,
                        text: 'Número de llamadas'
                    }
                }
            },
            plugins: {
                tooltip: {
                    callbacks: {
                        title: function(context) {
                            return 'Hora: ' + context[0].label;
                        }
                    }
                }
            }
        }
    });
    
    // Gráfico de Tasa de Éxito
    const successRateCtx = document.getElementById('success-rate-chart').getContext('2d');
    new Chart(successRateCtx, {
        type: 'bar',
        data: {
            labels: hours,
            datasets: [{
                label: 'Tasa de Éxito (%)',
                data: apiTrend.success_rate,
                backgroundColor: 'rgba(75, 192, 192, 0.2)',
                borderColor: 'rgba(75, 192, 192, 1)',
                borderWidth: 2
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                x: {
                    title: {
                        display: true,
                        text: 'Horas'
                    },
                    ticks: {
                        callback: skipLabelsCallback
                    }
                },
                y: {
                    beginAtZero: true,
                    max: 100,
                    title: {
                        display: true,
                        text: 'Porcentaje'
                    }
                }
            },
            plugins: {
                tooltip: {
                    callbacks: {
                        title: function(context) {
                            return 'Hora: ' + context[0].label;
                        }
                    }
                }
            }
        }
    });
    
    // Gráfico de Tiempo de Respuesta
    const responseTimeCtx = document.getElementById('response-time-chart').getContext('2d');
    new Chart(responseTimeCtx, {
        type: 'line',
        data: {
            labels: hours,
            datasets: [{
                label: 'Tiempo de Respuesta (ms)',
                data: apiTrend.response_time,
                backgroundColor: 'rgba(255, 206, 86, 0.2)',
                borderColor: 'rgba(255, 206, 86, 1)',
                borderWidth: 2,
                tension: 0.4,
                pointRadius: 2,
                pointHoverRadius: 5
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                x: {
                    title: {
                        display: true,
                        text: 'Horas'
                    },
                    ticks: {
                        callback: skipLabelsCallback
                    }
                },
                y: {
                    beginAtZero: true,
                    title: {
                        display: true,
                        text: 'Milisegundos'
                    }
                }
            },
            plugins: {
                tooltip: {
                    callbacks: {
                        title: function(context) {
                            return 'Hora: ' + context[0].label;
                        }
                    }
                }
            }
        }
    });
    
    // Gráfico de Errores
    const errorsCtx = document.getElementById('errors-chart').getContext('2d');
    new Chart(errorsCtx, {
        type: 'bar',
        data: {
            labels: hours,
            datasets: [{
                label: 'Errores',
                data: apiTrend.errors,
                backgroundColor: 'rgba(255, 99, 132, 0.2)',
                borderColor: 'rgba(255, 99, 132, 1)',
                borderWidth: 2
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                x: {
                    title: {
                        display: true,
                        text: 'Horas'
                    },
                    ticks: {
                        callback: skipLabelsCallback
                    }
                },
                y: {
                    beginAtZero: true,
                    title: {
                        display: true,
                        text: 'Número de errores'
                    }
                }
            },
            plugins: {
                tooltip: {
                    callbacks: {
                        title: function(context) {
                            return 'Hora: ' + context[0].label;
                        }
                    }
                }
            }
        }
    });
}

// Función para cargar el contenido inicial
function loadInitialContent() {
    // Cargar datos para cada pestaña
    loadStandings();
    loadFixtures();
    loadHistory();
    loadResults();
    loadMetrics();
    loadDashboard();
    displayTelegramBot();
}

// Función para mostrar la información del bot de Telegram
function displayTelegramBot() {
    const container = document.getElementById('telegram');
    
    // Crear el contenido del bot de Telegram
    const telegramContent = document.createElement('div');
    telegramContent.className = 'telegram-container';
    telegramContent.innerHTML = `
        <div class="card">
            <div class="card-header bg-primary text-white">
                <h4 class="mb-0"><i class="fab fa-telegram"></i> Bot de Notificaciones en Tiempo Real</h4>
            </div>
            <div class="card-body text-center">
                <div class="row justify-content-center">
                    <div class="col-md-8">
                        <div class="telegram-info mb-4">
                            <img src="https://telegram.org/img/t_logo.png" alt="Telegram Logo" class="img-fluid mb-3" style="max-width: 100px;">
                            <h3>¡Recibe notificaciones en tiempo real!</h3>
                            <p class="lead mb-4">Mantente al día con todos los resultados, goles y eventos importantes de la Liga MX directamente en tu teléfono.</p>
                            
                            <div class="features-list mb-4">
                                <div class="feature-item">
                                    <i class="fas fa-bell text-primary"></i>
                                    <span>Notificaciones instantáneas de goles</span>
                                </div>
                                <div class="feature-item">
                                    <i class="fas fa-calendar-alt text-primary"></i>
                                    <span>Recordatorios de partidos</span>
                                </div>
                                <div class="feature-item">
                                    <i class="fas fa-chart-line text-primary"></i>
                                    <span>Estadísticas en tiempo real</span>
                                </div>
                                <div class="feature-item">
                                    <i class="fas fa-newspaper text-primary"></i>
                                    <span>Noticias y actualizaciones</span>
                                </div>
                            </div>
                            
                            <a href="https://t.me/+kz4uIFKkIdwzMzRh" target="_blank" class="btn btn-primary btn-lg">
                                <i class="fab fa-telegram"></i> Unirse al Bot de Telegram
                            </a>
                            
                            <p class="mt-3 text-muted">O escanea el código QR con tu aplicación de Telegram</p>
                            
                            <div class="qr-code mt-2">
                                <img src="https://api.qrserver.com/v1/create-qr-code/?size=200x200&data=https://t.me/+kz4uIFKkIdwzMzRh" alt="QR Code" class="img-fluid" style="max-width: 200px;">
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    `;
    
    // Limpiar el contenedor y agregar el nuevo contenido
    container.innerHTML = '';
    container.appendChild(telegramContent);
}