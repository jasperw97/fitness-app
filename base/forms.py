from django.contrib.auth.forms import UserCreationForm
from base.models import User, Workout, Exercise
from django import forms
from crispy_bootstrap5.bootstrap5 import FloatingField
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout

class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", 'email', "first_name", "last_name", 'bio', 'password1', 'password2', 'pic']

# class WorkoutForm(forms.ModelForm):
#     class Meta:
#         model = Workout
#         fields = ["title"]

# class ExerciseForm(forms.ModelForm):
#     class Meta:
#         model= Exercise
#         fields = "__all__"

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["username", "email", "first_name", "last_name", "bio", "goal", "pic"]
        # def __init__(self, *args, **kwargs):
        #     super(UserForm, self).__init__(*args, **kwargs)
        #     self.helper = FormHelper()
        #     self.helper.layout = Layout(
        #         FloatingField('username'),
        #         FloatingField('email'),  
        #         # Render first_name field with floating label
        #                # Render email field with floating label
        #         # Add more FloatingField for other fields as needed
        #     )
        
    
    def clean_username(self):
        username = self.cleaned_data.get("username")
        # Get the username of the instance (user being edited)
        current_username = self.instance.username if self.instance else None
        # Check if the username already exists for other users
        if User.objects.exclude(username=current_username).filter(username=username).exists():
            raise forms.ValidationError("Username already exists. Please choose a different one.")
        return username
        