
from django.urls import path
from . import views

urlpatterns = [
    path('', view=views.homepage),
    path('update/', view=views.update),
    path('save/', view=views.save)
]
