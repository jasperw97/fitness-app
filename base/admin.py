from django.contrib import admin
from base.models import User, Workout, Exercise, LoadModel, SetsModel, RepsModel, ExerciseList
# Register your models here.
admin.site.register(User)
admin.site.register(Workout)
admin.site.register(Exercise)
admin.site.register(LoadModel)
admin.site.register(SetsModel)
admin.site.register(RepsModel)
admin.site.register(ExerciseList)