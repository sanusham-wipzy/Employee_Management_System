
from django.urls import path
from .import views

urlpatterns = [
    path('', views.employee_list,name='employee_list'),
    path('add/',views.add_employee,name='add_employee'),
    path('<int:id>/edit/', views.update_employee, name='update_employee'),
    path('<int:id>/view/', views.employee_details, name='employee_details'),
    path('<int:id>/delete/', views.delete_employee, name='delete_employee'),
    
    path('add_designation/', views.add_designation, name='add_designation'),
    path('<int:id>/edit_designation/', views.edit_designation, name='edit_designation'),
    path('<int:id>/delete_designation/', views.delete_designation, name='delete_designation'),

    path('employee/login/', views.employee_login, name='employee_login'),
    path('employee/dashboard/', views.employee_dashboard, name='employee_dashboard'),
    path('employee/edit_profile', views.edit_profile, name='edit_profile'),
    path('employee/change_password', views.change_password, name='change_password'),
]
