from django.shortcuts import render
from .models import Member

def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

def members_index(request):
    members = Member.objects.all()
    return render(request, 'members/index.html', {'members': members})

def member_detail(request, member_id):
    member = Member.objects.get(id=member_id)
    return render(request, 'members/detail.html', {'member': member})

def historical(request):
    return render(request, 'historical.html')

def graduation(request):
    return render(request, 'graduation.html')

def attrition(request):
    return render(request, 'attrition.html')

def analytics(request):
    return render(request, 'analytics.html')