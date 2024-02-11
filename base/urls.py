from django.urls import path
from . import views
from django.views.generic import TemplateView

app_name = "base"
urlpatterns = [
    path("", views.HomeView.as_view(), name="home"),
    path("create-workout", views.CreateWorkout.as_view(), name="create_workout"),
    path("login", views.LoginPage.as_view(), name="login"),
    path("logout", views.logoutuser, name="logout"),
    path("register", views.RegisterPage.as_view(), name="register"),
    path("workout-delete/<int:pk>", views.DeleteWorkout.as_view(), name="workout_delete"),
    path("update-workout/<int:pk>", views.UpdateWorkout.as_view(), name="workout_update"),
    path("userprofile/<int:pk>", views.UserProfileView.as_view(), name="userprofile"),
    path("userupdate/<int:pk>", views.UserEditView.as_view(), name="user_edit"),
]