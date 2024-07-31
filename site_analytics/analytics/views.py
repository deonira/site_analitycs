from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as auth_logout
from .models import VisitedPage
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
def set_cookie(request, response):
    visit_count = int(request.COOKIES.get('visit_count', 0)) + 1
    response.set_cookie('visit_count', str(visit_count))
    return response

@login_required
def index(request):
    users = User.objects.all()
    paginator = Paginator(users, 2)  # показывать 2 объекта на странице
    page = request.GET.get('page')
    products = paginator.get_page(page)
    response = render(request, 'index.html', context={'users': products, 'title': 'Мой сайт'})
    response = set_cookie(request, response)
    return response

@login_required
def logout_view(request):
    if request.user.is_authenticated:
        visited_pages = []
        visit_count = request.COOKIES.get('visit_count')
        if visit_count:
            visited_pages = [f'Page {i+1}' for i in range(int(visit_count))]
        for page in visited_pages:
            VisitedPage.objects.create(user=request.user, page_name=page)
        response = redirect('login')
        response.delete_cookie('visit_count')
        auth_logout(request)
        return response
    else:
        return redirect('login')

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('index')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

@login_required
def logout_view(request):
    if request.user.is_authenticated:
        visited_pages = []
        visit_count = request.COOKIES.get('visit_count')
        if visit_count:
            visited_pages = [f'Page {i+1}' for i in range(int(visit_count))]
        for page in visited_pages:
            VisitedPage.objects.create(user=request.user, page_name=page)
        response = redirect('login')
        response.delete_cookie('visit_count')
        auth_logout(request)
        return response
    else:
        return redirect('login')