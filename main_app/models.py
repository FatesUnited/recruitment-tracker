from django.db import models
from django.contrib.postgres.fields import ArrayField

class Member(models.Model):
    username = models.CharField(max_length=100, unique=True)
    timezone = models.CharField(max_length=100, blank=True, null=True)
    interviewed_by = models.IntegerField(blank=True, null=True)
    esi_check_by = models.IntegerField(blank=True, null=True)
    onboarded_by = models.IntegerField(blank=True, null=True)
    corporation = models.CharField(max_length=100, blank=True, null=True)
    join_date = models.DateField(blank=True, null=True)
    notes = models.TextField(max_length=500, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    member_state = models.CharField(max_length=100, blank=True, null=True)
    num_of_characters = models.IntegerField(blank=True, null=True)
    registry_number = models.CharField(max_length=100, blank=True, null=True)
    current_status = models.CharField(max_length=100, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)
    graduation_date = models.DateField(blank=True, null=True)
    attrition_headcount = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.username

