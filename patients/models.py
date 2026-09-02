from django.db import models
from django.contrib.auth.models import User


class PatientProfile(models.Model):
    """Профиль пациента"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='patient_profile')
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
    difficulty = models.CharField(
        max_length=50,
        choices=[
            ('easy', 'Лёгкое'),
            ('medium', 'Среднее'),
            ('hard', 'Сложное'),
        ],
        default='easy',
        verbose_name='Сложность'
    )

    def __str__(self):
        return self.name


class DailyPlan(models.Model):
    """План упражнений на день"""
    patient = models.ForeignKey(PatientProfile, on_delete=models.CASCADE, related_name='daily_plans')
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    date = models.DateField(verbose_name='Дата')
    is_done = models.BooleanField(default=False, verbose_name='Выполнено')
    notes = models.TextField(blank=True, null=True, verbose_name='Заметки')

    class Meta:
        unique_together = ['patient', 'exercise', 'date']

    def __str__(self):
        return f"{self.patient} — {self.exercise} ({self.date})"


class ProsthesisLog(models.Model):
    """Учёт времени ношения протеза"""
    patient = models.ForeignKey(PatientProfile, on_delete=models.CASCADE, related_name='prosthesis_logs')
    date = models.DateField(verbose_name='Дата')
    hours_worn = models.FloatField(verbose_name='Часы ношения')
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
        return f"{self.patient} — {self.date}: {self.hours_worn} ч."