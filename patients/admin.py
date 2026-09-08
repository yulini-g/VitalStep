from django.contrib import admin
from .models import PatientProfile, Exercise, DailyPlan, ProsthesisLog, Activity, EmergencyContact

@admin.register(PatientProfile)
class PatientProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'date_of_birth', 'phone', 'emergency_contact_name')
    search_fields = ('user__username', 'user__first_name', 'user__last_name')

@admin.register(Exercise)
class ExerciseAdmin(admin.ModelAdmin):
    list_display = ('name', 'rehab_stage', 'video_url')
    list_filter = ('rehab_stage',)
    search_fields = ('name', 'description')

@admin.register(DailyPlan)
class DailyPlanAdmin(admin.ModelAdmin):
    list_display = ('patient', 'exercise', 'date', 'is_done')
    list_filter = ('is_done', 'date')
    search_fields = ('patient__user__username', 'exercise__name')

@admin.register(ProsthesisLog)
class ProsthesisLogAdmin(admin.ModelAdmin):
    list_display = ('patient', 'date', 'minutes_worn', 'discomfort_level')
    list_filter = ('date', 'discomfort_level')
    
@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = ('patient', 'name', 'duration', 'date')
    list_filter = ('date',)
    search_fields = ('name', 'patient__user__username')

@admin.register(EmergencyContact)
class EmergencyContactAdmin(admin.ModelAdmin):
    list_display = ('patient', 'name', 'phone', 'relation')
    search_fields = ('name', 'phone', 'patient__user__username')