from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST
import requests as api_request
from .api_constants import APIConstants
from .decorators import user_authenticated
from django.contrib import messages


@user_authenticated
def dashboard(request):
    return render(request, 'system/dashboard.html')


@user_authenticated
def all_odometers(request):
    headers = {
        'Authorization': f'Bearer 6d39a192b49f936f27a4098c3e61b5dc3a804393',
    }
    response = api_request.get(APIConstants.ALL_ODOMETERS_URL, headers=headers)
    print(response.json())
    return render(request, "system/odometers/all-odometers.html")


@user_authenticated
def add_odometer(request):
    return render(request, "system/odometers/all-odometers.html")


@user_authenticated
def all_purchasers(request):
    headers = {
        'Authorization': f'Bearer 6d39a192b49f936f27a4098c3e61b5dc3a804393',
    }
    response = api_request.get(APIConstants.ALL_PURCHASERS_URL, headers=headers)
    print(response.json())
    return render(request, "system/purchasers/purchasers.html")


@user_authenticated
def add_purchaser(request):
    return render(request, "system/purchasers/purchasers.html")


