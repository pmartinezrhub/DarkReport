from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from .models import Project
from .forms import *

def workspace(request):
    projects = Project.objects.all()
    return render(request, 'workspace.html', {'projects': projects})

def project_create(request):
    if request.method == "POST":
        name = request.POST.get("project_name")
        description = request.POST.get("description", "")
        project = Project.objects.create(project_name=name, description=description)

        # Reemplazo de request.is_ajax()
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({
                "id": project.id,
                "project_name": project.project_name
            })

        return redirect('workspace')  # Cambia 'workspace' por tu página principal

    return redirect('workspace')

def project_detail(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    reports = project.reports.all()
    form = ReportForm()

    return render(request, 'project_detail.html', {
        'project': project,
        'reports': reports,
        'form': form
    })

def add_report(request, project_id):
    project = get_object_or_404(Project, id=project_id)

    if request.method == 'POST':
        form = ReportForm(request.POST)
        if form.is_valid():
            report = form.save(commit=False)  # No guardar todavía
            report.project = project         # Asignar el proyecto
            report.save()                    # Guardar ahora sí
            return redirect('project_detail', project_id=project.id)
    else:
        form = ReportForm()

    return render(request, 'add_report.html', {'form': form, 'project': project})

def add_find(request, report_id):
    report = get_object_or_404(Report, id=report_id)

    if request.method == 'POST':
        form = FindForm(request.POST)
        if form.is_valid():
            find = form.save(commit=False)
            find.report = report
            find.save()
            return redirect('project_detail', project_id=report.project.id)
    else:
        form = FindForm()

    return render(request, 'add_find.html', {
        'form': form,
        'report': report
    })