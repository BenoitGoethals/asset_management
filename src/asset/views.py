from django.http import HttpResponse
from django.shortcuts import render

from asset.models import Server


def index(request):
    return render(request, "asset/index.html")

def overview_servers(request):
    servers=Server.objects.all()
    return render(request, "asset/overview_servers.html", {"servers": servers})

    return render(request, "asset/overview_servers.html")
