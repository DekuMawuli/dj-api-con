import json

from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST
import requests as api_request
from .api_constants import APIConstants
from .decorators import user_authenticated, user_verified
from django.contrib import messages
from django.utils import timezone
import cloudinary.uploader
import cloudinary

cloudinary.config(
  cloud_name="drntdazzu",
  api_key="711572588646129",
  api_secret="JQ9mk1ykB-O4lNVomoTLwGE2yKs"
)

@user_verified
@user_authenticated
def dashboard(request):
    return render(request, 'system/dashboard.html')


@user_verified
@user_authenticated
def all_odometers(request):
    headers = {
        'Authorization': f'Token {request.session.get("token")}',
        'Content-Type': 'application/json'
    }
    response = api_request.get(APIConstants.ALL_ODOMETERS, headers=headers)
    equip_response = api_request.get(APIConstants.EQUIPMENTS_URL, headers=headers)
    print(equip_response.json())
    print(response.json())
    print(request.session.get("token"))
    ctx = {
        'odometers': response.json(),
        'equipments': equip_response.json()
    }
    return render(request, "system/odometers/all-odometers.html", ctx)


@require_POST
@user_verified
@user_authenticated
def save_odometer(request):
    header = {
        'Authorization': f'Token {request.session.get("token")}',
        'Content-Type': 'application/json'
    }
    name = request.POST.get("name")
    value = request.POST.get("value")
    equipment = request.POST.get("equipment")
    data = {
        "name": name,
        "value": value,
        "equipment": equipment,
    }

    response = api_request.post(APIConstants.CREATE_ODOMETERS, data=json.dumps(data), headers=header)
    if response.ok:
        messages.success(request, "New Odometer added successfully")
    else:
        messages.error(request, "Error occurred")
    return redirect("system:all_odometers")



@user_verified
@user_authenticated
def all_users(request):
    print(request.session.get('token'))
    header = {
        'Authorization': f'Token {request.session.get("token")}',
        'Content-Type': 'application/json'
    }
    response = api_request.get(APIConstants.ALL_USERS_URL, headers=header)
    users = response.json()
    ctx = {
        'users': users
    }
    return render(request, "system/users/users.html", ctx)


@require_POST
@user_verified
@user_authenticated
def save_user(request):
    header = {
        'Authorization': f'Token {request.session.get("token")}',
        'Content-Type': 'application/json'
    }
    first_name = request.POST.get("first_name")
    last_name = request.POST.get("last_name")
    email = request.POST.get("email")
    phone_number = request.POST.get("phone_number")
    role = request.POST.get("role")
    data = {
        "first_name": first_name, "last_name": last_name,
        "email": email, "phone_number": phone_number,
        "role": role,
        # "created": timezone.now(),"technician_equipment": []
    }
    response = api_request.post(APIConstants.CREATE_USER_URL, data=json.dumps(data), headers=header)
    print(response.json(), "new user")
    return redirect("system:all_users")


@user_verified
@user_authenticated
def all_service_types(request):
    header = {
        'Authorization': f'Token {request.session.get("token")}',
        'Content-Type': 'application/json'
    }
    response = api_request.get(APIConstants.ALL_SERVICE_TYPES, headers=header)
    service_types = response.json()
    ctx = {
        'service_types': service_types
    }
    return render(request, "system/service-type/service-types.html", ctx)


@require_POST
@user_verified
@user_authenticated
def save_service_type(request):
    header = {
        'Authorization': f'Token {request.session.get("token")}',
        'Content-Type': 'application/json'
    }
    name = request.POST.get("name")
    odometer_value = request.POST.get("odometer_value")
    notes = request.POST.get("notes")
    data = {
        "name": name,
        "odometer_value": odometer_value,
        "notes": notes,
    }
    response = api_request.post(APIConstants.CREATE_SERVICE_TYPES, headers=header, data=json.dumps(data))
    result = response.json()
    if result["name"] is not None:
        messages.success(request, "Service Type added Successfully")
    return redirect("system:all_service_types")


@user_verified
@user_authenticated
def all_purchasers(request):
    header = {
        'Authorization': f'Token {request.session.get("token")}',
        'Content-Type': 'application/json'
    }
    response = api_request.get(APIConstants.ALL_PURCHASERS_URL, headers=header)
    purchasers = response.json()
    ctx = {
        'purchasers': purchasers
    }
    return render(request, "system/purchasers/purchasers.html", ctx)



# Purchasers
@require_POST
@user_verified
@user_authenticated
def save_purchaser(request):
    header = {
        'Authorization': f'Token {request.session.get("token")}',
        'Content-Type': 'application/json'
    }
    name = request.POST.get("name")
    phone_number = request.POST.get("phone_number")
    email = request.POST.get("email")
    digital_address = request.POST.get("digital_address")
    residential_address = request.POST.get("residential_address")
    data = {
        "name": name,
        "phone_number": phone_number,
        "email": email,
        "digital_address": digital_address,
        "residential_address": residential_address,
    }
    response = api_request.post(APIConstants.CREATE_PURCHASER_URL, headers=header, data=json.dumps(data))
    result = response.json()
    print(result)
    if result["name"] is not None:
        messages.success(request, "Purchaser added Successfully")
    return redirect("system:all_purchasers")


@user_verified
@user_authenticated
def purchaser_sales(request, pk):
    header = {
        'Authorization': f'Token {request.session.get("token")}',
        'Content-Type': 'application/json'
    }
    response = api_request.get(
        f"{APIConstants.API_BASE_URL}/purchaser/{pk}/sales/",
        headers=header
    )
    print(response.text)
    ctx = {
        'sales': response.json()
    }
    return render(request, 'system/purchasers/purchaser_sales.html', ctx)



@user_verified
@user_authenticated
def all_referrers(request):
    header = {
        'Authorization': f'Token {request.session.get("token")}',
        'Content-Type': 'application/json'
    }
    response = api_request.get(APIConstants.ALL_REFERRERS_URL, headers=header)
    print(response.json())
    ctx = {
        'referrers': response.json()
    }
    return render(request, "system/referrers/referrers.html", ctx)


# Referrers
@require_POST
@user_verified
@user_authenticated
def save_referrer(request):
    header = {
        'Authorization': f'Token {request.session.get("token")}',
        'Content-Type': 'application/json'
    }
    email = request.POST.get("email")
    name = request.POST.get("name")
    phone_number = request.POST.get("phone_number")
    digital_address = request.POST.get("digital_address")
    residential_address = request.POST.get("residential_address")
    data = {
        "name": name,
        "phone_number": phone_number,
        "email": email,
        "digital_address": digital_address,
        "residential_address": residential_address,
    }
    response = api_request.post(APIConstants.CREATE_REFERRERS_URL, headers=header, data=json.dumps(data))
    result = response.json()
    print(result)
    if result["name"] is not None:
        messages.success(request, "Referrer added Successfully")
    return redirect("system:all_referrers")


@user_verified
@user_authenticated
def referrer_sales(request, pk):
    header = {
        'Authorization': f'Token {request.session.get("token")}',
        'Content-Type': 'application/json'
    }

    response = api_request.get(
        f"{APIConstants.API_BASE_URL}/referrer/{pk}/sales/",
        headers=header
    )
    print(response.json())
    ctx = {
        'sales': response.json()
    }
    return render(request, 'system/referrers/referrer_sales.html', ctx)


# Equipments
@user_verified
@user_authenticated
def all_equipments(request):
    header = {
        'Authorization': f'Token {request.session.get("token")}',
        'Content-Type': 'application/json'
    }
    response = api_request.get(APIConstants.EQUIPMENTS_URL, headers=header)
    equipments = response.json()
    ctx = {
        'equipments': equipments
    }
    return render(request, "system/equipments/all-equipments.html", ctx)


@require_POST
@user_verified
@user_authenticated
def save_equipment(request):
    header = {
        'Authorization': f'Token {request.session.get("token")}',
        'Content-Type': 'application/json',
    }
    name = request.POST.get("name")
    model = request.POST.get("model")
    engine_number = request.POST.get("engine_number")
    year = request.POST.get("year")
    image_url = request.FILES.get("image_url")
    uploaded_image = cloudinary.uploader.upload(file=image_url)

    data = {
        "name": name,
        "model": model,
        "engine_number": engine_number,
        "year": year,
        "image_url": uploaded_image['url']
    }
    response = api_request.post(
        APIConstants.CREATE_EQUIPMENTS_URL, headers=header, data=json.dumps(data))
    result = response.json()
    print(result)
    if result["name"] is not None:
        messages.success(request, "Equipment added Successfully")
    return redirect("system:all_equipments")


# Sales
@user_verified
@user_authenticated
def all_sales(request):
    header = {
        'Authorization': f'Token {request.session.get("token")}',
        'Content-Type': 'application/json'
    }
    response = api_request.get(APIConstants.ALL_SALES_URL, headers=header)
    referrer_response = api_request.get(APIConstants.ALL_REFERRERS_URL, headers=header)
    purchaser_response = api_request.get(APIConstants.ALL_PURCHASERS_URL, headers=header)
    sales = response.json()
    ctx = {
        'sales': sales,
        "referrers": referrer_response.json(),
        "purchasers": purchaser_response.json()
    }
    return render(request, "system/sales/all-sales.html", ctx)


@require_POST
@user_verified
@user_authenticated
def save_sale(request):
    header = {
        'Authorization': f'Token {request.session.get("token")}',
        'Content-Type': 'application/json'
    }
    name = request.POST.get("name")
    amount = request.POST.get("amount")
    duration = request.POST.get("duration")
    plan_type = request.POST.get("plan_type")
    purchaser_pk = request.POST.get("purchaser_pk")
    equipment_pk = request.POST.get("equipment_pk")
    referrer_pk = request.POST.get("referrer_pk")
    data = {
        "name": name,
        "amount": amount,
        "duration": duration,
        "plan_type": plan_type,
        "purchaser_pk": purchaser_pk,
        "equipment_pk": equipment_pk,
        "referrer_pk": referrer_pk,
    }
    response = api_request.post(APIConstants.CREATE_SALES_URL, headers=header, data=json.dumps(data))
    result = response.json()
    print(result)
    if result["name"] is not None:
        messages.success(request, "Sales added Successfully")
    return redirect("system:all_sales")


@user_verified
@user_authenticated
def all_inspections(request):
    header = {
        'Authorization': f'Token {request.session.get("token")}',
        'Content-Type': 'application/json'
    }
    response = api_request.get(APIConstants.ALL_INSPECTIONS_URL, headers=header)
    equipments_response = api_request.get(APIConstants.EQUIPMENTS_URL, headers=header)
    odometer_response = api_request.get(APIConstants.ALL_ODOMETERS, headers=header)
    users_response = api_request.get(APIConstants.ALL_USERS_URL, headers=header)
    print(response.json())
    ctx = {
        'inspections': response.json(),
        "equipments": equipments_response.json(),
        "odometers": odometer_response.json(),
        "users": users_response.json()
    }
    return render(request, "system/inspections/all-inspections.html", ctx)


@require_POST
@user_verified
@user_authenticated
def save_inspection(request):
    header = {
        'Authorization': f'Token {request.session.get("token")}',
        'Content-Type': 'application/json'
    }
    if request.FILES.getlist('inspection_pics'):
        inspection_pics = request.FILES.getlist('inspection_pics')
        name = request.POST.get('name')
        current_location = request.POST.get('current_location')
        odometer_value = request.POST.get('odometer_value')
        notes = request.POST.get('notes')
        equipment_pk = request.POST.get('equipment_pk')
        technician_pk = request.POST.get('technician_pk')

        uploaded_images_urls = []
        for pic in inspection_pics:
            print(pic)
            uploaded_image = cloudinary.uploader.upload(file=pic)
            uploaded_images_urls.append(uploaded_image['url'])
        data = {
          "name": name,
          "current_location": current_location,
          "odometer_value": odometer_value,
          "notes": notes,
          "inspection_pics": uploaded_images_urls,
          "equipment_pk": equipment_pk,
          "technician_pk": 0 if technician_pk is None else technician_pk
        }
        response = api_request.post(APIConstants.CREATE_INSPECTIONS_URL, headers=header, data=json.dumps(data))
        result = response.json()
        print(result)
        if result["name"] is not None:
            messages.success(request, "Sales added Successfully")
    return redirect("system:all_inspections")


@user_verified
@user_authenticated
def all_services(request):
    header = {
        'Authorization': f'Token {request.session.get("token")}',
        'Content-Type': 'application/json'
    }
    response = api_request.get(APIConstants.ALL_SERVICES_URL, headers=header)
    equipments_response = api_request.get(APIConstants.EQUIPMENTS_URL, headers=header)
    odometer_response = api_request.get(APIConstants.ALL_ODOMETERS, headers=header)
    service_type_response = api_request.get(APIConstants.ALL_SERVICE_TYPES, headers=header)
    ctx = {
        'services': response.json(),
        "equipments": equipments_response.json(),
        "odometers": odometer_response.json(),
        "service_types": service_type_response.json(),
    }
    return render(request, "system/services/all-services.html", ctx)


@require_POST
@user_verified
@user_authenticated
def save_service(request):
    header = {
        'Authorization': f'Token {request.session.get("token")}',
        'Content-Type': 'application/json'
    }
    odometer_value = request.POST.get('odometer_value')
    notes = request.POST.get('notes')
    service_type_pk = request.POST.get('service_type_pk')
    equipment_pk = request.POST.get('equipment_pk')
    technician_pk = request.POST.get('technician_pk')

    data = {
      "equipment_pk": equipment_pk,
      "odometer_value": odometer_value,
      "notes": notes,
      "service_type_pk": service_type_pk,
      "technician_pk": technician_pk
    }
    response = api_request.post(APIConstants.CREATE_INSPECTIONS_URL, headers=header, data=json.dumps(data))
    result = response.json()
    print(result)
    if result["name"] is not None:
        messages.success(request, "Sales added Successfully")
    return redirect("all-inspections")
