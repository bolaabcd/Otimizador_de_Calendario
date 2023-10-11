# Import necessary modules and classes

from django.http import HttpRequest, HttpResponse
from .frontend.pages import Pages
from .frontend.authUserController import AuthUserController
from .frontend.createUserController import CreateUserController
from .frontend.saveCalendarController import SaveCalendarController
from .frontend.getCalendarController import GetCalendarController
from .frontend.optimizeCalendarController import OptimizeCalendarController
from .frontend.deleteCalendarController import DeleteCalendarController

from .domain.authUserService import AuthUserService
from .domain.createUserService import CreateUserService
from .domain.deleteCalendarService import DeleteCalendarService
from .domain.getCalendarService import GetCalendarService
from .domain.optimizeCalendarService import OptimizeCalendarService
from .domain.saveCalendarService import SaveCalendarService

from .frontend.JSONrequest import JSONRequest
from .solver.concreteSolver import ConcreteSolver
from .storage.storageConcrete import ConcreteStorage

# Define the homepage view function
def homepage(request: HttpRequest) -> HttpResponse:
    return Pages().getHomePage(request)

# Define the authentication page view function
def authPage(request: HttpRequest) -> HttpResponse:
    return Pages().getAuthPage(request)

# Initialize necessary objects and services
requestsParser = JSONRequest()
storage = ConcreteStorage()
authService = AuthUserService(storage)
solver = ConcreteSolver()

# Define the view function for creating a user
def createUser(request: HttpRequest) -> HttpResponse:
    createUserService = CreateUserService(storage)
    createUserController = CreateUserController(requestsParser, createUserService)
    return createUserController.createUser(request)

# Define the view function for authenticating a user
def authUser(request: HttpRequest) -> HttpResponse:
    authUserService = AuthUserService(storage)
    authUserController = AuthUserController(requestsParser, authUserService)
    return authUserController.authUser(request)

# Define the view function for saving a calendar
def saveCalendar(request: HttpRequest) -> HttpResponse:
    saveCalendarService = SaveCalendarService(storage, authService)
    saveCalendarController = SaveCalendarController(requestsParser, saveCalendarService)
    return saveCalendarController.saveCalendar(request)

# Define the view function for getting a calendar
def getCalendar(request: HttpRequest) -> HttpResponse:
    getCalendarService = GetCalendarService(storage, authService)
    getCalendarController = GetCalendarController(requestsParser, getCalendarService)
    return getCalendarController.getCalendar(request)

# Define the view function for optimizing a calendar
def optimizeCalendar(request: HttpRequest) -> HttpResponse:
    optimizeCalendarService = OptimizeCalendarService(authService, solver)
    optimizeCalendarController = OptimizeCalendarController(requestsParser, optimizeCalendarService)
    return optimizeCalendarController.optimizeCalendar(request)

# Define the view function for deleting a calendar
def deleteCalendar(request: HttpRequest) -> HttpResponse:
    deleteCalendarService = DeleteCalendarService(storage, authService)
    deleteCalendarController = DeleteCalendarController(requestsParser, deleteCalendarService)
    return deleteCalendarController.deleteCalendar(request)
