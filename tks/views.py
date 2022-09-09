from django.shortcuts import render
from django.views.decorators.cache import cache_control

# Create your views here.
def index(request):
    return render(request, 'index.html')