from django.contrib import admin
from . import models
from django.contrib.admin.models import LogEntry
from django.contrib.auth.admin import GroupAdmin as BaseGroupAdmin
from django.contrib.auth.models import Group, User
from django.contrib.auth.admin import UserAdmin


import data_wizard #this may be the Godsent solution to data import madness that has refused to go
from data_wizard.sources.models import FileSource,URLSource #customize import soureces

from . models import CustomUser, CustomGroup

#from . models import FileSource,URLSource

from django_admin_listfilter_dropdown.filters import (
    DropdownFilter, RelatedDropdownFilter, ChoiceDropdownFilter, RelatedOnlyDropdownFilter) #custom
from common_info.admin import OverideImportExport, OverideExport, OverideExportAdmin


@admin.register(CustomUser)
class UserAdmin (UserAdmin):
    readonly_fields = ('last_login','date_joined',)

    fieldsets = (
        ('Personal info', {'fields': ('title','first_name', 'last_name','gender','location')}),
        ('Login Credentials', {'fields': ('email', 'username','password',)}),
        ('Account Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Login Details', {'fields': ('last_login',)}),
    )

    limited_fieldsets = (
        (None, {'fields': ('email',)}),
        ('Personal info', {'fields': ('first_name', 'last_name','location')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2')}
        ),
    )

    list_display = ['first_name','last_name','username','email','gender','location','date_joined','last_login']
    list_display_links = ['first_name','last_name','username','email']

@admin.register(CustomGroup)
class GroupAdmin(BaseGroupAdmin):# This is a custom dome group
    list_display = ['name','group_manager']
