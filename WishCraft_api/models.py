from django.db import models

# Create your models here.

class UsersTemplates(models.Model):
    id = models.AutoField(primary_key=True)
    session_id = models.CharField(max_length=255, null=True, blank=True)
    token = models.CharField(max_length=255, unique=True, null=False, blank=False)
    template_code = models.CharField(max_length=15, unique=True, null=False, blank=False)
    template_id = models.CharField(max_length=5, null=False, blank=False)
    data = models.JSONField(null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Template Code: {self.template_code} - Template ID: {self.template_id}"

