


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
from .solver.solver import ConcreteSolver


def homepage(request: HttpRequest) -> HttpResponse:
    return Pages().getHomePage(request)

def authPage(request: HttpRequest) -> HttpResponse:
    return Pages().getAuthPage(request)


requestsParser = JSONRequest()
storage = None # TODO
authService = AuthUserService(storage)
solver = ConcreteSolver()


def createUser(request: HttpRequest) -> HttpResponse:
    createUserService = CreateUserService(storage)
    createUserController = CreateUserController(requestsParser, createUserService)
    return createUserController.createUser(request)

def authUser(request: HttpRequest) -> HttpResponse:
    authUserService = AuthUserService(storage)
    authUserController = AuthUserController(requestsParser, authUserService)
    return authUserController.authUser(request)

def saveCalendar(request: HttpRequest) -> HttpResponse:
    saveCalendarService = SaveCalendarService(storage, authService)
    saveCalendarController = SaveCalendarController(requestsParser, saveCalendarService)
    return saveCalendarController.saveCalendar(request)

def getCalendar(request: HttpRequest) -> HttpResponse:
    getCalendarService = GetCalendarService(storage, authService)
    getCalendarController = GetCalendarController(requestsParser, getCalendarService)
    return getCalendarController.getCalendar(request)

def optimizeCalendar(request: HttpRequest) -> HttpResponse:
    optimizeCalendarService = OptimizeCalendarService(authService, solver)
    optimizeCalendarController = OptimizeCalendarController(requestsParser, optimizeCalendarService)
    return optimizeCalendarController.optimizeCalendar(request)

def deleteCalendar(request: HttpRequest) -> HttpResponse:
    deleteCalendarService = DeleteCalendarService(storage, authService)
    deleteCalendarController = DeleteCalendarController(requestsParser, deleteCalendarService)
    return deleteCalendarController.deleteCalendar(request)

