from django.urls import path
from . import views

urlpatterns = [
    path('', view=views.authPage),
    path('homepage/', view=views.homepage),
    path('createUser/', view=views.createUser),
    path('authUser/', view=views.authUser),
    path('saveCalendar/', view=views.saveCalendar),
    path('getCalendar/', view=views.getCalendar),
    path('optimize/', view=views.optimizeCalendar),
    path('deleteCalendar/', view=views.deleteCalendar),
]
