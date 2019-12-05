import data_wizard #this may be the Godsent solution to data import madness that has refused to go
from data_wizard.sources.models import FileSource,URLSource #customize import soureces

from django.contrib import admin
from django.contrib.admin import AdminSite #customize adminsite
from import_export.admin import (ImportExportModelAdmin, ExportActionModelAdmin,
    ExportMixin,ImportMixin,ExportActionModelAdmin) #added exportaction mixin only
from import_export.formats import base_formats
#these libraries are imported to support monkey of admin_menu package
from django.urls import resolve, reverse, NoReverseMatch
from django.utils.text import capfirst

#import custom menu for customization to change apps order
from admin_menu.templatetags import custom_admin_menu

# Customize the site admin header for login, title bar, and data admin form section.
class AdminSite(AdminSite):
    site_header = 'Kenya Health and Research Observatory' #also shown on login form
    site_title = 'KHRO Data Capture and Admin Tool' #shown on the title bar
    index_title = 'KHRO Data Management' #shown in the content section

#Import this method and do nothing to it. It is required by get_app_list()!!
def get_admin_site(context):
    pass

get_admin_site = custom_admin_menu.get_admin_site #assign as is!

# Now this is the method that does the menu tweaks using the ordering dict!!!
def get_app_list(context, order=True):
    admin_site = get_admin_site(context)
    request = context['request']

    app_dict = {}
    for model, model_admin in admin_site._registry.items():
        app_label = model._meta.app_label
        try:
            has_module_perms = model_admin.has_module_permission(request)
        except AttributeError:
            has_module_perms = request.user.has_module_perms(app_label) # Fix Django < 1.8 issue

        if has_module_perms:
            perms = model_admin.get_model_perms(request)
            # Check whether user has any permission for this module.
            # If so, add the module to the model_list.
            if True in perms.values():
                info = (app_label, model._meta.model_name)
                model_dict = {
                    'name': capfirst(model._meta.verbose_name_plural),
                    'object_name': model._meta.object_name,
                    'perms': perms,
                    'model_admin': model_admin,
                }
                if perms.get('change', False):
                    try:
                        model_dict['admin_url'] = reverse('admin:%s_%s_changelist' % info,
                        current_app=admin_site.name)
                    except NoReverseMatch:
                        pass
                if perms.get('add', False):
                    try:
                        model_dict['add_url'] = reverse('admin:%s_%s_add' % info,
                        current_app=admin_site.name)
                    except NoReverseMatch:
                        pass
                if app_label in app_dict:
                    app_dict[app_label]['models'].append(model_dict)
                else:
                    try:
                        name = apps.get_app_config(app_label).verbose_name
                    except NameError:
                        name = app_label.title()
                    app_dict[app_label] = {
                        'name': name,
                        'app_label': app_label,
                        'app_url': reverse(
                            'admin:app_list',
                            kwargs={'app_label': app_label},
                            current_app=admin_site.name,
                        ),
                        'has_module_perms': has_module_perms,
                        'models': [model_dict],
                    }

    # This is the dict to take care of memu ordering on KHRO admin interface
    ordering = {
    'Home':1,
    'Indicators':2,
    'Research':3,
    'Elements':4,
    'Regions':5,
    'Commodities': 6,
    'Authentication':7,
    'Sources':8,
    'Data_Wizard':9,
    }
    # Create the list to be sorted using python ordering dictionary.
    app_list = list(app_dict.values())
    # This code is used to remove (pop) the Auth menu from navigation menu
    auth_menu = [
        app_items for app_items in app_list if app_items['name'] == 'Auth'][0]
    auth_menu_index = app_list.index(auth_menu)
    app_list.pop(auth_menu_index)

    #Note that the ordering dict has been added here to effect the custom ordering
    if order:
        app_list.sort(key=lambda x: ordering[x['name']])
        # Sort the models alphabetically within each app.
        for app in app_list:
            app['models'].sort(key=lambda x: x['name'])
    return app_list
#apply the menu patching so that menu appears as per the order defined above
custom_admin_menu.get_app_list = get_app_list


class OverideImportExport(ImportExportModelAdmin):
    def get_import_formats(self):
        """
        Returns available export formats.
        """
        formats = (
              base_formats.CSV,
              base_formats.XLS,
              base_formats.XLSX,
        )
        return [f for f in formats if f().can_import()]

    def get_export_formats(self):
        """
        Returns available export formats.
        """
        formats = (
              base_formats.CSV,
              base_formats.XLS,
              base_formats.XLSX,
        )
        return [f for f in formats if f().can_export()]

#This class is used to override export base format types to limit to only CSV,XLS and XLSx
class OverideExport(ExportMixin, admin.ModelAdmin):
    def get_export_formats(self):
        """
        Returns available export formats.
        """
        formats = (
              base_formats.CSV,
              base_formats.XLS,
              base_formats.XLSX,
        )
        return [f for f in formats if f().can_export()]


#This class is used to override export base format types to limit to only CSV,XLS and XLSx
class OverideExportAdmin(ExportActionModelAdmin, ExportMixin, admin.ModelAdmin):
    def get_export_formats(self):
        """
        Returns available export formats.
        """
        formats = (
              base_formats.CSV,
              base_formats.XLS,
              base_formats.XLSX,
        )
        return [f for f in formats if f().can_export()]

#This class is used to override import base format types to limit to only CSV,XLS and XLSx
class OverideImport(ImportMixin, admin.ModelAdmin):
    def get_import_formats(self):
        """
        Returns available export formats.
        """
        formats = (
              base_formats.CSV,
              base_formats.XLS,
              base_formats.XLSX,
        )
        return [f for f in formats if f().can_import()]
