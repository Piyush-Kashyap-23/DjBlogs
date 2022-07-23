from django.http import HttpResponse

def aboutPage(request):
    return HttpResponse("<h1>About page</h1>")