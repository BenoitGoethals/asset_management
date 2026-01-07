from django.http import HttpResponse
from django.shortcuts import render

def index(request):
    return HttpResponse("Hello, world. You're at the asset index.")

def overview_servers(request):
    return render(request, "asset/overview_servers.html")
