from django.db import models

class Project(models.Model):
    project_name = models.CharField(max_length=30)
    
class Report(models.Model):
    project_id = models.Project.project_id
    target_name = models.CharField(max_length=250)
    
class Finding(models.Model):
    report_id = models.Report.report_id
    reconnaissance = models.CharField(max_length=500)
    weaponization = models.CharField(max_length=500)
    delivery = models.CharField(max_length=500)
    explotation = models.CharField(max_length=500)
    installation = models.CharField(max_length=500)
    commandcontrol = models.CharField(max_length=500)
    actions = models.CharField(max_length=500)