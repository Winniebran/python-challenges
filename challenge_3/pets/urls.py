from django.urls import path
from .views import PetView, PetIdView

urlpatterns = [
    path("pets/", PetView.as_view()),
    path("pets/<int:pet_id>/", PetIdView.as_view()),
]
