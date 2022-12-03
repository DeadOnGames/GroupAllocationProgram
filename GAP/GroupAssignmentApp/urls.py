from django.urls import path
from . import views

app_name = "gaa"
urlpatterns = [
    path("user/<int:person_id>/", views.person_view, name="user"),
    path("participant/<int:participant_id>/preferences/", views.participant_preference_form, name="preferences"),
    path(
        "<int:supervisor_id>/register_participant/", views.person_details_form, name="person_details"
    ),
    path(
        "<int:supervisor_id>/register_participant/thanks/",
        views.participant_registration_success,
        name="thanks",
    ),
    path(
        "<int:participant_id>/preferences/thanks",
        views.participant_registration_success,
        name="thanks",
    ),

]
