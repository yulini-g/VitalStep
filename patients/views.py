from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import PatientProfile, Activity, EmergencyContact
from .forms import ActivityForm

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
    return render(request, 'patients/plan.html')

@login_required
def prosthesis(request):
    return render(request, 'patients/prosthesis.html')