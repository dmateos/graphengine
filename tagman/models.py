from django.db import models


class Schedule(models.Model):
    name = models.CharField(max_length=255)
    schedule = models.CharField(max_length=255)
    action = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class UniversalTag(models.Model):
    key = models.CharField(max_length=255)
    value = models.CharField(max_length=255)
    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.key}: {self.value}"
