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
    ctx = {
        'odometers': response.json(),
        'equipments': equip_response.json()
    }
    return render(request, "system/odometers/all-odometers.html", ctx)


@user_verified
@user_authenticated
def view_odometer(request, pk):
    headers = {
        'Authorization': f'Token {request.session.get("token")}',
        'Content-Type': 'application/json'
    }
    response = api_request.get(f"{APIConstants.ALL_ODOMETERS}{pk}/", headers=headers)
    equip_response = api_request.get(APIConstants.EQUIPMENTS_URL, headers=headers)
    single_equip = api_request.get(f"{APIConstants.EQUIPMENTS_URL}{response.json()['equipment']}", headers=headers)
    ctx = {
        'odometer': response.json(),
        'equipments': equip_response.json(),
        "selected_equipment": single_equip.json()
    }
    return render(request, "system/odometers/view-odometer.html", ctx)


# @user_verified
# @user_authenticated
# def edit_odometer(request, pk):
#     headers = {
#         'Authorization': f'Token {request.session.get("token")}',
#         'Content-Type': 'application/json'
#     }
#     response = api_request.get(f"{APIConstants.ALL_ODOMETERS}/{pk}/", headers=headers)
#     ctx = {
#         'odometer': response.json(),
#     }
#     return render(request, "system/odometers/edit-odometer.html", ctx)


@require_POST
@user_verified
@user_authenticated
def update_odometer(request, pk):
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

    response = api_request.patch(f"{APIConstants.ALL_ODOMETERS}{pk}/", data=json.dumps(data), headers=header)
    if response.ok:
        messages.info(request, "Odometer updated successfully")
    else:
        messages.error(request, "Error occurred")
    return redirect("system:all_odometers")


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
    from_eq = request.POST.get("from_equipment")
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
    if from_eq is not None:
        return redirect('system:view_equipment', equipment)
    return redirect("system:all_odometers")


@user_verified
@user_authenticated
def all_users(request):
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
    return redirect("system:all_users")


@user_verified
@user_authenticated
def all_technicians(request):
    header = {
        'Authorization': f'Token {request.session.get("token")}',
        'Content-Type': 'application/json'
    }
    response = api_request.get(APIConstants.ALL_USERS_URL, headers=header)
    users = response.json()
    technicians = [user for user in users if user['role'] == "TECHNICIAN"]
    ctx = {
        'technicians': technicians
    }
    return render(request, "system/users/technicians.html", ctx)


@user_verified
@user_authenticated
def view_technician(request, pk):
    header = {
        'Authorization': f'Token {request.session.get("token")}',
        'Content-Type': 'application/json'
    }
    response = api_request.get(f"{APIConstants.API_BASE_URL}/users/{pk}", headers=header)
    ctx = {
        'technician': response.json()
    }
    return render(request, "system/users/view-technicians.html", ctx)


@user_verified
@user_authenticated
def edit_technician(request, pk):
    header = {
        'Authorization': f'Token {request.session.get("token")}',
        'Content-Type': 'application/json'
    }
    response = api_request.get(f"{APIConstants.API_BASE_URL}/users/{pk}", headers=header)
    ctx = {
        'technician': response.json()
    }
    return render(request, "system/users/edit-technician.html", ctx)


@user_verified
@user_authenticated
def view_user(request, pk):
    header = {
        'Authorization': f'Token {request.session.get("token")}',
        'Content-Type': 'application/json'
    }
    response = api_request.get(f"{APIConstants.API_BASE_URL}/users/{pk}/", headers=header)
    ctx = {
        'user': response.json()
    }
    return render(request, "system/users/view-user.html", ctx)


@user_verified
@user_authenticated
def edit_user(request, pk):
    header = {
        'Authorization': f'Token {request.session.get("token")}',
        'Content-Type': 'application/json'
    }
    response = api_request.get(f"{APIConstants.API_BASE_URL}/users/{pk}/", headers=header)
    ctx = {
        'user': response.json()
    }
    return render(request, "system/users/edit-user.html", ctx)



@require_POST
@user_verified
@user_authenticated
def save_technician(request):
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
    return redirect("system:all_technicians")


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


@user_verified
@user_authenticated
def view_service_type(request, pk):
    header = {
        'Authorization': f'Token {request.session.get("token")}',
        'Content-Type': 'application/json'
    }
    response = api_request.get(f"{APIConstants.API_BASE_URL}/service-types/{pk}/", headers=header)
    service_type = response.json()
    ctx = {
        'service_type': service_type
    }
    return render(request, "system/service-type/view-service-type.html", ctx)


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


@require_POST
@user_verified
@user_authenticated
def update_service_type(request, pk):
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
    response = api_request.patch(f"{APIConstants.CREATE_SERVICE_TYPES}{pk}/", headers=header, data=json.dumps(data))
    result = response.json()
    if result["name"] is not None:
        messages.info(request, "Service Type updated Successfully")
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


@user_verified
@user_authenticated
def view_purchaser(request, pk):
    header = {
        'Authorization': f'Token {request.session.get("token")}',
        'Content-Type': 'application/json'
    }
    response = api_request.get(f"{APIConstants.API_BASE_URL}/purchaser/{pk}/", headers=header)
    purchaser = response.json()
    ctx = {
        'purchaser': purchaser
    }
    return render(request, "system/purchasers/view-purchaser.html", ctx)


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
    if result["name"] is not None:
        messages.success(request, "Purchaser added Successfully")
    return redirect("system:all_purchasers")


@require_POST
@user_verified
@user_authenticated
def update_purchaser(request, pk):
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
    response = api_request.patch(f"{APIConstants.ALL_PURCHASERS_URL}{pk}/", headers=header, data=json.dumps(data))
    result = response.json()
    if result["name"] is not None:
        messages.info(request, "Purchaser updated Successfully")
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
    ctx = {
        'referrers': response.json()
    }
    return render(request, "system/referrers/referrers.html", ctx)


@user_verified
@user_authenticated
def view_referrer(request, pk):
    header = {
        'Authorization': f'Token {request.session.get("token")}',
        'Content-Type': 'application/json'
    }
    response = api_request.get(f"{APIConstants.API_BASE_URL}/referrer/{pk}/", headers=header)
    ctx = {
        'referrer': response.json()
    }
    return render(request, "system/referrers/view-referrer.html", ctx)


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
    if result["name"] is not None:
        messages.success(request, "Referrer added Successfully")
    return redirect("system:all_referrers")



@require_POST
@user_verified
@user_authenticated
def update_referrer(request, pk):
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
    response = api_request.patch(f"{APIConstants.CREATE_REFERRERS_URL}{pk}/", headers=header, data=json.dumps(data))
    result = response.json()
    if result["name"] is not None:
        messages.info(request, "Referrer added Successfully")
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



@user_verified
@user_authenticated
def view_equipment(request, pk):
    header = {
        'Authorization': f'Token {request.session.get("token")}',
        'Content-Type': 'application/json',
    }
    response = api_request.get(f"{APIConstants.EQUIPMENTS_URL}{pk}/", headers=header)

    ctx = {
        'equipment': response.json()
    }
    return render(request, "system/equipments/view-equipment.html", ctx)


@user_verified
@user_authenticated
def edit_equipment(request, pk):
    header = {
        'Authorization': f'Token {request.session.get("token")}',
        'Content-Type': 'application/json',
    }
    response = api_request.get(f"{APIConstants.EQUIPMENTS_URL}{pk}/", headers=header)
    user_response = api_request.get(APIConstants.ALL_USERS_URL, headers=header)
    technicians = [user for user in user_response.json() if user['role'] == "TECHNICIAN"]
    ctx = {
        'equipment': response.json(),
        'technicians': technicians,
    }
    return render(request, "system/equipments/edit-equipment.html", ctx)


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
    if result["name"] is not None:
        messages.success(request, "Equipment added Successfully")
    return redirect("system:all_equipments")


@require_POST
@user_verified
@user_authenticated
def update_equipment(request, pk):
    header = {
        'Authorization': f'Token {request.session.get("token")}',
        'Content-Type': 'application/json',
    }
    name = request.POST.get("name")
    model = request.POST.get("model")
    engine_number = request.POST.get("engine_number")
    year = request.POST.get("year")
    image_url = request.FILES.get("image_url")
    old_image = request.POST.get("old_image")
    from_eq = request.POST.get("from_equipment")
    uploaded_image = None
    if image_url is not None:
        uploaded_image = cloudinary.uploader.upload(file=image_url)

    data = {
        "name": name,
        "model": model,
        "engine_number": engine_number,
        "year": year,
        "image_url": uploaded_image['url'] if uploaded_image is not None else old_image,
        "technicians_id": []
    }

    response = api_request.patch(
        f"{APIConstants.EQUIPMENTS_URL}{pk}/", headers=header, data=json.dumps(data))
    result = response.json()
    if result["name"] is not None:
        messages.info(request, "Equipment updated Successfully")
    if from_eq is not None:
        return redirect('system:view_equipment', pk)
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
    equipments_response = api_request.get(APIConstants.EQUIPMENTS_URL, headers=header)
    sales = response.json()
    ctx = {
        'sales': sales,
        "referrers": referrer_response.json(),
        "purchasers": purchaser_response.json(),
        "equipments": equipments_response.json()
    }
    return render(request, "system/sales/all-sales.html", ctx)


@user_verified
@user_authenticated
def view_sale(request, pk):
    header = {
        'Authorization': f'Token {request.session.get("token")}',
        'Content-Type': 'application/json'
    }
    response = api_request.get(f"{APIConstants.API_BASE_URL}/sales/{pk}/", headers=header)
    referrer_response = api_request.get(APIConstants.ALL_REFERRERS_URL, headers=header)
    purchaser_response = api_request.get(APIConstants.ALL_PURCHASERS_URL, headers=header)
    equipments_response = api_request.get(APIConstants.EQUIPMENTS_URL, headers=header)
    sale = response.json()
    ctx = {
        'sale': sale,
        "referrers": referrer_response.json(),
        "purchasers": purchaser_response.json(),
        "equipments": equipments_response.json()
    }
    return render(request, "system/sales/view-sale.html", ctx)


@require_POST
@user_verified
@user_authenticated
def update_sale(request, pk):
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
    response = api_request.patch(f"{APIConstants.CREATE_SALES_URL}{pk}/", headers=header, data=json.dumps(data))
    if response.ok:
        messages.info(request, "Sales updated Successfully")
    return redirect("system:all_sales")


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
    if response.ok:
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
    ctx = {
        'inspections': response.json(),
        "equipments": equipments_response.json(),
        "odometers": odometer_response.json(),
        "users": users_response.json()
    }
    return render(request, "system/inspections/all-inspections.html", ctx)


@user_verified
@user_authenticated
def view_inspection(request, pk):
    header = {
        'Authorization': f'Token {request.session.get("token")}',
        'Content-Type': 'application/json'
    }
    response = api_request.get(f"{APIConstants.ALL_INSPECTIONS_URL}{pk}/", headers=header)
    equipments_response = api_request.get(APIConstants.EQUIPMENTS_URL, headers=header)
    odometer_response = api_request.get(APIConstants.ALL_ODOMETERS, headers=header)
    users_response = api_request.get(APIConstants.ALL_USERS_URL, headers=header)
    ctx = {
        'inspection': response.json(),
        "equipments": equipments_response.json(),
        "odometers": odometer_response.json(),
        "users": users_response.json()
    }
    return render(request, "system/inspections/view-inspection.html", ctx)


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
    user_response = api_request.get(APIConstants.ALL_USERS_URL, headers=header)
    users = user_response.json()
    technicians = [user for user in users if user['role'] == "TECHNICIAN"]
    ctx = {
        'services': response.json(),
        "equipments": equipments_response.json(),
        "odometers": odometer_response.json(),
        "service_types": service_type_response.json(),
        'technicians': technicians
    }
    return render(request, "system/services/all-services.html", ctx)


@user_verified
@user_authenticated
def view_service(request, pk):
    header = {
        'Authorization': f'Token {request.session.get("token")}',
        'Content-Type': 'application/json'
    }
    response = api_request.get(f"{APIConstants.ALL_SERVICES_URL}{pk}/", headers=header)
    equipments_response = api_request.get(APIConstants.EQUIPMENTS_URL, headers=header)
    odometer_response = api_request.get(APIConstants.ALL_ODOMETERS, headers=header)
    service_type_response = api_request.get(APIConstants.ALL_SERVICE_TYPES, headers=header)
    user_response = api_request.get(APIConstants.ALL_USERS_URL, headers=header)
    users = user_response.json()
    technicians = [user for user in users if user['role'] == "TECHNICIAN"]
    ctx = {
        'service': response.json(),
        "equipments": equipments_response.json(),
        "odometers": odometer_response.json(),
        "service_types": service_type_response.json(),
        "technicians": technicians
    }
    return render(request, "system/services/view-service.html", ctx)


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
    response = api_request.post(APIConstants.CREATE_SERVICES_URL, headers=header, data=json.dumps(data))
    result = response.json()
    if response.ok:
        messages.success(request, "Sales added Successfully")
    return redirect("system:all_services")


@require_POST
@user_verified
@user_authenticated
def update_service(request, pk):
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
    response = api_request.patch(f"{APIConstants.ALL_SERVICES_URL}{pk}/", headers=header, data=json.dumps(data))
    if response.ok:
        messages.info(request, "Service updated Successfully")
    return redirect("system:all_services")
