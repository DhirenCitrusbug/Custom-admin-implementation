from django.db import models
from . import User

PUBLISH_STATUS = (
	('Published', 'Published'),
	('Draft', 'Draft'),
)


class TrustedAccessories(models.Model):
	name = models.CharField(max_length=255)
	slide_link = models.CharField(max_length=255, null=True, blank=True)
	alt_text = models.CharField(max_length=255, null=True, blank=True)
	featured_image = models.ImageField(upload_to='trusted-images/', null=True, blank=True)
	status = models.CharField(max_length=50, choices=PUBLISH_STATUS, default='Draft')

	create_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
	create_at = models.DateTimeField(auto_now_add=True)
	update_at = models.DateTimeField(auto_now=True)

	def __str__(self):
		return str(self.name)

	# def get_absolute_url(self):
	# 	return f"{self.slug}"
	# 	# return reverse("core:review-list")

	class Meta:
		db_table = "trusted_accessories"
		verbose_name = "Trusted Accessory"
		verbose_name_plural = "Trusted Accessories"
		indexes = [
			models.Index(fields=['id']),
			models.Index(fields=['name']),
		]
