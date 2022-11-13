from django.urls import path
from . import views
urlpatterns = [
        path("user/<int:person_id>/",views.person_view)
]
