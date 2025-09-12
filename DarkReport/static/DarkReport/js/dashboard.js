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
        if (link) link.click();
    }

    projectLinks.forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();

            const projectName = link.textContent.trim();
            const description = link.getAttribute('data-description');
            const reportsData = JSON.parse(link.getAttribute('data-reports'));
            const projectId = link.getAttribute('data-project-id');
            const totalFinds = reportsData.reduce((sum, report) => sum + report.finds.length, 0);

            let html = `<h2>${projectName}</h2>
                        <p>${description}</p>
                        <p><strong>${window.translations.reports}: ${reportsData.length}</strong> | <strong>${window.translations.finds}: ${totalFinds}</strong></p>
                        <hr>`;

            if (reportsData.length > 0) {
                html += `<ul class="list-group mb-3">`;
                reportsData.forEach(report => {
                    html += `<li class="list-group-item">
                                <strong>${report.target}</strong>
                                <ul>`;

                    const priorityOrder = { very_high: 3, high: 2, medium: 1, low: 0 };

                    report.finds
                        .sort((a, b) => (priorityOrder[b.priority] || -1) - (priorityOrder[a.priority] || -1))
                        .forEach(find => {
                            let priorityClass = '';
                            let priorityLabel = '';

                            switch(find.priority) {
                                case 'very_high':
                                    priorityClass = 'bg-danger text-white';
                                    priorityLabel = window.translations.very_high;
                                    break;
                                case 'high':
                                    priorityClass = 'bg-warning text-dark';
                                    priorityLabel = window.translations.high;
                                    break;
                                case 'medium':
                                    priorityClass = 'bg-info text-dark';
                                    priorityLabel = window.translations.medium;
                                    break;
                                case 'low':
                                    priorityClass = 'bg-secondary text-white';
                                    priorityLabel = window.translations.low;
                                    break;
                                default:
                                    priorityClass = 'bg-secondary text-white';
                                    priorityLabel = find.priority;
                            }

                            html += `<li>${window.translations.find} - ${find.vulnerability} 
                                     <span class="badge ${priorityClass} ms-2">${priorityLabel}</span>
                                     </li>`;
                        });

                    html += `</ul></li>`;
                });
                html += `</ul>`;
            }

            html += `
                <button class="btn btn-dark me-2" onclick="window.location.href='/project/${projectId}/'">${window.translations.open}</button>
                <button class="btn btn-dark me-2" onclick="exportProject(${projectId})">${window.translations.export}</button>
                <button class="btn btn-dark" data-bs-toggle="modal" data-bs-target="#deleteProjectModal" onclick="setDeleteProjectId(${projectId})">🗑️${window.translations.delete}</button>
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
