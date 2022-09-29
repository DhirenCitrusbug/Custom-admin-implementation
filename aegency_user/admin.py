from django.contrib import admin
from .models import AgencyUser, AgencyHostname
# Register your models here.

admin.site.register(AgencyUser)
admin.site.register(AgencyHostname)