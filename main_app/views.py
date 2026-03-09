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
from collections import defaultdict
from datetime import date
from django.db.models import Count, Q


class Home(LoginView):
    template_name = 'home.html'

def about(request):
    return render(request, 'about.html')

@login_required
def members_index(request):
    query = request.GET.get('q', '').strip()

    members = Member.objects.filter(current_status__in=['Member','Recruit'])

    if query:
        members = members.filter(Q(username__icontains=query))
        
    return render(request, 'members/index.html', {'members': members, 'query': query, 'clear_url': request.path})

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
def recruitment(request):
    query = request.GET.get('q', '').strip()

    members = Member.objects.filter(current_status__in=['Pending', 'Recruit']).order_by('created_at')

    if query:
        members = members.filter(Q(username__icontains=query))

    return render(request, 'members/recruitment.html', {'members': members, 'query': query, 'clear_url': request.path,})

@login_required
def historical(request):
    query = request.GET.get('q', '').strip()

    members = Member.objects.all()

    if query:
        members = members.filter(Q(username__icontains=query))

    return render(request, 'members/historical.html', {'members': members, 'query': query, 'clear_url': request.path})

@login_required
def graduation(request):
    query = request.GET.get('q', '').strip()

    members = Member.objects.filter(graduation_date__isnull=False)

    if query:
        members = members.filter(Q(username__icontains=query))

    return render(request, 'members/graduation.html', {'members': members, 'query': query, 'clear_url': request.path})

@login_required
def attrition(request):
    query = request.GET.get('q', '').strip()

    members = Member.objects.filter(current_status__in=['Purged','Left','Kicked'])

    if query:
        members = members.filter(Q(username__icontains=query))

    return render(request, 'members/attrition.html', {'members': members, 'query': query, 'clear_url': request.path})

@login_required
def analytics(request):
    today = date.today()
    current_month = today.month
    next_month = 1 if current_month == 12 else current_month + 1

    all_members = Member.objects.all()

    # Core totals
    active_members = Member.objects.filter(member_state='Member').count()
    active_recruits = Member.objects.filter(member_state='Recruit').count()
    total_records = all_members.count()
    total_attrition = Member.objects.filter(current_status__in=['Purged', 'Left', 'Kicked']).count()

    # Timezone breakdown for active member states
    timezone_breakdown = (
        Member.objects
        .filter(member_state__in=['Member', 'Recruit'])
        .values('timezone', 'member_state')
        .annotate(total=Count('id'))
        .order_by('timezone', 'member_state')
    )

    timezone_stats = {
        'US': {'Member': 0, 'Recruit': 0},
        'EU': {'Member': 0, 'Recruit': 0},
        'AU': {'Member': 0, 'Recruit': 0},
    }

    for row in timezone_breakdown:
        tz = row['timezone'] or 'Unknown'
        state = row['member_state']
        if tz in timezone_stats and state in timezone_stats[tz]:
            timezone_stats[tz][state] = row['total']

    # Corporation breakdown
    corporation_breakdown = (
        Member.objects
        .filter(member_state__in=['Member', 'Recruit'])
        .values('corporation')
        .annotate(total=Count('id'))
        .order_by('-total')
    )

    # Tenure buckets for active members/recruits with join_date
    tenure_buckets = {
        'months_0_5': 0,
        'months_6_11': 0,
        'months_12_17': 0,
        'months_18_23': 0,
        'months_24_29': 0,
        'months_30_35': 0,
        'months_36_41': 0,
        'months_42_47': 0,
    }

    tenure_queryset = Member.objects.filter(
        member_state__in=['Member', 'Recruit'],
        join_date__isnull=False
    )

    for member in tenure_queryset:
        delta = today - member.join_date
        tenure_months = delta.days // 30

        if tenure_months <= 5:
            tenure_buckets['months_0_5'] += 1
        elif tenure_months <= 11:
            tenure_buckets['months_6_11'] += 1
        elif tenure_months <= 17:
            tenure_buckets['months_12_17'] += 1
        elif tenure_months <= 23:
            tenure_buckets['months_18_23'] += 1
        elif tenure_months <= 29:
            tenure_buckets['months_24_29'] += 1
        elif tenure_months <= 35:
            tenure_buckets['months_30_35'] += 1
        elif tenure_months <= 41:
            tenure_buckets['months_36_41'] += 1
        elif tenure_months <= 47:
            tenure_buckets['months_42_47'] += 1
        

    # Recruitment outcomes
    recruitment_outcomes = {
        'Recruit': Member.objects.filter(current_status='Recruit').count(),
        'Member': Member.objects.filter(current_status='Member').count(),
        'Rejected': Member.objects.filter(current_status='Rejected').count(),
        'Declined': Member.objects.filter(current_status='Declined').count(),
        'Pending': Member.objects.filter(current_status='Pending').count(),
    }

    # Graduation stats
    graduated_total = Member.objects.filter(graduation_date__isnull=False).count()

    graduation_by_month = (
        Member.objects
        .filter(graduation_date__isnull=False)
        .extra(select={'grad_month': "EXTRACT(MONTH FROM graduation_date)"})
        .values('grad_month')
        .annotate(total=Count('id'))
        .order_by('grad_month')
    )

    # Conversion / rejection rates
    recruit_count = recruitment_outcomes['Recruit']
    member_count = recruitment_outcomes['Member']
    rejected_count = recruitment_outcomes['Rejected']
    declined_count = recruitment_outcomes['Declined']

    conversion_denominator = recruit_count + member_count
    conversion_rate = round((member_count / conversion_denominator) * 100, 1) if conversion_denominator else 0

    rejection_denominator = recruit_count + member_count + rejected_count + declined_count
    rejection_rate = round(((rejected_count + declined_count) / rejection_denominator) * 100, 1) if rejection_denominator else 0

    # Attrition stats
    attrition_breakdown = {
        'Left': Member.objects.filter(current_status='Left').count(),
        'Kicked': Member.objects.filter(current_status='Kicked').count(),
        'Purged': Member.objects.filter(current_status='Purged').count(),
    }

    voluntary_attrition = attrition_breakdown['Left']
    involuntary_attrition = attrition_breakdown['Kicked'] + attrition_breakdown['Purged']

    attrition_by_timezone = (
        Member.objects
        .filter(current_status__in=['Purged', 'Left', 'Kicked'])
        .values('timezone')
        .annotate(total=Count('id'))
        .order_by('-total')
    )

    attrition_by_corporation = (
        Member.objects
        .filter(current_status__in=['Purged', 'Left', 'Kicked'])
        .values('corporation')
        .annotate(total=Count('id'))
        .order_by('-total')
    )

    # Anniversaries by join month
    current_month_anniversaries = Member.objects.filter(
        join_date__month=current_month,
        member_state__in=['Member', 'Recruit']
    ).order_by('join_date')

    next_month_anniversaries = Member.objects.filter(
        join_date__month=next_month,
        member_state__in=['Member', 'Recruit']
    ).order_by('join_date')

    anniversary_groups = defaultdict(list)
    anniversary_queryset = Member.objects.filter(
        join_date__isnull=False,
        member_state__in=['Member', 'Recruit']
    ).order_by('join_date')

    month_names = {
        1: 'January', 2: 'February', 3: 'March', 4: 'April',
        5: 'May', 6: 'June', 7: 'July', 8: 'August',
        9: 'September', 10: 'October', 11: 'November', 12: 'December',
    }

    for member in anniversary_queryset:
        anniversary_groups[month_names[member.join_date.month]].append(member)

    # Recruiter contribution
    interview_stats = (
        Member.objects
        .filter(interviewed_by__isnull=False)
        .values('interviewed_by__username')
        .annotate(total=Count('id'))
        .order_by('-total')
    )

    esi_stats = (
        Member.objects
        .filter(esi_checked_by__isnull=False)
        .values('esi_checked_by__username')
        .annotate(total=Count('id'))
        .order_by('-total')
    )

    onboarding_stats = (
        Member.objects
        .filter(onboarded_by__isnull=False)
        .values('onboarded_by__username')
        .annotate(total=Count('id'))
        .order_by('-total')
    )

    # Data quality / attention-needed stats
    missing_registry = Member.objects.filter(
        Q(registry_number__isnull=True) | Q(registry_number=''),
        member_state__in=['Member', 'Recruit']
    ).count()

    missing_interviewer = Member.objects.filter(
        member_state__in=['Member', 'Recruit'],
        interviewed_by__isnull=True
    ).count()

    missing_portrait_id = Member.objects.filter(
        member_state__in=['Member', 'Recruit'],
        eve_character_id__isnull=True
    ).count()

    context = {
        'active_members': active_members,
        'active_recruits': active_recruits,
        'total_records': total_records,
        'total_attrition': total_attrition,

        'timezone_stats': timezone_stats,
        'corporation_breakdown': corporation_breakdown,
        'tenure_buckets': tenure_buckets,

        'recruitment_outcomes': recruitment_outcomes,
        'graduated_total': graduated_total,
        'graduation_by_month': graduation_by_month,
        'conversion_rate': conversion_rate,
        'rejection_rate': rejection_rate,

        'attrition_breakdown': attrition_breakdown,
        'voluntary_attrition': voluntary_attrition,
        'involuntary_attrition': involuntary_attrition,
        'attrition_by_timezone': attrition_by_timezone,
        'attrition_by_corporation': attrition_by_corporation,

        'current_month_anniversaries': current_month_anniversaries,
        'next_month_anniversaries': next_month_anniversaries,
        'anniversary_groups': dict(anniversary_groups),

        'interview_stats': interview_stats,
        'esi_stats': esi_stats,
        'onboarding_stats': onboarding_stats,

        'missing_registry': missing_registry,
        'missing_interviewer': missing_interviewer,
        'missing_portrait_id': missing_portrait_id,
    }

    return render(request, 'analytics.html', context)

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

class MemberDelete(LoginRequiredMixin, DeleteView):
    model = Member
    success_url = '/members/'
