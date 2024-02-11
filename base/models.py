from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class GoalsModel(models.Model):
    goal = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.goal

class User(AbstractUser):
    email = models.EmailField(unique=True, null=True)
    bio = models.TextField(null=True)
    goal = models.ForeignKey(GoalsModel, on_delete=models.SET_NULL, null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    pic = models.ImageField(null=True, default='person.svg')

class LoadModel(models.Model):
    load = models.FloatField()

    def __str__(self):
        return str(self.load)

class SetsModel(models.Model):
    sets = models.IntegerField()

    def __str__(self):
        return str(self.sets)

class RepsModel(models.Model):
    reps = models.IntegerField()

    def __str__(self):
        return str(self.reps)



class ExerciseList(models.Model):
    name = models.CharField(max_length=200)
    def __str__(self):
        return self.name

class Exercise(models.Model):
    name = models.ForeignKey(ExerciseList, blank=True, null=True, on_delete=models.SET_NULL)
    
    
    description = models.TextField(null=True)
    load = models.ForeignKey(LoadModel, blank=True, null=True, on_delete=models.SET_NULL)
    sets = models.ForeignKey(SetsModel, blank=True, null=True, on_delete=models.SET_NULL)
    reps = models.ForeignKey(RepsModel, blank=True, null=True, on_delete=models.SET_NULL)
    def __str__(self):
        return str(self.name)



class Workout(models.Model):
    class Meta:
        ordering = ["-created"]
    title = models.CharField(max_length=200, default="My workout")
    exercises = models.ManyToManyField(Exercise)
    created = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    goal = models.ForeignKey(GoalsModel, on_delete=models.SET_NULL, null=True)
    

    def __str__(self):
        return str(self.title)

