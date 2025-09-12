from django.db import models
from django.utils.translation import gettext_lazy as _

class Project(models.Model):
    project_name = models.CharField(max_length=50)
    description = models.CharField(max_length=500, null=True, blank=True)

    def __str__(self):
        return self.project_name


class Report(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="reports")
    target = models.CharField(
        max_length=255,
        verbose_name=_("Target")
    )

    def __str__(self):
        return f"{self.target_name} ({self.project})"


class Find(models.Model):
    PRIORITY_CHOICES = [
        ('very_high', _('Very High')),
        ('high', _('High')),
        ('medium', _('Medium')),
        ('low', _('Low')),
    ]

    report = models.ForeignKey(Report, on_delete=models.CASCADE, related_name="finds")
    reconnaissance = models.TextField()
    weaponization = models.TextField()
    delivery = models.TextField()
    exploitation = models.TextField()
    installation = models.TextField()
    commandcontrol = models.TextField()
    actions = models.TextField(blank=True, null=True)
    vulnerability = models.TextField()
    cve = models.CharField(max_length=32, blank=True, null=True)
    recon_file = models.FileField(upload_to='recon/', blank=True, null=True)
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='low')

    def __str__(self):
        return f"Findings for {self.report}"



class Vuln(models.Model):
    vuln_name = models.CharField(max_length=80)

    def __str__(self):
        return self.vuln_name


class CVE(models.Model):
    cve_id = models.CharField(max_length=15)
