from django.db import models


class ContactUs(models.Model):
    name = models.CharField(max_length=80)
    email = models.EmailField()
    message = models.TextField()
    is_spam = models.BooleanField(default=False)
    
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return str(self.name)
    
    class Meta:
        db_table = "contact_us"
        verbose_name = "contact_us"
        verbose_name_plural = "contact_us"
