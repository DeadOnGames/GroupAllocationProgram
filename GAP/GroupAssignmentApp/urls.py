from django.urls import path
from . import views

app_name = "gaa"
urlpatterns = [
    path("user/<int:person_id>/", views.person_view, name="user"),
    path(
        "<int:supervisor_id>/register_participant/", views.person_details_form, name="person_details"
    ),
    path(
        "<int:supervisor_id>/register_participant/thanks/",
        views.participant_registration_success,
        name="thanks",
    ),
]
