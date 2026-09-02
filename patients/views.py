from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import PatientProfile

def home(request):
    return render(request, 'patients/home.html')

@login_required
def profile(request):
    try:
        patient_profile = request.user.patient_profile
    except PatientProfile.DoesNotExist:
        patient_profile = None
    return render(request, 'patients/profile.html', {'patient_profile': patient_profile})
