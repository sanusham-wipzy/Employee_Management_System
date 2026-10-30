from django.db import models

# Create your models here.

class Designation(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Employees(models.Model):
    name = models.CharField(max_length = 100)
    email = models.EmailField()
    designation = models.ForeignKey(
        Designation,
        on_delete=models.PROTECT
    )
    phone = models.CharField(max_length=15)
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at =models.DateTimeField(auto_now=True)
    user_name = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    profile_picture = models.ImageField(
        upload_to='profile_pictures/',
        blank=True,
        null=True
    )
    gender = models.CharField(
        max_length=10,
        choices=[
            ('Male', 'Male'),
            ('Female', 'Female'),
            ('Other', 'Other')
        ],
        blank=True
    )

    def __str__(self):
        return self.name

    
