from django.db import models


class Participant(models.Model):
    name = models.CharField(max_length=100)
    colour = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Competition(models.Model):
    name = models.CharField(max_length=100)
    date_and_time = models.DateTimeField()
    participants = models.ManyToManyField(Participant)

    def __str__(self):
        return self.name


class Result(models.Model):
    race = models.ForeignKey(Competition, on_delete=models.CASCADE)
    racer = models.ForeignKey(Participant, on_delete=models.CASCADE)
    position = models.IntegerField()

    def __str__(self):
        return f"{self.race.name} - {self.racer.name} - {self.position}"


class Pick(models.Model):
    race = models.ForeignKey(Competition, on_delete=models.CASCADE)
    racer = models.ForeignKey(Participant, on_delete=models.CASCADE)
    user = models.ForeignKey("auth.User", on_delete=models.CASCADE)
