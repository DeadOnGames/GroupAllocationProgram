from django.urls import path
from . import views

app_name = "gaa"
urlpatterns = [
    path("user/<int:person_id>/", views.person_view, name="user"),
    path("register_supervisor/", views.register_supervisor, name="register_supervisor"),
    path("participant/<int:participant_id>/preferences/", views.participant_preference_form, name="preferences"),
    path(
        "supervisor/<int:supervisor_id>/register_participant/", views.person_details_form, name="person_details"
    ),
    path(
        "supervisor/<int:supervisor_id>/register_participant/thanks/",
        views.participant_registration_success,
        name="thanks",
    ),
    path(
        "supervisor/<int:supervisor_id>/assign_groups/",
        views.assign_groups,
        name="assign_groups",
    ),
    path(
        "<int:participant_id>/preferences/thanks",
        views.participant_registration_success,
        name="thanks",
    ),
    path(
        "group/<int:group_id>/",
        views.group_view,
        name="group"
        ),

]
