from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from asgiref.sync import sync_to_async

from asset.models import Server


class AsyncUser:
    """Wrapper for user data in async templates."""
    def __init__(self, is_authenticated, username):
        self.is_authenticated = is_authenticated
        self.username = username


async def get_user_context(request):
    """Helper to get user context for templates in async views."""
    user_data = await sync_to_async(lambda: (
        request.user.is_authenticated,
        getattr(request.user, 'username', '')
    ))()
    return {'user': AsyncUser(user_data[0], user_data[1])}


async def index(request):
    is_authenticated = await sync_to_async(lambda: request.user.is_authenticated)()
    if not is_authenticated:
        return render(request, "asset/login.html")

    context = await get_user_context(request)
    return render(request, "asset/index.html", context)

@login_required
async def overview_servers(request):
    servers = [server async for server in Server.objects.all()]
    context = await get_user_context(request)
    context['servers'] = servers
    return render(request, "asset/overview_servers.html", context)


# Authentication Views
async def login_view(request):
    is_authenticated = await sync_to_async(lambda: request.user.is_authenticated)()
    if is_authenticated:
        return redirect('server_list')

    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = await sync_to_async(authenticate)(request, username=username, password=password)

        if user is not None:
            await sync_to_async(auth_login)(request, user)
            next_url = request.GET.get('next', 'server_list')
            return redirect(next_url)
        else:
            messages.error(request, "Invalid username or password.")

    return render(request, "asset/login.html")


async def logout_view(request):
    await sync_to_async(auth_logout)(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect('login')

@login_required
# CRUD Views for Server
async def server_list(request):
    servers = [server async for server in Server.objects.all().order_by('-created_at')]
    context = await get_user_context(request)
    context['servers'] = servers
    return render(request, "asset/server_list.html", context)


async def server_detail(request, pk):
    server = await sync_to_async(get_object_or_404)(Server, pk=pk)
    context = await get_user_context(request)
    context['server'] = server
    return render(request, "asset/server_detail.html", context)


@login_required
async def server_create(request):
    context = await get_user_context(request)

    if request.method == "POST":
        # Basic required fields
        asset_tag = request.POST.get('asset_tag')
        name = request.POST.get('name')
        server_type = request.POST.get('server_type')
        operating_system = request.POST.get('operating_system')
        server_role = request.POST.get('server_role')

        if not all([asset_tag, name, server_type, operating_system, server_role]):
            messages.error(request, "Please fill in all required fields.")
            context['server'] = None
            return render(request, "asset/server_form.html", context)

        # Create server with all available fields from POST
        server = await Server.objects.acreate(
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

    context['server'] = None
    return render(request, "asset/server_form.html", context)


@login_required
async def server_update(request, pk):
    server = await sync_to_async(get_object_or_404)(Server, pk=pk)
    context = await get_user_context(request)

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

        await sync_to_async(server.save)()
        messages.success(request, f"Server '{server.name}' updated successfully.")
        return redirect('server_detail', pk=server.pk)

    context['server'] = server
    return render(request, "asset/server_form.html", context)


@login_required
async def server_delete(request, pk):
    server = await sync_to_async(get_object_or_404)(Server, pk=pk)
    context = await get_user_context(request)

    if request.method == "POST":
        server_name = server.name
        await sync_to_async(server.delete)()
        messages.success(request, f"Server '{server_name}' deleted successfully.")
        return redirect('server_list')

    context['server'] = server
    return render(request, "asset/server_confirm_delete.html", context)
