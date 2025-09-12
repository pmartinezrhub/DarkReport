from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from .models import Project
from .forms import *
from collections import Counter
import requests
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib import messages
from django.http import HttpResponse
import csv
from django.db.models import Case, When, Value, IntegerField

@login_required
def dashboard(request):
    project_id = request.GET.get('project')
    projects = Project.objects.all()
    total_projects = projects.count()
    total_reports = sum(p.reports.count() for p in projects)
    total_finds = Find.objects.count()

    context = {
        'projects': projects,
        'total_projects': total_projects,
        'total_reports': total_reports,
        'total_finds': total_finds,
        'selected_project_id': project_id
    }
    return render(request, 'dashboard.html', context)

@login_required
def project_create(request):
    if request.method == "POST":
        name = request.POST.get("project_name")
        description = request.POST.get("description", "")
        project = Project.objects.create(project_name=name, description=description)

      
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({
                "id": project.id,
                "project_name": project.project_name
            })

        return redirect('dashboard')  

    return redirect('dashboard')

@login_required
def project_detail(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    reports = project.reports.all()

    total_finds = Find.objects.filter(report__in=reports).count()

    for report in reports:
        report.finds_ordered = report.finds.annotate(
            priority_order=Case(
                When(priority='very_high', then=Value(1)),
                When(priority='high', then=Value(2)),
                When(priority='medium', then=Value(3)),
                When(priority='low', then=Value(4)),
                output_field=IntegerField()
            )
        ).order_by('priority_order')

    add_report_form = ReportForm()

    return render(request, 'project_detail.html', {
        'project': project,
        'reports': reports,
        'total_finds': total_finds,
        'form': add_report_form
    })

@login_required
def add_report(request, project_id):
    project = get_object_or_404(Project, id=project_id)

    if request.method == 'POST':
        form = ReportForm(request.POST)
        if form.is_valid():
            report = form.save(commit=False)  
            report.project = project         
            report.save()                 
            return redirect('project_detail', project_id=project.id)
    else:
        form = ReportForm()

    return render(request, 'add_report.html', {'form': form, 'project': project})

@login_required
def add_find(request, report_id):
    report = get_object_or_404(Report, id=report_id)

    if request.method == 'POST':
    
        form = FindForm(request.POST, request.FILES)
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


@login_required
def edit_find(request, pk):
    find = get_object_or_404(Find, pk=pk)
    project = find.report.project 

    if request.method == 'POST':
        form = FindForm(request.POST, instance=find)
        if form.is_valid():
            form.save()
            return redirect('project_detail', project_id=project.id)
    else:
        form = FindForm(instance=find)  

    return render(request, 'edit_find.html', {
        'form': form,
        'find': find,
        'project': project
    })

@login_required
def delete_find(request, pk):
    find = get_object_or_404(Find, pk=pk)
    project_id = find.report.project.id  

    if request.method == 'POST':
        find.delete()
        return redirect('project_detail', project_id=project_id)
    
    vulnerability = forms.ChoiceField(
        choices=load_vulnerabilities(),
        required=True,
        widget=forms.Select(attrs={
            'class': 'form-control',
            'style': 'width: 200px;'  
        })
    )

@login_required
def delete_report(request, pk):
    report = get_object_or_404(Report, pk=pk)
    project_id = report.project.id

    if request.method == 'POST':
        report.delete()
        return redirect('project_detail', project_id=project_id)

@login_required
def delete_project(request, pk):
    project = get_object_or_404(Project, pk=pk)
    if request.method == 'POST':
        project.delete()
        return redirect('dashboard')  

@login_required
def cve_lookup(request):
    query = request.GET.get("q", "").strip()
    if not query:
        return JsonResponse([], safe=False)

    url = f"https://services.nvd.nist.gov/rest/json/cves/2.0?cveId={query}"
    headers = {
        # "apiKey": "TU_CLAVE_DE_API"  # optional
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()

        if "vulnerabilities" in data and len(data["vulnerabilities"]) > 0:
            cve_info = data["vulnerabilities"][0]["cve"]
            result = {
                "id": cve_info.get("id"),
                "descriptions": cve_info.get("descriptions", []),
                "metrics": cve_info.get("metrics", {}),
                "references": cve_info.get("references", [])
            }
            return JsonResponse([result], safe=False)
        else:
            return JsonResponse([], safe=False)

    except requests.exceptions.HTTPError as e:
        print(f"Error HTTP al buscar CVE: {e}")
        return JsonResponse([], safe=False)
    except Exception as e:
        print(f"Error al buscar CVE: {e}")
        return JsonResponse([], safe=False)


@login_required
def graph_data(request):
    finds = Find.objects.all()

    total = len(finds)
    if total == 0:
        return JsonResponse({
            "cve": {"labels": [], "data": []},
            "vulnerability": {"labels": [], "data": []}
        })

 
    cve_counter = Counter(f.cve if f.cve else "no CVE" for f in finds)
    vuln_counter = Counter(f.vulnerability if f.vulnerability else "Sin Vulnerabilidad" for f in finds)

  
    cve_labels = list(cve_counter.keys())
    cve_data = [round(count / total * 100, 2) for count in cve_counter.values()]

    vuln_labels = list(vuln_counter.keys())
    vuln_data = [round(count / total * 100, 2) for count in vuln_counter.values()]

    return JsonResponse({
        "cve": {"labels": cve_labels, "data": cve_data},
        "vulnerability": {"labels": vuln_labels, "data": vuln_data}
    })


def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)   
            return redirect("/")        
        else:
            messages.error(request, "Invalid username or password.")

    return render(request, "login.html")


@login_required
def logout_view(request):
    auth_logout(request)              
    return redirect("login")

@login_required
def export_report(request, report_id):
    report = get_object_or_404(Report, id=report_id)
    target = report.target     
    project = report.project     
    finds = report.finds.all()

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="report_{project.project_name}_{report.target}.csv"'

    writer = csv.writer(response)
    writer.writerow([
        'Vulnerability', 'Reconnaissance', 'File', 'Weaponization', 'Delivery', 
        'Exploitation', 'CVE', 'Installation', 'Command/Control', 'Actions'
    ])

    for find in finds:
        writer.writerow([
            find.vulnerability or '',
            find.reconnaissance or '',
            find.recon_file.url if find.recon_file else '',
            find.weaponization or '',
            find.delivery or '',
            find.exploitation or '',
            find.cve or '',
            find.installation or '',
            find.commandcontrol or '',
            find.actions or '',
            find.priority or ''
        ])

    return response

@login_required
def export_project(request, project_id):
    project = Project.objects.get(id=project_id)
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="project_{project.project_name}.csv"'

    writer = csv.writer(response)
    writer.writerow(['Report', 'Find ID', 'Vulnerability', 'Reconnaissance', 'File', 'Weaponization', 'Delivery', 
                     'Exploitation', 'CVE', 'Installation', 'Command/Control', 'Actions'])

    for report in project.reports.all():
        for find in report.finds.all():
            writer.writerow([
                report.target,
                find.id,
                find.vulnerability or '',
                find.reconnaissance or '',
                find.recon_file.url if find.recon_file else '',
                find.weaponization or '',
                find.delivery or '',
                find.exploitation or '',
                find.cve or '',
                find.installation or '',
                find.commandcontrol or '',
                find.actions or '',
                find.priority or ''
            ])
    return response
