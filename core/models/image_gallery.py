from django.db import models
from core.utils import resize_image


class ImageGallery(models.Model):
	name = models.CharField(max_length=255)
	alt_text = models.CharField(max_length=255, null=True, blank=True)
	title = models.CharField(max_length=255)
	caption = models.TextField(null=True, blank=True)
	description = models.TextField(null=True, blank=True)
	image_size = models.CharField(max_length=20)
	ratio = models.CharField(max_length=50)
	image = models.ImageField(upload_to='image-gallery')
	thumbnail_image = models.ImageField(upload_to='thumbnail-image-gallery')

	create_at = models.DateTimeField(auto_now_add=True)
	update_at = models.DateTimeField(auto_now=True)

	def __str__(self):
		return str(self.name)

	def save(self, *args, **kwargs):
		if self.image:
			self.thumbnail_image = resize_image(self.image, (300, 225))
		super().save(*args, *kwargs)

	class Meta:
		db_table = "image_gallery"
