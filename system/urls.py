from . import views
from . import auth_views
from django.urls import path

app_name = 'system'

urlpatterns = [
    path('dashboard', views.dashboard, name='dashboard'),

    path('odometers', views.all_odometers, name='all_odometers'),
    path('add-odometer', views.save_odometer, name='save_odometer'),
    path('view-odometer/<int:pk>/update', views.update_odometer, name='update_odometer'),
    path('view-odometer/<int:pk>/', views.view_odometer, name='view_odometer'),

    path('purchasers', views.all_purchasers, name='all_purchasers'),
    path('add-purchaser', views.save_purchaser, name='save_purchaser'),
    path('view-purchaser/<int:pk>/update', views.update_purchaser, name='update_purchaser'),
    path('view-purchaser/<int:pk>/', views.view_purchaser, name='view_purchaser'),

    path('referrers', views.all_referrers, name='all_referrers'),
    path('add-referrer', views.save_referrer, name='save_referrer'),
    path('view-referrer/<int:pk>/update', views.update_referrer, name='update_referrer'),
    path('view-referrer/<int:pk>/', views.view_referrer, name='view_referrer'),

    path('users', views.all_users, name='all_users'),
    path('add-user', views.save_user, name='save_user'),
    path('view-user/<int:pk>/', views.view_user, name='view_user'),

    path('technicians', views.all_technicians, name='all_technicians'),
    path('add-technician', views.save_technician, name='save_technician'),
    path('view-technician/<int:pk>/', views.view_technician, name='view_technician'),

    path('service-types', views.all_service_types, name='all_service_types'),
    path('add-service-type', views.save_service_type, name='save_service_type'),
    path('view-service-type/<int:pk>/', views.view_service_type, name='view_service_type'),

    # ============== EQUIPMENTS URLS
    path('equipments', views.all_equipments, name='all_equipments'),
    path('add-equipment', views.save_equipment, name='save_equipment'),
    path('view-equipment/<int:pk>', views.view_equipment, name='view_equipment'),
    path('edit-equipment/<int:pk>', views.edit_equipment, name='edit_equipment'),
    path('edit-equipment/<int:pk>/update', views.update_equipment, name='update_equipment'),
    # ============== END OF EQUIPMENTS URL

    path('service', views.all_services, name='all_services'),
    path('add-service', views.save_service, name='save_service'),
    path('view-service/<int:pk>/update', views.update_service, name='update_service'),
    path('view-service/<int:pk>/', views.view_service, name='view_service'),

    path('inspections', views.all_inspections, name='all_inspections'),
    path('save-inspection', views.save_inspection, name='save_inspection'),
    path('view-inspection/<int:pk>/', views.view_inspection, name='view_inspection'),

    path('sales', views.all_sales, name='all_sales'),
    path('add-sale', views.save_sale, name='save_sale'),
    path('view-sale/<int:pk>/update', views.update_sale, name='update_sale'),
    path('view-sale/<int:pk>/', views.view_sale, name='view_sale'),

    path('purchaser/<int:pk>/sales/', views.purchaser_sales, name='purchaser_sales'),
    path('referrer/<int:pk>/sales/', views.referrer_sales, name='referrer_sales'),

]

urlpatterns += [
    path("", auth_views.login_page, name="login_page"),
    path("process-login", auth_views.process_login, name="process_login"),
    path("change-password", auth_views.change_password, name="change_password"),
    path("update-password", auth_views.update_password, name="update_password"),
    path("sign-out", auth_views.sign_out, name="sign_out"),
]
