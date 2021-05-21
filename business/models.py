from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy, reverse
from django.db.models.signals import post_save
from django.dispatch import receiver

User = get_user_model()


class Company(models.Model):
    name = models.CharField(max_length=255, verbose_name='Company name', unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Company'
        verbose_name_plural = 'Companies'


class Department(models.Model):
    name = models.CharField(max_length=255, verbose_name='Department name', unique=True)
    company = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True, verbose_name='Company name')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Department'
        verbose_name_plural = 'Departments'
        ordering = ['id']


class Role(models.Model):
    name = models.CharField(max_length=255, verbose_name='Role name', unique=True)
    depatrment = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, verbose_name='Department name')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Role'
        verbose_name_plural = 'Roles'


class TypeEmployee(models.Model):
    type_employee = models.CharField(max_length=20, unique=True, verbose_name='Type of Employee')

    def __str__(self):
        return '{}'.format(self.type_employee)

    class Meta:
        verbose_name = 'Type of Employee'
        verbose_name_plural = 'Types of Employees'


class Employee(models.Model):
    type_of_employee = models.ForeignKey(TypeEmployee, on_delete=models.SET_NULL, null=True, default=None)
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, default=None)
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True, default=None)
    observations = models.TextField(verbose_name='Observations', null=True, blank=True, default=None)
    date_hired = models.DateField(verbose_name='Date hired', null=True, default=None)

    class Meta:
        ordering = ['-id', ]

    def __str__(self):
        return '{}'.format(self.user)  #.format(self.id, self.user.id, self.user, self.role, self.type_of_employee)

    def get_absolute_url(self):
        return reverse('webapp:admin-employee-update', args=[str(self.id)])

# @receiver(post_save, sender=User)
# def create_user_profile(sender, instance, created, **kwargs):
#     if created:
#         Employee.objects.create(user=instance)

# @receiver(post_save, sender=User)
# def save_user_profile(sender, instance, **kwargs):
#     instance.employee.save()
