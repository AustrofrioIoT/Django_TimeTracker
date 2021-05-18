from django.db.models import fields
from django.contrib.auth import get_user_model
from django.forms import *
from django import forms
from .models import Employee, Company, Department, Role
from users.forms import UserCreationForm

from betterforms.multiform import MultiModelForm
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from tempus_dominus.widgets import DateTimePicker

import datetime

User = get_user_model()


class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ('type_of_employee', 'department', 'role', 'observations', 'date_hired')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in iter(self.fields):
            # print('Field -------> ', field)
            self.fields[field].widget.attrs.update({
                'class': 'form-control',
                'autocomplete': 'off',
                'autofocus': True
            })
        self.fields['observations'].widget.attrs['cols'] = '30'
        self.fields['observations'].widget.attrs['rows'] = '3'
        self.fields['date_hired'] = DateTimeField(
            widget=DateTimePicker(
                options={
                    "format": "YYYY-MM-DD HH:mm:ss",
                    'sideBySide': True,
                }
            )
        )
    # self.fields['sub_total'].widget.attrs['readonly']=True
    # self.fields['descuento'].widget.attrs['readonly']=True
    # self.fields['total'].widget.attrs['readonly']=True


class UserCreationMultiForm(MultiModelForm):
    form_classes = {
        'user': UserCreationForm,
        'employee': EmployeeForm,
    }


class UserEditForm(forms.ModelForm):
    # password = ReadOnlyPasswordHashField()
    avatar = forms.ImageField(required=False)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'direction', 'province', 'country', 'telephone', 'avatar')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })


class EmployeeEditForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ('type_of_employee', 'department', 'role', 'observations', 'date_hired')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })
        self.fields['observations'].widget.attrs['cols'] = '30'
        self.fields['observations'].widget.attrs['rows'] = '3'
        self.fields['date_hired'] = DateTimeField(
            widget=DateTimePicker(
                options={
                    "format": "YYYY-MM-DD HH:mm:ss",
                    'sideBySide': True,
                }
            )
        )


class UserEditMultiForm(MultiModelForm):
    form_classes = {
        'user': UserEditForm,
        'employee': EmployeeEditForm,
    }


class CompanyForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for form in self.visible_fields():
            form.field.widget.attrs['class'] = 'form-control'
            form.field.widget.attrs['autocomplete'] = 'off'
            form.field.widget.attrs['autofocus'] = True

    class Meta:
        model = Company
        fields = '__all__'
        widgets = {
            'name': TextInput(
                attrs={
                    'placeholder': 'Insert Company Name',
                }
            ),
        }


class DepartmentForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for form in self.visible_fields():
            form.field.widget.attrs['class'] = 'form-control'
            form.field.widget.attrs['autocomplete'] = 'off'
            form.field.widget.attrs['autofocus'] = True

    class Meta:
        model = Department
        fields = '__all__'
        widgets = {
            'name': TextInput(
                attrs={
                    'placeholder': 'Insert Department Name',
                }
            ),
        }


class RoleForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for form in self.visible_fields():
            form.field.widget.attrs['class'] = 'form-control'
            form.field.widget.attrs['autocomplete'] = 'off'
            form.field.widget.attrs['autofocus'] = True

    class Meta:
        model = Role
        fields = '__all__'
        widgets = {
            'name': TextInput(
                attrs={
                    'placeholder': 'Insert Role Name',
                }
            ),
        }
