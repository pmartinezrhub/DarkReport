from django.db import models

class Project(models.Model):
    project_name = models.CharField(max_length=50)
    description = models.CharField(max_length=500, null=True, blank=True)

    def __str__(self):
        return self.project_name


class Report(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="reports")
    target = models.CharField(max_length=250)

    def __str__(self):
        return f"{self.target_name} ({self.project})"


class Find(models.Model):
    report = models.ForeignKey(Report, on_delete=models.CASCADE, related_name="finds")
    reconnaissance = models.CharField(max_length=500)
    weaponization = models.CharField(max_length=500)
    delivery = models.CharField(max_length=500)
    exploitation = models.CharField(max_length=500)
    installation = models.CharField(max_length=500)
    commandcontrol = models.CharField(max_length=500)
    actions = models.CharField(max_length=500)
    vulnerability = models.TextField()  # descripción propia del hallazgo
    cve = models.CharField(max_length=32, blank=True, null=True)  # ID del CVE
       
    # Nuevo campo para el archivo de escaneo
    recon_file = models.FileField(upload_to='recon/', blank=True, null=True)

    def __str__(self):
        return f"Findings for {self.report}"



class Vuln(models.Model):
    vuln_name = models.CharField(max_length=80)

    def __str__(self):
        return self.vuln_name


class CVE(models.Model):
    cve_id = models.CharField(max_length=15)
