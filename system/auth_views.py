from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST
import requests as api_request
from .api_constants import APIConstants
from .decorators import user_not_authenticated
from django.contrib import messages


@user_not_authenticated
def login_page(request):
    return render(request, 'system/auth/login.html')


@require_POST
def process_login(request):
    email = request.POST.get('email')
    password = request.POST.get('password')
    data = {
        'email': email,
        'password': password
    }
    response = api_request.post(APIConstants.LOGIN_URL, data=data)
    results = response.json()
    print(results)
    if response.status_code == 200:
        request.session['email'] = results['email']
        request.session['fullname'] = f"{results['first_name']} {results['last_name']}"
        return redirect("system:dashboard")
    else:
        messages.error(request, results['detail'])
        return redirect('system:login_page')


def sign_out(request):
    del request.session['email']
    return redirect('system:login_page')