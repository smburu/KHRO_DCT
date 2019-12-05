"""
The two classes in this module overrides original Django User and Group classess.
"""
from django.db import models
from django.contrib.auth.models import Group, AbstractUser
from khro_app.regions.models import StgLocation

def make_choices(values):
    return [(v, v) for v in values]


# This custom model class overrides the library Django user auth model.
class CustomUser(AbstractUser):
    GENDER = ( 'Male','Female', 'Other')
    TITLE = ( 'Mr.','Ms.', 'Mrs.','Dr.', 'Prof.', 'Other')
    title = models.CharField(max_length=45, choices=make_choices(TITLE),
        default=GENDER[0])  # Field name made lowercase.
    gender = models.CharField(max_length=45, choices=make_choices(GENDER),
        default=GENDER[0])  # Field name made lowercase.
    email = models.EmailField(unique=True,blank=False, null=False)
    postcode = models.CharField(max_length=6)
    username = models.CharField(blank=False, null=False, max_length=150)
    location = models.ForeignKey(
        StgLocation, models.PROTECT, verbose_name='Location', default=2)

    REQUIRED_FIELDS = ['postcode', 'username']
    USERNAME_FIELD = 'email'

    class Meta:
        managed = True
        verbose_name = 'User'
        verbose_name_plural = '  Manage Users'
        ordering = ('username', )

    def __str__(self):
        return self.email


# This model class overrides the original Django Group model.
class CustomGroup(Group):
        # This has made it possible to move group menu to settings module/app
        group = models.OneToOneField('auth.Group', parent_link=True,
            unique=True,on_delete=models.CASCADE)
        group_manager = models.CharField(max_length=70, blank=False,
            default="Staff")

        class Meta:
            managed = True
            verbose_name = 'Group'
            verbose_name_plural = ' Manage Groups'

        def __str__(self):
            return "{}".format(self.group.name)
