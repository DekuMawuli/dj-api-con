import json

from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST
import requests as api_request
from .api_constants import APIConstants
from .decorators import user_not_authenticated, user_authenticated
from django.contrib import messages


@user_not_authenticated
def login_page(request):
    return render(request, 'system/auth/login.html')


@require_POST
def process_login(request):
    header = {

        'Content-Type': 'application/json',
    }
    email = request.POST.get('email')
    password = request.POST.get('password')
    data = {
        'email': email,
        'password': password
    }
    response = api_request.post(APIConstants.LOGIN_URL, data=json.dumps(data), headers=header)
    results = response.json()
    print(results)
    if response.status_code == 200:
        if results['is_verified'] is True:
            request.session['is_verified'] = True
            request.session['token'] = results['auth_token']
            request.session['email'] = results['email']
            request.session['role'] = results['role']
            request.session['fullname'] = f"{results['first_name']} {results['last_name']}"
            return redirect("system:dashboard")
        else:
            request.session['is_verified'] = False
            request.session['email'] = results['email']
            request.session['token'] = 'n/a'
            request.session['fullname'] = f"{results['first_name']} {results['last_name']}"
            return redirect("system:change_password")
    else:
        messages.error(request, results['detail'])
        return redirect('system:login_page')


@user_authenticated
def sign_out(request):
    request.session.clear()
    return redirect('system:login_page')


@user_authenticated
def change_password(request):
    return render(request, 'system/auth/change-password.html')


@user_authenticated
@require_POST
def update_password(request):
    header = {
        # 'Authorization': f'Token {request.session.get("token")}',
        'Content-Type': 'application/json',
    }
    password = request.POST.get('new_password')
    confirm_password = request.POST.get('confirm_password')
    if password != confirm_password:
        messages.error(request, 'Passwords do not match')
        return redirect('system:change_password')
    data = {
        "email": request.session['email'],
        'password': password
    }
    response = api_request.post(APIConstants.RESET_PASSWORD_URL, data=json.dumps(data), headers=header)
    results = response.json()
    if response.status_code == 200:
        messages.success(request, 'Password Changed successfully')
        del request.session['email']
        del request.session['token']
        del request.session['is_verified']
        del request.session['fullname']
        return redirect('system:dashboard')

    return redirect("system:change_password")





# {
#   "email": "gh@gmail.com",
#   "password": "1233445"
# }
