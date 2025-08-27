from django.db import models

class Project(models.Model):
    project_name = models.CharField(max_length=30)

    def __str__(self):
        return self.project_name


class Report(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="reports")
    target_name = models.CharField(max_length=250)

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

    def __str__(self):
        return f"Findings for {self.report}"


class Vuln(models.Model):
    vuln_name = models.CharField(max_length=80)

    def __str__(self):
        return self.vuln_name


class CVE(model.Model):
    cve_id = models.CharField(max_length=15)
