from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse
from .models import Employees, Designation
from django.contrib import messages
from django.db.models import Count


# Create your views here.

import random
import string
from django.contrib.auth.hashers import make_password


def random_password():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=8))


def employee_list(request):

    employees = Employees.objects.all()

    designations = Designation.objects.annotate(
        employee_count=Count('employees')
    ).order_by('name')

    total_employees = employees.count()
    total_designations = designations.count()

    most_employees = designations.order_by(
        '-employee_count', 'name'
    ).first()

    least_employee = designations.filter(
        employee_count__gt=0
    ).order_by(
        'employee_count', 'name'
    ).first()


    context = {
        'employees': employees,
        'designations': designations,
        'total_employees': total_employees,
        'total_designations': total_designations,
        'most_employees': most_employees,
        'least_employee': least_employee
    }

    return render(request, 'employee_list.html', context)

def add_designation(request):
    if request.method == 'POST':
        name = request.POST.get('name')

        if not name:
            messages.error(request, 'Please enter a designation')
        elif Designation.objects.filter(name__iexact=name).exists():
            messages.error(request, 'This desination is alredy exist.')
        else:
             Designation.objects.create(name=name)
             messages.success(request, 'Designation added successfully.')
             return redirect('employee_list')

    designation = Designation.objects.all().order_by('name')

    return render(request, 'add_designation.html', {'designation':designation})

def edit_designation(request, id):

    designation = get_object_or_404(Designation, id=id)
    if request.method == 'POST':
        name = request.POST.get('name')
    
        if not name:
            messages.error(request, 'Please enter a designation')
        elif Designation.objects.filter(name__iexact=name).exists():
            messages.error(request, 'This desination is alredy exist.')
        else:
            designation.name = name
            designation.save()
            messages.success(request, 'Designation added successfully.')
            return redirect('employee_list')

    
    return render(request, 'edit_designation.html', {'designation':designation})

def delete_designation(request, id):
    designation = get_object_or_404(Designation, id=id)
    
    if request.method == 'POST':

        employees = Employees.objects.filter(designation=designation)
        if employees.exists():
            messages.error(
                request,
                'Cannot delete this designation because employees are assigned to it.'
            )

        else:
            designation.delete()
            messages.success(request, 'Employee deleted successfully.')
        return redirect('employee_list')
    
    return render(request, 'delete_designation.html', {'desiganation': designation})

def add_employee(request):
    designation = Designation.objects.all().order_by('name')
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        designation_id = request.POST.get('designation')
        salary = request.POST.get('salary')

        if Employees.objects.filter(email=email).exists():
            messages.error(request, 'This email is already exists.')
            return render(request, 'add_employee.html', {'designation': designation})

        if Employees.objects.filter(phone=phone).exists():
            messages.error(request, 'This Phone Number is already exists.')
            return render(request, 'add_employee.html', {'designation': designation})

        if not designation_id:
            messages.error(request, 'Please select a designation')
            return render(
                request, 'add_employee.html',
                {'designation': designation}
            )

        last = Employees.objects.order_by('-id').first()
        next_id = (last.id + 1) if last else 1

        username = f"EMP{next_id:04d}"
        password = random_password()

        try:
            salary = float(salary)
        
            if salary <= 0:
                messages.error(request, 'Must be a valid positive number.')
                return render(request, 'add_employee.html')
        
        except (ValueError, TypeError):
            messages.error(request, 'Please enter a valid number.')
            return render(request, 'add_employee.html')

        Employees.objects.create(
            name=name,
            email=email,
            phone=phone,
            designation_id=designation_id,
            salary=salary,
            user_name = username,
            password = password
        )
        
        messages.success(request,'Employee created successfully.')

        return redirect('employee_list')
        
        
    return render(request, 'add_employee.html', {'designation': designation})

def update_employee(request, id):

    designation = Designation.objects.all().order_by('name')

    employee = get_object_or_404(Employees, id=id)

    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        designation_id = request.POST.get('designation')
        salary = request.POST.get('salary')

        if Employees.objects.filter(email=email).exclude(id=employee.id).exists():
            messages.error(request, 'This email is already exists.')
            return render(request, 'add_employee.html', {'designation': designation})

        if Employees.objects.filter(phone=phone).exclude(id=employee.id).exists():
            messages.error(request, 'This Phone Number is already exists.')
            return render(request, 'add_employee.html', {'designation': designation})   

        if not designation_id:
            messages.error(request, 'Please select a designation')
            return render(
                request, 'add_employee.html',
                {'designation': designation}
            )     

        try:
            salary = float(salary)
        
            if salary <= 0:
                messages.error(request, 'Must be a valid positive number.')
                return render(request, 'add_employee.html')
        
        except (ValueError, TypeError):
            messages.error(request, 'Please enter a valid number.')
            return render(request, 'add_employee.html')

        employee.name = name
        employee.email = email
        employee.phone = phone
        designation_id=designation_id,
        employee.salary = salary

        employee.save()

        messages.success(request, 'Employee Updated Successfully.')

        return redirect('employee_list')

    context = {
        'designation': designation,
        'employee':employee
    }

    return render(request, 'add_employee.html', context)




def employee_details(request, id):

     employee = get_object_or_404(Employees, id=id)

     return render(request, 'employee_details.html', {'employee':employee})
     
def delete_employee(request, id):
    employee = get_object_or_404(Employees, id=id)

    if request.method == 'POST':
        employee.delete()
        messages.success(request, 'Employee deleted successfully.')
        return redirect('employee_list')

    return render(request, 'delete_employee.html', {'employee': employee})


def employee_login(request):

    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            employee = Employees.objects.get(user_name = username)

            if employee.password == password:
                request.session['employee_id'] = employee.id
                return redirect('employee_dashboard')

            else:
                messages.error(request, "Incorrect Password")
        

        except Employees.DoesNotExist:
            messages.error(request, "Invalid Username Not found")

    return render(request, 'login.html')

def employee_dashboard(request):
    employee_id = request.session.get('employee_id')

    if not employee_id:
        return redirect('employee_login')

    employee = Employees.objects.get(id=employee_id)

    return render(
        request,
        'employee_dashboard.html',
        {'employee': employee}
    )


def edit_profile(request):
    employee_id = request.session.get('employee_id')

    if not employee_id:
        return redirect('employee_login')

    employee = Employees.objects.get(id=employee_id)

    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        gender = request.POST.get('gender')

        profile_picture = request.FILES.get('profile_picture')

        if profile_picture and profile_picture.size > 2 * 1024 * 1024:
            messages.error(request, 'Profile picture must not exceed 2 MB.')
            return render(request, 'edit_profile.html', {'employee': employee})

        if Employees.objects.filter(email=email).exclude(id=employee.id).exists():
            messages.error(request, 'This email is already exists.')
        
        elif Employees.objects.filter(phone=phone).exclude(id=employee.id).exists():
            messages.error(request, 'This Phone Number is already exists.')

        else:
            employee.name = name
            employee.email = email
            employee.phone = phone
            employee.gender = gender

            if profile_picture:
                employee.profile_picture = profile_picture

            employee.save()

            messages.success(request, 'Profile updated successfully.')
            return redirect('employee_dashboard')
        
    return render(request, 'edit_profile.html', {'employee': employee})


def change_password(request):

    employee_id = request.session.get('employee_id')

    if not employee_id:
        return redirect('employee_login')

    employee = Employees.objects.get(id=employee_id)

    if request.method == 'POST':
        current_password = request.POST.get('current_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        if current_password != employee.password:
            messages.error(request, 'Current Password is Incorrect')

        elif new_password != confirm_password:
            messages.error(request, "New Password do note match")

        elif len(new_password) < 8:
            messages.error(request, "Password mus contains atleast 8 characters")

        else:
            employee.password = new_password
            employee.save(update_fields=['password'])

            messages.success(request, 'Password changed successfully.')
            return redirect('employee_dashboard')

    return render(request, 'change_password.html')
