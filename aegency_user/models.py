# from django.db import models
# from admin_user.models import Admin, Address, ActivityTracking
# # Create your models here.


# class AgencyUser(Admin):
#     business_name = models.CharField(max_length=30, blank=True, null=True)
#     business_email = models.EmailField(blank=True, null=True)
#     business_phone_no = models.CharField(max_length=15, blank=True, null=True)
#     whitelabeldomian = models.CharField(max_length=200, blank=True, null=True)
#     transaction_id = models.CharField(max_length=100, blank=True, null=True)
#     plan_duration = models.CharField(max_length=100, blank=True, null=True)
#     account_sid = models.CharField(max_length=100, blank=True, null=True)
#     auth_token = models.TextField(blank=True, null=True)
#     owner = models.ForeignKey(Admin, on_delete=models.CASCADE, related_name='admin_user')
#     address = models.ForeignKey(Address, on_delete=models.SET_NULL, blank=True, null=True)
#     support_email = models.EmailField(blank=True, null=True)
#     host = models.ForeignKey("AgencyHostname", on_delete=models.CASCADE, null=True, blank=True)

#     def __str__(self):
#         return self.first_name

# class AgencyHostname(ActivityTracking):
#     user = models.ForeignKey(AgencyUser, on_delete=models.SET_NULL, blank=True, null=True)
#     host_id = models.CharField(max_length=250, blank=True, null=True)
#     hostname = models.CharField(max_length=250, blank=True, null=True)
#     response = models.JSONField(blank=True, null=True)
#     is_verified = models.BooleanField(default=False)
#     is_deleted = models.BooleanField(default=False)

#     def __str__(self):
#         return self.hostname