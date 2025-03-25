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

document.addEventListener('DOMContentLoaded', function() {
    // Load standings data by default
    loadStandings();
    
    // Add event listeners for tab switching
    document.getElementById('livescores-tab').addEventListener('click', loadLiveScores);
    document.getElementById('fixtures-tab').addEventListener('click', loadFixtures);
    document.getElementById('history-tab').addEventListener('click', loadResults);
    
    // Set auto-refresh for live scores tab
    setInterval(function() {
        if (document.getElementById('livescores-tab').classList.contains('active')) {
            loadLiveScores();
        }
    }, 60000); // Refresh every minute
});

// Function to load standings data
function loadStandings() {
    fetch('/api/standings')
        .then(response => response.json())
        .then(data => {
            if (data.success && data.data.table) {
                displayStandings(data.data.table);
            } else {
                showError('standings-body', 'No se pudieron cargar los datos de la tabla.');
            }
        })
        .catch(error => {
            console.error('Error fetching standings:', error);
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

// Function to load live scores
function loadLiveScores() {
    const container = document.getElementById('livescores-container');
    container.innerHTML = '<div class="text-center"><div class="loading-spinner"></div><p>Cargando partidos en vivo...</p></div>';
    
    fetch('/api/livescores')
        .then(response => response.json())
        .then(data => {
            if (data.success && data.data.match) {
                displayMatches(data.data.match, 'livescores-container', 'en vivo');
            } else {
                container.innerHTML = '<div class="alert alert-info">No hay partidos en vivo en este momento.</div>';
            }
        })
        .catch(error => {
            console.error('Error fetching live scores:', error);
            container.innerHTML = '<div class="alert alert-danger">Error al cargar los datos. Por favor, intente más tarde.</div>';
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
