from django.db import models
from ckeditor.fields import RichTextField
from core.models import User

CommnetType = (
    ("Review", 'Review'),
    ("Brand", 'Brand'),
    ("Category", 'Category'),
    ("Custom_Landing", 'Custom Landing'),
)


class Comments(models.Model):
    ip = models.CharField(max_length=50, null=True, blank=True)
    name = models.CharField(max_length=150, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    description = RichTextField()
    comment_type = models.CharField(max_length=255, choices=CommnetType, default='Review')
    comment_type_id = models.IntegerField()
    is_approved = models.BooleanField(default=False)
    parent_id = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='child_comment')
    is_spam = models.BooleanField(default=False)
    is_notification = models.BooleanField(default=False)
    old_id = models.IntegerField(default=0)

    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        if self.name:
            return str(self.name)
        else:
            return 'anonymous'

    class Meta:
        db_table = "comments"
        verbose_name = "comment"
        verbose_name_plural = "comments"
        indexes = [
            models.Index(fields=['id']),
            models.Index(fields=['ip', 'is_approved']),
        ]


class UpVote(models.Model):
    comment_id = models.ForeignKey(Comments, on_delete=models.CASCADE)
    ip = models.CharField(max_length=50, null=False, blank=False)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "upvote"
        verbose_name = "upvote"
        verbose_name_plural = "upvotes"
        indexes = [
            models.Index(fields=['id']),
            models.Index(fields=['ip']),
        ]
