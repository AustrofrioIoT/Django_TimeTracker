from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdminn
from .models import User
from .forms import UserCreationForm, UserChangeForm
from django.contrib.auth.hashers import make_password

# class CustomUserAdmin(admin.ModelAdmin):
# 	ordering = ('-id', 'last_name', )
# 	list_display = ('id', 'email', 'password', 'first_name', 'is_active')

# 	def save_model(self, request, obj, form, change):
# 		if not change:
# 			obj.password = make_password(request.POST['password'])
# 		return super(CustomUserAdmin, self).save_model(request, obj, form, change)

class CustomUserAdmin(BaseUserAdminn):
    form = UserChangeForm
    add_form = UserCreationForm
    list_display = ('id','first_name','last_name','email', 'is_staff', 'is_active', 'is_superuser', )
    list_filter = ('email', 'is_staff', 'is_active',)
    fieldsets = (
        ('User info', {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'direction', 'province', 'country', 'telephone', 'avatar')}),
        ('Permissions', {'fields': ('is_active', 'is_staff')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    search_fields = ('email',)
    ordering = ('-id',)

admin.site.register(User, CustomUserAdmin)
admin.site.unregister(Group)
