from django import forms
from .models import Project, Report, Find, Vuln
from .utils import load_vulnerabilities
from django.utils.translation import gettext_lazy as _

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['project_name']


class ReportForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = ['target']
        widgets = {
            'target': forms.TextInput(attrs={
                'class': 'form-control',   
                'placeholder': 'host, URL, ip, API..',
                'size': 120               
            })
        }

class FindForm(forms.ModelForm):
    vulnerability = forms.ChoiceField(
        choices=load_vulnerabilities(),
        required=True,
        label=_("Vulnerability"),
        widget=forms.Select(attrs={
            'class': 'form-control',
            'style': 'width: 450px;'
        })
    )

    cve = forms.CharField(
        required=False,
        label=_("CVE"),
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'style': 'width: 450px;',
            'placeholder': _('CVE-XXXX-XXXX')
        })
    )

    class Meta:
        model = Find
        fields = [
            'reconnaissance',
            'recon_file',
            'weaponization',
            'vulnerability',
            'cve',
            'delivery',
            'exploitation',
            'installation',
            'commandcontrol',
            'actions',
            'priority',
        ]
        labels = {
            'reconnaissance': _("Reconnaissance"),
            'recon_file': _("Recon file"),
            'weaponization': _("Weaponization"),
            'delivery': _("Delivery"),
            'exploitation': _("Exploitation"),
            'installation': _("Installation"),
            'commandcontrol': _("Command & Control"),
            'actions': _("Actions"),
            'priority': _("Priority"),
        }
        widgets = {
            'reconnaissance': forms.Textarea(attrs={'rows': 2, 'class': 'form-control', 'placeholder': _('How discovery was done, Nmap, Nuclei...')}),
            'weaponization': forms.Textarea(attrs={'rows': 1, 'class': 'form-control', 'placeholder': _('Which software can be used for attack')}),
            'delivery': forms.Textarea(attrs={'rows': 2, 'class': 'form-control', 'placeholder': _('How the payload is delivered, POST, mail...')}),
            'exploitation': forms.Textarea(attrs={'rows': 2, 'class': 'form-control', 'placeholder': _('A brief explanation of the vulnerability')}),
            'installation': forms.Textarea(attrs={'rows': 1, 'class': 'form-control', 'placeholder': _('Malware installed, like RAT, virus')}),
            'commandcontrol': forms.Textarea(attrs={'rows': 1, 'class': 'form-control', 'placeholder': _('Protocols and ports used for C&C')}),
            'actions': forms.Textarea(attrs={'rows': 1, 'class': 'form-control', 'placeholder': _('Which actions can be performed after the exploit')}),
            'priority': forms.Select(attrs={'class': 'form-control','style': 'width: 200px; display: inline-block;'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['vulnerability'].choices = load_vulnerabilities()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['reconnaissance'].required = False
        self.fields['weaponization'].required = False
        self.fields['installation'].required = False
        self.fields['commandcontrol'].required = False

class VulnForm(forms.ModelForm):
    class Meta:
        model = Vuln
        fields = ['vuln_name']
