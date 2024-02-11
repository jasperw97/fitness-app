from django.shortcuts import render
from django.views import View
from base.models import ExerciseList, SetsModel, RepsModel, LoadModel, Exercise, Workout, User, GoalsModel
from django.shortcuts import redirect, reverse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from base.forms import RegisterForm, UserForm
from django.http import HttpResponse
from django.db.models import Q
# Create your views here.

class LoginPage(View):
    def get(self, request):
        
        if request.user.is_authenticated:
            return redirect("base:home")
        ctx = {"page":"login"}
        return render(request, "base/login.html", ctx)
    
    def post(self, request):
        email = request.POST.get("email").lower()
        password = request.POST.get("password")
        try:
            user = User.objects.get(email=email)
        except:
            messages.error(request, "User does not exist")
        
        user = authenticate(request, username=email, password=password)

        if user is not None:
            login(request, user)
            return redirect("base:home")
        else:
            messages.error(request, "Username or password incorrect")
        ctx = {}
        return redirect("base:login")

class RegisterPage(View):
    def get(self, request):
        
        if request.user.is_authenticated:
            return redirect("base:home")
        form = RegisterForm()
        ctx = {"form":form}
        return render(request, "base/register.html", ctx)
    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            # user.username = user.username.lower()
            user.save()
            
            login(request, user)
            return redirect("base:home")
        else:
            messages.error(request, "An error occured during registeration!!")
            return(redirect("base:register"))
            

def logoutuser(request):
    logout(request)
    return redirect("base:home")

class HomeView(View):
    template_name = 'base/home.html'
    def get(self, request):
        search = request.GET.get("search") if request.GET.get("search") != None else ''
        if request.GET.get("goal") == None:
            workouts = Workout.objects.filter(
                Q(goal__goal__icontains=search) |
                Q(title__icontains=search) |
                Q(user__username__icontains=search) |
                Q(exercises__name__name__icontains=search)
            ).distinct()
            # workouts = Workout.objects.all()
        else:
            goal = GoalsModel.objects.get(goal=request.GET.get("goal"))
            workouts = Workout.objects.filter(goal=goal.pk).filter(
                Q(goal__goal__icontains=search) |
                Q(title__icontains=search) |
                Q(user__username__icontains=search) |
                Q(exercises__name__name__icontains=search)
            ).distinct()

        
        ctx = {"workouts":workouts}

        return render(request, self.template_name, ctx)

class CreateWorkout(View):
    template_name = 'base/workout_form.html'
    def get(self, request):
        exercises = ExerciseList.objects.all()
        ctx = {"exercises":exercises, "len":1, "goals":GoalsModel.objects.all(), "page":"create"}
        return render(request, self.template_name, ctx)
    
    def post(self, request):
        result = list(request.POST.items())
        exercises = (len(result)-3)/4
        title = request.POST.get("title")
        goal, created = GoalsModel.objects.get_or_create(goal=request.POST.get("goal"))
        workout = Workout.objects.create(title=title, user=request.user, goal=goal)
        for i in range(1, int(exercises)+1):
            
            exercise_name, created = ExerciseList.objects.get_or_create(name=request.POST.get("exercise"+str(i))) 
            sets, created = SetsModel.objects.get_or_create(sets=request.POST.get("sets"+str(i))) 
            reps, created = RepsModel.objects.get_or_create(reps=request.POST.get("reps"+str(i)))
            load, created = LoadModel.objects.get_or_create(load=request.POST.get("load"+str(i)))
            description = request.POST.get("description"+str(i))
            exercise = Exercise.objects.create(name=exercise_name, load=load, sets=sets, reps=reps, description=description)
            workout.exercises.add(exercise)


        return redirect("base:home")

class DeleteWorkout(View):
    template_name = "base/delete.html"
    def get(self, request, pk):
        obj = Workout.objects.get(pk=pk)
        ctx = {"obj":obj}
        return render(request, self.template_name, ctx)
    def post(self, request, pk):
        workout = Workout.objects.get(pk=pk)
        workout.delete()
        return redirect("base:home")

class UpdateWorkout(View):
    template_name="base/workout_form.html"
    def get(self, request, pk):
        workout = Workout.objects.get(pk=pk)
        count = len(workout.exercises.all())
        ctx = {"workout":workout, "len":count, "goals":GoalsModel.objects.all(), "exercises":ExerciseList.objects.all()}
        return render(request, self.template_name, ctx)
    def post(self, request, pk):
        workout = Workout.objects.get(pk=pk)
        original_length = len(workout.exercises.all())
        result = list(request.POST.items())
        exercises = (len(result)-3)/4
        workout.title = request.POST.get("title")
        workout.goal, created = GoalsModel.objects.get_or_create(goal=request.POST.get("goal"))
        #Updating part
        for i in range(1, int(original_length)+1):
            exercise = workout.exercises.all()[i-1]
            exercise.name, created = ExerciseList.objects.get_or_create(name=request.POST.get("exercise"+str(i)))
            exercise.sets, created = SetsModel.objects.get_or_create(sets=request.POST.get("sets"+str(i))) 
            exercise.reps, created = RepsModel.objects.get_or_create(reps=request.POST.get("reps"+str(i)))
            exercise.load, created = LoadModel.objects.get_or_create(load=request.POST.get("load"+str(i)))
            exercise.description = request.POST.get("description"+str(i))
            exercise.save()
        workout.save()  

        #Creating Part
        for i in range(int(original_length)+1, int(exercises)+1):
            
            exercise_name, created = ExerciseList.objects.get_or_create(name=request.POST.get("exercise"+str(i))) 
            sets, created = SetsModel.objects.get_or_create(sets=request.POST.get("sets"+str(i))) 
            reps, created = RepsModel.objects.get_or_create(reps=request.POST.get("reps"+str(i)))
            load, created = LoadModel.objects.get_or_create(load=request.POST.get("load"+str(i)))
            description = request.POST.get("description"+str(i))
            exercise = Exercise.objects.create(name=exercise_name, load=load, sets=sets, reps=reps, description=description)
            workout.exercises.add(exercise)
        

        return redirect("base:home")

class UserProfileView(View):
    template_name = "base/userprofile.html"
    def get(self, request, pk):
        workouts = Workout.objects.filter(user=pk)
        ctx = {"workouts":workouts, "profileuser":User.objects.get(pk=pk)}
        return render(request, self.template_name, ctx)

class UserEditView(View):
    template_name = "base/profile_form.html"
    
    def get(self, request, pk):
        user = User.objects.get(pk=pk)
        
        form = UserForm(instance=user)
        
        ctx = {"form":form}
        return render(request, self.template_name, ctx)
    
    def post(self, request, pk):
        user = User.objects.get(pk=pk)
        form = UserForm(request.POST, request.FILES, instance=user)
        if not form.is_valid() :
            ctx = {'form' : form}
            messages.error(request, "Form not valid")
            return render(request, self.template_name, ctx)
        else:
            form.save()
            return redirect("base:userprofile", pk=pk)
