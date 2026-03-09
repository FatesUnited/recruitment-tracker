from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from datetime import date

CORPORATIONS = (
    ('TL', 'Tidal Lock'),
    ('VL', 'Vapor Lock.')
)

TIMEZONES = (
    ('US', 'US'),
    ('EU', 'EU'),
    ('AU', 'AU')
)

MEMBER_STATES = (
    ('Recruit', 'Recruit'),
    ('Member', 'Member')
)

STATUS_CHOICES = (
    ('Pending', 'Pending'),
    ('Recruit', 'Recruit'),
    ('Member', 'Member'),
    ('Purged', 'Purged'),
    ('Rejected', 'Rejected'),
    ('Declined', 'Declined'),
    ('Left', 'Left'),
    ('Kicked', 'Kicked')
)

class Member(models.Model):
    username = models.CharField(max_length=100, unique=True)
    timezone = models.CharField(max_length=100, choices=TIMEZONES, default=TIMEZONES[0][0], blank=True, null=True)
    interviewed_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name='interviewed_members', blank=True, null=True)
    esi_checked_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name='esi_checked_members', blank=True, null=True)
    onboarded_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name='onboarded_members', blank=True, null=True)
    corporation = models.CharField(max_length=100, choices=CORPORATIONS, default=CORPORATIONS[0][0], blank=True, null=True)
    join_date = models.DateField(blank=True, null=True)
    notes = models.TextField(max_length=500, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    member_state = models.CharField(max_length=100, choices=MEMBER_STATES, default=MEMBER_STATES[0][0], blank=True, null=True)
    num_of_characters = models.IntegerField(blank=True, null=True)
    registry_number = models.CharField(max_length=100, blank=True, null=True)
    current_status = models.CharField(max_length=100, choices=STATUS_CHOICES, default=STATUS_CHOICES[0][0], blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)
    graduation_date = models.DateField(blank=True, null=True)
    attrition_headcount = models.IntegerField(blank=True, null=True)
    eve_character_id = models.BigIntegerField(blank=True, null=True, unique=True)

    @property
    def portrait_url(self):
        if self.eve_character_id:
            return f"https://images.evetech.net/characters/{self.eve_character_id}/portrait?size=256"
        return None
    
    def __str__(self):
        return self.username

    def get_absolute_url(self):
        return reverse('member_detail', kwargs={'member_id': self.id})
    
    @property
    def days_in_recruit(self):
        if self.current_status == 'Recruit' and self.join_date:
            return (date.today() - self.join_date).days
        return None
    
class Comment(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='comments')
    comment_text = models.TextField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'Comment for {self.member.username} at {self.created_at}'