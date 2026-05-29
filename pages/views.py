from django.shortcuts import render
from .models import HomePage

def home_view(request):
    home = HomePage.objects.first()
    return render(request, "pages/home.html", {"home": home})
