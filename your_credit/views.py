from django.http import HttpResponse


def index(request):
    return HttpResponse("<h1>¡Hola! Django está corriendo correctamente.</h1>")
