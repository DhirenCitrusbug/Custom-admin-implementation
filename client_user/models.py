from django.db import models
from admin_user.models import Admin,Address
from client.models import Client
# Create your models here.

class ClientUser(Admin):
    account_sid=models.CharField(max_length=100,blank=True,null=True)
    auth_token=models.TextField(blank=True,null=True)
    client_owner=models.ForeignKey(Client,on_delete=models.CASCADE,related_name='client_owner')
    address=models.ForeignKey(Address,on_delete=models.SET_NULL,blank=True,null=True)
    server_passcode=models.CharField(max_length=100,blank=True,null=True)

    def __str__(self):
        return self.first_name