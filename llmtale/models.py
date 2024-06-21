from django.db import models


class Agent(models.Model):
    name = models.CharField(max_length=100)
    backstory = models.TextField() 
    base_image = models.ImageField(upload_to="agents/")

    def __str__(self):
        return self.name

    def greeting(self):
        pass


class History(models.Model):
    agent = models.ForeignKey(Agent, on_delete=models.CASCADE)
    message = models.TextField()
