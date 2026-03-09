from django.shortcuts import render, redirect
from .models import Member
from .forms import CommentForm
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.views import LoginView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .utils import resolve_eve_character_id

class Home(LoginView):
    template_name = 'home.html'

def about(request):
    return render(request, 'about.html')

@login_required
def members_index(request):
    members = Member.objects.filter(current_status__in=['Member','Recruit'])
    return render(request, 'members/index.html', {'members': members})

@login_required
def member_detail(request, member_id):
    member = Member.objects.get(id=member_id)
    comment_form = CommentForm()
    return render(request, 'members/detail.html', {
        'member': member,
        'comment_form': comment_form
    })

@login_required
def add_comment(request, member_id):
    member = Member.objects.get(id=member_id)
    form = CommentForm(request.POST)
    if form.is_valid():
        new_comment = form.save(commit=False)
        new_comment.member = member
        new_comment.user = request.user
        new_comment.save()
    return redirect('member_detail', member_id=member.id)

def signup(request):
    error_message = ''
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('members_index')
        else:
            error_message = 'Invalid sign up - try again'
    form = UserCreationForm()
    context = {'form': form, 'error_message': error_message}
    return render(request, 'signup.html', context)

@login_required
def historical(request):
    members = Member.objects.all()
    return render(request, 'members/historical.html', {'members': members})

@login_required
def graduation(request):
    members = Member.objects.filter(graduation_date__isnull=False)
    return render(request, 'members/graduation.html', {'members': members})

@login_required
def attrition(request):
    members = Member.objects.filter(current_status__in=['Purged','Left','Kicked'])
    return render(request, 'members/attrition.html', {'members': members})

@login_required
def analytics(request):
    return render(request, 'analytics.html')

class MemberCreate(LoginRequiredMixin, CreateView):
    model = Member
    fields = [
        'username',
        'timezone',
        'interviewed_by',
        'esi_checked_by',
        'onboarded_by',
        'corporation',
        'join_date',
        'notes',
        'member_state',
        'num_of_characters',
        'registry_number',
        'current_status',
        'graduation_date',
        'attrition_headcount'
    ]

    def form_valid(self, form):
        character_name = form.cleaned_data.get('username')
        character_id = resolve_eve_character_id(character_name)
        form.instance.eve_character_id = character_id
        return super().form_valid(form)

class MemberUpdate(LoginRequiredMixin, UpdateView):
    model = Member
    fields = [
        'username',
        'timezone',
        'interviewed_by',
        'esi_checked_by',
        'onboarded_by',
        'corporation',
        'join_date',
        'notes',
        'member_state',
        'num_of_characters',
        'registry_number',
        'current_status',
        'graduation_date',
        'attrition_headcount'
    ]

    def form_valid(self, form):
        if 'username' in form.changed_data:
            character_name = form.cleaned_data.get('username')
            character_id = resolve_eve_character_id(character_name)
            form.instance.eve_character_id = character_id
        return super().form_valid(form)

class MemberDelete(DeleteView):
    model = Member
    success_url = '/members/'
