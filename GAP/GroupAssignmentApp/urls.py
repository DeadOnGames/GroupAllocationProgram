from django.urls import path
from . import views

app_name = "gaa"
urlpatterns = [path("user/<int:person_id>/", views.person_view, name="user")]
