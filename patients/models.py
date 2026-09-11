from django.db import models
from django.contrib.auth.models import User


class PatientProfile(models.Model):
    """Профиль пациента"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='patient_profile')
    first_name = models.CharField(max_length=50, blank=True, verbose_name='Имя')
    last_name = models.CharField(max_length=50, blank=True, verbose_name='Фамилия')
    middle_name = models.CharField(max_length=50, blank=True, verbose_name='Отчество')
    date_of_birth = models.DateField(verbose_name='Дата рождения')
    phone = models.CharField(max_length=20, verbose_name='Телефон')
    emergency_contact_name = models.CharField(max_length=100, verbose_name='Имя экстренного контакта')
    emergency_contact_phone = models.CharField(max_length=20, verbose_name='Телефон экстренного контакта')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"


class Exercise(models.Model):
    """Упражнение для реабилитации"""
    name = models.CharField(max_length=200, verbose_name='Название')
    description = models.TextField(verbose_name='Описание')
    video_url = models.URLField(blank=True, null=True, verbose_name='Ссылка на видео')
    image = models.ImageField(upload_to='exercises/', blank=True, null=True, verbose_name='Фото упражнения')
    rehab_stage = models.CharField(
        max_length=50,
        choices=[
            ('early', 'Ранний'),
            ('mid', 'Средний'),
            ('late', 'Поздний'),
        ],
        default='early',
        verbose_name='Этап реабилитации'
    )

    def __str__(self):
        return self.name

class DailyPlan(models.Model):
    """План упражнений на день"""
    patient = models.ForeignKey(PatientProfile, on_delete=models.CASCADE, related_name='daily_plans')
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    date = models.DateField(verbose_name='Дата')
    end_date = models.DateField(blank=True, null=True, verbose_name='Дата окончания')
    notes = models.TextField(blank=True, null=True, verbose_name='Заметки')
    repetitions = models.IntegerField(blank=True, null=True, verbose_name='Количество повторений')
    duration_minutes = models.IntegerField(blank=True, null=True, verbose_name='Длительность (минут)')

    class Meta:
        unique_together = ['patient', 'exercise', 'date']

    def __str__(self):
        return f"{self.patient} — {self.exercise} ({self.date})"


class IsDone(models.Model):
    """Булевое значение выполнения одного упражнения в рамках одного дня"""
    daily_plan = models.ForeignKey(DailyPlan, on_delete=models.CASCADE, related_name='completions')
    date = models.DateField()
    completed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('daily_plan', 'date')


class ProsthesisLog(models.Model):
    """Учёт времени ношения протеза"""
    patient = models.ForeignKey(PatientProfile, on_delete=models.CASCADE, related_name='prosthesis_logs')
    date = models.DateField(verbose_name='Дата')
    minutes_worn = models.IntegerField(verbose_name='Минуты ношения')
    discomfort_level = models.IntegerField(
        choices=[(i, i) for i in range(1, 11)],
        blank=True,
        null=True,
        verbose_name='Уровень дискомфорта (1-10)'
    )
    notes = models.TextField(blank=True, null=True, verbose_name='Заметки')

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return f"{self.patient} — {self.date}: {self.minutes_worn} мин."
    
class Activity(models.Model):
    """Собственная активность пациента"""
    patient = models.ForeignKey(PatientProfile, on_delete=models.CASCADE, related_name='activities')
    name = models.CharField(max_length=200, verbose_name='Название активности')
    duration = models.IntegerField(verbose_name='Длительность (минут)')
    date = models.DateField(verbose_name='Дата')
    notes = models.TextField(blank=True, null=True, verbose_name='Заметки')
    
    class Meta:
        verbose_name = 'activity'
        verbose_name_plural = 'activities'
        ordering = ['-date']

    def __str__(self):
        return f"{self.patient} — {self.name} ({self.date})"


class EmergencyContact(models.Model):
    """Экстренный контакт пациента"""
    patient = models.ForeignKey(PatientProfile, on_delete=models.CASCADE, related_name='emergency_contacts')
    name = models.CharField(max_length=100, verbose_name='Имя')
    phone = models.CharField(max_length=20, verbose_name='Телефон')
    relation = models.CharField(max_length=50, verbose_name='Кем приходится', blank=True, null=True)

    def __str__(self):
        return f"{self.name} ({self.phone})"