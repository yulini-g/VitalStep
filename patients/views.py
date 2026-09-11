from datetime import date, datetime, timedelta
from django.shortcuts import render, redirect, get_object_or_404
from .forms import ActivityForm, ProsthesisLogForm, UserRegisterForm
from django.contrib.auth.decorators import login_required
from .models import PatientProfile, Activity, EmergencyContact, ProsthesisLog, DailyPlan, Exercise, IsDone

def home(request):
    return render(request, 'patients/home.html')

@login_required
def profile(request):
    try:
        patient_profile = request.user.patient_profile
        emergency_contacts = patient_profile.emergency_contacts.all()
    except PatientProfile.DoesNotExist:
        patient_profile = None
        emergency_contacts = []
    return render(request, 'patients/profile.html', {
        'patient_profile': patient_profile,
        'emergency_contacts': emergency_contacts,
    })

@login_required
def activities(request):
    try:
        patient_profile = request.user.patient_profile
    except PatientProfile.DoesNotExist:
        patient_profile = None

    if request.method == 'POST':
        form = ActivityForm(request.POST)
        if form.is_valid():
            activity = form.save(commit=False)
            activity.patient = patient_profile
            activity.save()
            return redirect('activities')
    else:
        form = ActivityForm()

    activities_list = Activity.objects.filter(patient=patient_profile)

    return render(request, 'patients/activities.html', {
        'form': form,
        'activities_list': activities_list,
    })

@login_required
def plan(request):
    try:
        patient_profile = request.user.patient_profile
    except PatientProfile.DoesNotExist:
        return redirect('profile')

    selected_date = request.GET.get('date')
    if selected_date:
        selected_date = datetime.strptime(selected_date, '%Y-%m-%d').date()
    else:
        selected_date = date.today()

    if request.method == 'POST':
        plan_id = request.POST.get('plan_id')
        action = request.POST.get('action', 'complete')

        daily_plan = DailyPlan.objects.filter(id=plan_id, patient=patient_profile).first()
        if daily_plan:
            if action == 'complete':
                IsDone.objects.get_or_create(
                    daily_plan=daily_plan,
                    date=selected_date,
                )
            elif action == 'uncomplete':
                IsDone.objects.filter(
                    daily_plan=daily_plan,
                    date=selected_date,
                ).delete()

        return redirect(f'/plan/?date={selected_date.isoformat()}')

    today = date.today()
    plans = DailyPlan.objects.filter(
        patient=patient_profile,
        date__lte=selected_date,
        end_date__gte=selected_date,
    ) | DailyPlan.objects.filter(
        patient=patient_profile,
        date=selected_date,
        end_date__isnull=True,
    )

    done_ids = set(
        IsDone.objects
        .filter(date=selected_date, daily_plan__in=plans)
        .values_list('daily_plan_id', flat=True)
    )

    for p in plans:
        p.is_done_today = p.id in done_ids

    if selected_date == today:
        header = 'План упражнений на сегодня'
    elif selected_date == today - timedelta(days=1):
        header = 'План упражнений на вчера'
    elif selected_date == today + timedelta(days=1):
        header = 'План упражнений на завтра'
    else:
        header = f'План упражнений на {selected_date.strftime("%d.%m.%y")}'

    return render(request, 'patients/plan.html', {
        'plans': plans,
        'header': header,
        'selected_date': selected_date.strftime('%Y-%m-%d'),
    })

@login_required
def prosthesis(request):
    try:
        patient_profile = request.user.patient_profile
    except PatientProfile.DoesNotExist:
        return redirect('profile')

    if request.method == 'POST':
        form = ProsthesisLogForm(request.POST)
        if form.is_valid():
            log = form.save(commit=False)
            log.patient = patient_profile
            log.save()
            return redirect('prosthesis')
    else:
        form = ProsthesisLogForm()

    logs = ProsthesisLog.objects.filter(patient=patient_profile)

    return render(request, 'patients/prosthesis.html', {
        'form': form,
        'logs': logs,
    })

@login_required
def progress(request):
    try:
        patient_profile = request.user.patient_profile
    except PatientProfile.DoesNotExist:
        return redirect('profile')

    done_count = IsDone.objects.filter(daily_plan__patient=patient_profile).count()
    total_count = DailyPlan.objects.filter(patient=patient_profile).count()

    logs = ProsthesisLog.objects.filter(patient=patient_profile).order_by('date')
    activities = Activity.objects.filter(patient=patient_profile).order_by('date')

    return render(request, 'patients/progress.html', {
        'done_count': done_count,
        'total_count': total_count,
        'logs': logs,
        'activities': activities,
    })

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'patients/register.html', {'form': form})

def exercise_detail(request, exercise_id):
    exercise = get_object_or_404(Exercise, id=exercise_id)
    return render(request, 'patients/exercise_detail.html', {'exercise': exercise})