from django import forms
from .models import Project, Report, Find, Vuln
from .utils import load_vulnerabilities

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['project_name']


class ReportForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = ['target']


class FindForm(forms.ModelForm):
    vulnerability = forms.ChoiceField(
        choices=load_vulnerabilities(),
        required=True,
        widget=forms.Select(attrs={
            'class': 'form-control',
            'style': 'width: 450px;'  # Ajusta el ancho a tu gusto
        })
    )

    class Meta:
        model = Find
        fields = [
            'reconnaissance',
            'weaponization',
            'vulnerability',
            'delivery',
            'exploitation',
            'installation',
            'commandcontrol',
            'actions',
            
        ]
        widgets = {
            'reconnaissance': forms.Textarea(attrs={'rows': 1, 'class': 'form-control'}),
            'weaponization': forms.Textarea(attrs={'rows': 1, 'class': 'form-control'}),
            'delivery': forms.Textarea(attrs={'rows': 1, 'class': 'form-control'}),
            'exploitation': forms.Textarea(attrs={'rows': 1, 'class': 'form-control'}),
            'installation': forms.Textarea(attrs={'rows': 1, 'class': 'form-control'}),
            'commandcontrol': forms.Textarea(attrs={'rows': 1, 'class': 'form-control'}),
            'actions': forms.Textarea(attrs={'rows': 1, 'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Campos opcionales
        self.fields['reconnaissance'].required = False
        self.fields['weaponization'].required = False
        self.fields['installation'].required = False
        self.fields['commandcontrol'].required = False

class VulnForm(forms.ModelForm):
    class Meta:
        model = Vuln
        fields = ['vuln_name']
