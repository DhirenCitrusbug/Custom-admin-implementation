from django.db import models
from admin_user.models import ActivityTracking
from .agency_user import AgencyUser
from admin_user.models import Admin, Address


class AgencyHostname(ActivityTracking):
    user = models.ForeignKey(AgencyUser, on_delete=models.SET_NULL, blank=True, null=True)
    host_id = models.CharField(max_length=250, blank=True, null=True)
    hostname = models.CharField(max_length=250, blank=True, null=True)
    response = models.JSONField(blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.hostname