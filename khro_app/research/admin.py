from django.contrib import admin
from django.utils.html import format_html
from django.contrib.auth.decorators import permission_required
from . import models
import data_wizard #this may be the Godsent solution to data import madness that has refused to go
from . models import (StgDiseaseDomain,StgResearchThemes,StgEthicsCommittee,
    StgResearchProposal,StgKnowledgePipelineType,StgResearchTopic,
    StgKnowledgePipeline)
#from .resources import StgKnowledgeProductResourceExport,StgKnowledgeProductResourceImport
from import_export.admin import (ImportExportModelAdmin, ExportMixin,
    ImportExportActionModelAdmin)
from import_export.formats import base_formats
from django.forms import TextInput,Textarea #for customizing textarea row and column size
from khro_app.common_info.admin import OverideExport
from khro_app.regions.models import StgLocation

from django_admin_listfilter_dropdown.filters import (
    DropdownFilter, RelatedDropdownFilter, ChoiceDropdownFilter,
    RelatedOnlyDropdownFilter) #custom

#the following functions are used to register global actions performed on the data. See actions listbox
def transition_to_pending (modeladmin, request, queryset):
    queryset.update(comment = 'pending')
transition_to_pending.short_description = "Mark selected as Pending"

def transition_to_approved (modeladmin, request, queryset):
    queryset.update (comment = 'approved')
transition_to_approved.short_description = "Mark selected as Approved"

def transition_to_rejected (modeladmin, request, queryset):
    queryset.update (comment = 'rejected')
transition_to_rejected.short_description = "Mark selected as Rejected"

'''
--------------------------------------------------------------------------------
These are ModelAdmins that facilitate viewing of knowledge products and their
related dimensions
--------------------------------------------------------------------------------
'''
#data_wizard.register(StgKnowledgeProduct) #register knowledge product to allow wizard driven import

@admin.register(StgDiseaseDomain)
class ICD_Domains_Admin(OverideExport):
    from django.db import models
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size':'80'})},
        models.TextField: {'widget': Textarea(attrs={'rows':3, 'cols':120})},
    }

    list_display=['name','code','description','parent','level']
    list_display_links =('code', 'name',)
    search_fields = ('code','name',) #display search field
    list_per_page = 30 #limit records displayed on admin site to 30

    list_filter = (
        ('parent', RelatedOnlyDropdownFilter,),
        ('level', DropdownFilter,),
    )

    exclude = ('uuid','date_created','date_lastupdated','code',)


@admin.register(StgResearchThemes)
class Research_StreamAdmin(OverideExport):
    from django.db import models
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size':'80'})},
        models.TextField: {'widget': Textarea(attrs={'rows':3, 'cols':120})},
    }

    filter_horizontal = ('domains',) # this should display an inline with multiselect
    list_display=['name','code','description']
    list_display_links =('code', 'name',)
    search_fields = ('code','name',) #display search field
    list_per_page = 30 #limit records displayed on admin site to 15
    exclude = ('uuid','date_created','date_lastupdated','code',)

@admin.register(StgEthicsCommittee)
class Research_CommitteeAdmin(OverideExport):
    from django.db import models
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size':'80'})},
        models.TextField: {'widget': Textarea(attrs={'rows':3, 'cols':120})},
    }

    list_display=['name','license_number','location','authorization']
    list_display_links =('name', 'license_number',)
    search_fields = ('name','license_number',) #display search field
    list_per_page = 30 #limit records displayed on admin site to 15
    exclude = ('uuid','date_created','date_lastupdated','code',)


@admin.register(StgKnowledgePipelineType)
class KnowledgePipeline_TypeAdmin(OverideExport):
    from django.db import models
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size':'80'})},
        models.TextField: {'widget': Textarea(attrs={'rows':3, 'cols':120})},
    }

    list_display=['name','code','description']
    list_display_links =('code', 'name',)
    search_fields = ('code','name',) #display search field
    list_per_page = 30 #limit records displayed on admin site to 15
    exclude = ('uuid','date_created','date_lastupdated','code',)


@admin.register(StgResearchTopic)
class Research_TopicAdmin(OverideExport):
    from django.db import models
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size':'80'})},
        models.TextField: {'widget': Textarea(attrs={'rows':3, 'cols':120})},
    }

    list_display=['name','code','description']
    list_display_links =('code', 'name',)
    search_fields = ('code','name',) #display search field
    list_per_page = 30 #limit records displayed on admin site to 15
    exclude = ('uuid','date_created','date_lastupdated','code',)


data_wizard.register(StgKnowledgePipeline) #register fact data element to allow wizard driven import
@admin.register(StgKnowledgePipeline)
class Knowledge_Pipeline_Admin(ImportExportModelAdmin,ImportExportActionModelAdmin):
    from django.db import models
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size':'80'})},
        models.TextField: {'widget': Textarea(attrs={'rows':3, 'cols':120})},
    }

    #This function is used to register permissions for approvals. See signals,py
    def get_actions(self, request):
        actions = super(Knowledge_Pipeline_Admin, self).get_actions(request)
        if not request.user.has_perm('research.approve_stgknowledgepipeline'):
           actions.pop('transition_to_approved', None)

        if not request.user.has_perm('research.reject_stgknowledgepipeline'):
            actions.pop('transition_to_rejected', None)

        if not request.user.has_perm('research.delete_stgknowledgepipeline'):
            actions.pop('delete_selected', None)
        return actions

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser or request.user.groups.filter(
            name__icontains='Admin'):
            return qs #provide access to all instances/rows of all location,
        return qs.filter(location_id=request.user.location_id)

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

    fieldsets = (
        ('Product Description', {
                'fields': ('title', 'type','theme','description','quality_level',)
            }),
            (' Publication details ', {
                'fields': ('main_author','co_authors','author_affiliations',
                'publisher','year_published','location','sharing_status','sort_order'),
            }),
            (' Abstract and Access', {
                'fields': ('abstract','internal_link','external_link',
                'cover_image'),
            }),
        )

    def get_location(obj):
           return obj.location.name
    get_location.short_description = 'Location'

    def get_type(obj):
           return obj.type.name
    get_type.short_description = 'Type'

    # To display the choice field values use the helper method get_foo_display
    list_display=['title','code',get_type, get_location,'quality_level']
    list_display_links = ['code','title',]
    search_fields = ('title','type__name','location__name',) #display search field
    list_per_page = 30 #limit records displayed on admin site to 30
    list_filter = (
        ('location',RelatedOnlyDropdownFilter),
        ('type',RelatedOnlyDropdownFilter),
    )

    actions = [transition_to_pending, transition_to_approved, transition_to_rejected]
    exclude = ('date_created','date_lastupdated','code',)

data_wizard.register(StgResearchProposal) #register publication serializer to allow wizard driven import
@admin.register(StgResearchProposal)
class Research_ProposalAdmin(OverideExport):
    from django.db import models
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size':'80'})},
        models.TextField: {'widget': Textarea(attrs={'rows':3, 'cols':120})},
    }
    filter_horizontal = ('domains',) # this should display an inline with multiselect
    list_display=['title','research_objective','principal_researcher',
        'num_of_researchers','affiliate_insititutions','funding_source','approval_status']
    list_display_links =('title','principal_researcher', 'affiliate_insititutions',)
    search_fields = ('affiliate_insititutions','affiliate_insititutions',) #display search field
    list_per_page = 30 #limit records displayed on admin site to 15
    exclude = ('uuid','date_created','date_lastupdated','code',)
