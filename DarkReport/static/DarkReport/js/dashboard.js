window.onload = function () {
    const contentDiv = document.querySelector('.content');
    const selectedId = contentDiv.getAttribute('data-selected-project');
    if (selectedId) {
        const link = document.querySelector(`.project-link[data-project-id="${selectedId}"]`);
        if (link) {
            link.click();
        }
    }
};

function getCSRFToken() {
    const name = 'csrftoken';
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let cookie of cookies) {
            cookie = cookie.trim();
            if (cookie.startsWith(name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function exportProject(projectId) {
    const form = document.createElement('form');
    form.method = 'POST';
    form.action = `/project/${projectId}/export/`;

    // CSRF
    const csrfInput = document.createElement('input');
    csrfInput.type = 'hidden';
    csrfInput.name = 'csrfmiddlewaretoken';
    csrfInput.value = getCSRFToken();
    form.appendChild(csrfInput);

    document.body.appendChild(form);
    form.submit();
}

document.addEventListener('DOMContentLoaded', () => {
    const projectLinks = document.querySelectorAll('.project-link');
    const contentDiv = document.querySelector('.content');
    const selectedId = contentDiv.getAttribute('data-selected-project');
    if (selectedId) {
        const link = document.querySelector(`.project-link[data-project-id="${selectedId}"]`);
        if (link) {
            link.click();  // simula click en el proyecto seleccionado
        }
    }
    projectLinks.forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();

            const projectName = link.textContent.trim();
            const description = link.getAttribute('data-description');
            const reportsData = JSON.parse(link.getAttribute('data-reports'));
            const projectId = link.getAttribute('data-project-id');

            let html = `<h2>${projectName}</h2>
                        <p>${description}</p>
                        <p><strong>Reports: ${reportsData.length}</strong></p>`;

            if (reportsData.length > 0) {
                html += `<ul class="list-group mb-3">`;
                reportsData.forEach(report => {
                    html += `<li class="list-group-item">
                                <strong> ${report.target}</strong>
                                <ul>`;
                    report.finds.forEach(find => {
                        html += `<li>Find ${find.id}: ${find.vulnerability}</li>`;
                    });
                    html += `</ul></li>`;
                });
                html += `</ul>`;
            }

            html += `
                <button class="btn btn-dark me-2" style="color:white;" onclick="window.location.href='/project/${projectId}/'">Open</button>
                <button class="btn btn-dark me-2" onclick="exportProject(${projectId})">📤 Export</button>
                <button class="btn btn-dark" data-bs-toggle="modal" data-bs-target="#deleteProjectModal" onclick="setDeleteProjectId(${projectId})">Delete</button>
            `;

            contentDiv.innerHTML = html;
            projectLinks.forEach(l => l.classList.remove('active'));
            link.classList.add('active');
        });
    });
});

function setDeleteProjectId(projectId) {
    const form = document.getElementById('deleteProjectForm');
    form.action = `/project/${projectId}/delete/`;
}

// Gráficos de porcentajes por find y vulnerabilidad
fetch('/graph-data/')
    .then(res => res.json())
    .then(data => {
        const cveChartCtx = document.getElementById('cveChart').getContext('2d');
        const vulnChartCtx = document.getElementById('vulnChart').getContext('2d');

        new Chart(cveChartCtx, {
            type: 'doughnut',
            data: {
                labels: data.cve.labels,
                datasets: [{
                    data: data.cve.data,
                    backgroundColor: ['#00ff00','#36a2eb','#ffcd56','#4bc0c0','#9966ff','#c9cbcf']
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: { legend: { position: 'bottom' } }
            }
        });

        new Chart(vulnChartCtx, {
            type: 'doughnut',
            data: {
                labels: data.vulnerability.labels,
                datasets: [{
                    data: data.vulnerability.data,
                    backgroundColor: ['#00ff00','#36a2eb','#ffcd56','#4bc0c0','#9966ff','#c9cbcf']
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: { legend: { position: 'bottom' } }
            }
        });
    });