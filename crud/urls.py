
from django.urls import path
from . import views

# urls do crud/
# as rotas continuam em views.py
urlpatterns = [
    path('', view=views.homepage),
    path('update/', view=views.update),
    path('save/', view=views.save)
]
