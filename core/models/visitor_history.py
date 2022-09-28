from django.db import models


class VisitorHistory(models.Model):
    ip = models.CharField(max_length=80)
    type = models.CharField(max_length=100)
    type_name = models.CharField(max_length=150)
    type_url = models.CharField(max_length=255)

    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "visitor_history"
        verbose_name = "Visitor History"
        verbose_name_plural = "Visitor Histories"
        indexes = [
            models.Index(fields=['id']),
            models.Index(fields=['ip', 'type']),
        ]
