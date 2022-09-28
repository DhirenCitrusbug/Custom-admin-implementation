from django.db.models.signals import pre_save, post_save
from django.db import models
from django.urls import reverse
from .users import User
from core.utils import category_brand_slugify, resize_image

PUBLISH_STATUS = (
	('Published', 'Published'),
	('Draft', 'Draft'),
)


class ReviewCategory(models.Model):
	name = models.CharField(max_length=255)
	slug = models.SlugField(max_length=255, unique=True, null=True, blank=True)
	meta_title = models.CharField(max_length=255, null=True, blank=True)
	description = models.TextField()
	short_description = models.TextField()
	category_image_full = models.ImageField(upload_to='category-images/', null=True, blank=True)
	category_image_web = models.ImageField(upload_to='category-web-images/', null=True, blank=True)
	category_image_mobile = models.ImageField(upload_to='category-mobile-images/', null=True, blank=True)
	icon_image = models.ImageField(upload_to='category-icon-images/', null=True, blank=True)
	parent_category = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)
	status = models.CharField(max_length=50, choices=PUBLISH_STATUS, default='Draft')
	featured_review = models.CharField(max_length=100, null=True, blank=True)
	create_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
	create_at = models.DateTimeField(auto_now_add=True)
	update_at = models.DateTimeField(auto_now=True)

	def __str__(self):
		return str(self.name)

	def save(self, *args, **kwargs):
		if self.category_image_full:
			self.category_image_mobile = resize_image(self.category_image_full, (97, 52))
			self.category_image_web = resize_image(self.category_image_full, (432, 239))
		super().save(*args, *kwargs)

	def get_absolute_url(self):
		return f'/category/{self.slug}/'


	class Meta:
		db_table = "review_category"
		verbose_name = "Review category"
		verbose_name_plural = "Review categories"
		indexes = [
			models.Index(fields=['id']),
			models.Index(fields=['name']),
			models.Index(fields=['slug']),
		]


# Here we are use signal for create slug.
def review_category_pre_save(sender, instance, *args, **kwargs):
	"""
		Pre save signal use for review category slug generate.
	"""
	# print('pre_save')
	if instance.slug is None or instance.slug == '':
		category_brand_slugify(instance, save=False)
	else:
		category_brand_slugify(instance, save=False, new_slug=instance.slug)

	if instance.meta_title is None or instance.meta_title == '':
		try:
			instance.meta_title = instance.name.title() + ' | ElectricBikeReview.com'
			instance.save()
		except:
			pass


pre_save.connect(review_category_pre_save, sender=ReviewCategory)


def review_category_post_save(sender, instance, created, *args, **kwargs):
	"""
		Post save signal use for review category slug generate.
	"""
	# print('post_save')
	if created:
		if instance.slug is None:
			category_brand_slugify(instance, save=False)
		else:
			category_brand_slugify(instance, save=False, new_slug=instance.slug)
	if instance.meta_title is None or instance.meta_title == '':
		try:
			instance.meta_title = instance.name.title() + ' | ElectricBikeReview.com'
			instance.save()
		except:
			pass


post_save.connect(review_category_post_save, sender=ReviewCategory)
