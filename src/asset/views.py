from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required

from asset.models import Server


def index(request):
    if not request.user.is_authenticated:
        return render(request, "asset/login.html")
    return render(request, "asset/index.html")

@login_required
def overview_servers(request):
    servers = Server.objects.all()
    return render(request, "asset/overview_servers.html", {"servers": servers})


# Authentication Views
def login_view(request):
    if request.user.is_authenticated:
        return redirect('server_list')

    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            auth_login(request, user)
            next_url = request.GET.get('next', 'server_list')
            return redirect(next_url)
        else:
            messages.error(request, "Invalid username or password.")

    return render(request, "asset/login.html")


def logout_view(request):
    auth_logout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect('login')

@login_required
# CRUD Views for Server
def server_list(request):
    servers = Server.objects.all().order_by('-created_at')
    return render(request, "asset/server_list.html", {"servers": servers})


def server_detail(request, pk):
    server = get_object_or_404(Server, pk=pk)
    return render(request, "asset/server_detail.html", {"server": server})


@login_required
def server_create(request):
    if request.method == "POST":
        # Basic required fields
        asset_tag = request.POST.get('asset_tag')
        name = request.POST.get('name')
        server_type = request.POST.get('server_type')
        operating_system = request.POST.get('operating_system')
        server_role = request.POST.get('server_role')

        if not all([asset_tag, name, server_type, operating_system, server_role]):
            messages.error(request, "Please fill in all required fields.")
            return render(request, "asset/server_form.html", {"server": None})

        # Create server with all available fields from POST
        server = Server.objects.create(
            asset_tag=asset_tag,
            name=name,
            server_type=server_type,
            operating_system=operating_system,
            server_role=server_role,
            description=request.POST.get('description', ''),
            hostname=request.POST.get('hostname', ''),
            primary_ip_address=request.POST.get('primary_ip_address') or None,
            status=request.POST.get('status', 'ACTIVE'),
            environment=request.POST.get('environment', 'PROD'),
        )
        messages.success(request, f"Server '{server.name}' created successfully.")
        return redirect('server_detail', pk=server.pk)

    return render(request, "asset/server_form.html", {"server": None})


@login_required
def server_update(request, pk):
    server = get_object_or_404(Server, pk=pk)

    if request.method == "POST":
        # Update basic required fields
        server.asset_tag = request.POST.get('asset_tag', server.asset_tag)
        server.name = request.POST.get('name', server.name)
        server.server_type = request.POST.get('server_type', server.server_type)
        server.operating_system = request.POST.get('operating_system', server.operating_system)
        server.server_role = request.POST.get('server_role', server.server_role)
        server.description = request.POST.get('description', '')
        server.hostname = request.POST.get('hostname', '')
        server.status = request.POST.get('status', server.status)
        server.environment = request.POST.get('environment', server.environment)

        # Handle IP address (can be empty)
        ip_address = request.POST.get('primary_ip_address')
        server.primary_ip_address = ip_address if ip_address else None

        server.save()
        messages.success(request, f"Server '{server.name}' updated successfully.")
        return redirect('server_detail', pk=server.pk)

    return render(request, "asset/server_form.html", {"server": server})


@login_required
def server_delete(request, pk):
    server = get_object_or_404(Server, pk=pk)

    if request.method == "POST":
        server_name = server.name
        server.delete()
        messages.success(request, f"Server '{server_name}' deleted successfully.")
        return redirect('server_list')

    return render(request, "asset/server_confirm_delete.html", {"server": server})
