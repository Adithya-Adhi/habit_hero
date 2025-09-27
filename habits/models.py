
from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Habit(models.Model):
    FREQUENCY_CHOICES = [
        ("daily", "Daily"),
        ("weekly", "Weekly"),
    ]
    name = models.CharField(max_length=200)
    frequency = models.CharField(max_length=20, choices=FREQUENCY_CHOICES)
    category = models.ForeignKey(Category, null=True, blank=True, on_delete=models.SET_NULL)
    start_date = models.DateField()

    def __str__(self):
        return self.name

class CheckIn(models.Model):
    habit = models.ForeignKey(Habit, on_delete=models.CASCADE, related_name="checkins")
    date = models.DateField()
    note = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.habit.name} - {self.date}"
