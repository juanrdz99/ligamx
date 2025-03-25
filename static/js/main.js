document.addEventListener('DOMContentLoaded', function() {
    // Load standings data by default
    loadStandings();
    
    // Add event listeners for tab changes
    document.getElementById('livescores-tab').addEventListener('click', loadLiveScores);
    document.getElementById('fixtures-tab').addEventListener('click', loadFixtures);
    document.getElementById('history-tab').addEventListener('click', loadHistory);
    
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
    
    tableData.forEach((team, index) => {
        const row = document.createElement('tr');
        
        // Add position with background color based on position (for visual indication)
        let positionClass = '';
        if (index < 4) positionClass = 'bg-success text-white'; // Champions League spots
        else if (index < 7) positionClass = 'bg-info text-white'; // Europa League spots
        else if (index >= tableData.length - 3) positionClass = 'bg-danger text-white'; // Relegation spots
        
        row.innerHTML = `
            <td class="${positionClass}">${team.rank}</td>
            <td>
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

// Function to display matches (used for live, fixtures, and history)
function displayMatches(matches, containerId, type) {
    const container = document.getElementById(containerId);
    container.innerHTML = '';
    
    if (!matches || matches.length === 0) {
        container.innerHTML = `<div class="alert alert-info">No hay ${type} disponibles.</div>`;
        return;
    }
    
    // Group matches by date
    const matchesByDate = {};
    matches.forEach(match => {
        const date = match.date || 'Sin fecha';
        if (!matchesByDate[date]) {
            matchesByDate[date] = [];
        }
        matchesByDate[date].push(match);
    });
    
    // Create match cards grouped by date
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
            
            if (match.status === 'IN PLAY' || match.status === 'LIVE') {
                statusClass = 'status-live';
                statusText = 'En Vivo';
            } else if (match.status === 'FINISHED' || match.ft_score) {
                statusClass = 'status-finished';
                statusText = 'Finalizado';
            }
            
            matchCard.innerHTML = `
                <div class="match-card">
                    <div class="d-flex justify-content-between align-items-center mb-2">
                        <span class="match-time">${match.time || ''}</span>
                        <span class="match-status ${statusClass}">${statusText}</span>
                    </div>
                    <div class="row align-items-center">
                        <div class="col-5 text-end">
                            <span class="team-name">${match.home_name}</span>
                        </div>
                        <div class="col-2 text-center score">
                            ${match.ft_score || match.score || '-'}
                        </div>
                        <div class="col-5 text-start">
                            <span class="team-name">${match.away_name}</span>
                        </div>
                    </div>
                    ${match.location ? `<div class="mt-2 small text-muted">Estadio: ${match.location}</div>` : ''}
                </div>
            `;
            
            matchesGroup.appendChild(matchCard);
        });
        
        container.appendChild(matchesGroup);
    }
}

// Helper function to format date
function formatDate(dateString) {
    if (!dateString || dateString === 'Sin fecha') return 'Fecha no disponible';
    
    const options = { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' };
    try {
        const date = new Date(dateString);
        return date.toLocaleDateString('es-MX', options);
    } catch (e) {
        return dateString;
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
