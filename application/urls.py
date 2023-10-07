from django.urls import path
from . import views

urlpatterns = [
    path('', view=views.authPage),
    path('homepage/', view=views.homepage),
    path('createUser/', view=views.createUser),
    path('authUser/', view=views.authUser),
    path('homepage/saveCalendar/', view=views.saveCalendar),
    path('homepage/getCalendar/', view=views.getCalendar),
    path('homepage/optimizeCalendar/', view=views.optimizeCalendar),
    path('homepage/deleteCalendar/', view=views.deleteCalendar)
]
