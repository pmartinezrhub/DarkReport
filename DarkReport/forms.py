from django import forms
from .models import Project, Report, Find, Vuln


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['project_name']


class ReportForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = ['project', 'target_name']


class FindForm(forms.ModelForm):
    class Meta:
        model = Find
        fields = [
            'report',
            'reconnaissance',
            'weaponization',
            'delivery',
            'exploitation',
            'installation',
            'commandcontrol',
            'actions'
        ]


class VulnForm(forms.ModelForm):
    class Meta:
        model = Vuln
        fields = ['vuln_name']
