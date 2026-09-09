from datetime import date, datetime, timedelta
from django.shortcuts import render, redirect, get_object_or_404
from .forms import ActivityForm, ProsthesisLogForm, UserRegisterForm
from django.contrib.auth.decorators import login_required
from .models import PatientProfile, Activity, EmergencyContact, ProsthesisLog, DailyPlan, Exercise

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
        try:
            daily_plan = DailyPlan.objects.get(id=plan_id, patient=patient_profile)
            daily_plan.is_done = True
            daily_plan.save()
        except DailyPlan.DoesNotExist:
            pass
        return redirect(f'/plan/?date={selected_date}')

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

    done_count = DailyPlan.objects.filter(patient=patient_profile, is_done=True).count()
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