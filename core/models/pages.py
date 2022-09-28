from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
from . import User, Review, ReviewCategory, ReviewBrand
from django.db.models.signals import pre_save, post_save
from core.utils import pages_slugify
from .model_changes import BikeClass

PUBLISH_STATUS = (
	('Published', 'Published'),
	('Draft', 'Draft'),
)

BOOL_CHOICES = ((True, 'Basic Search Filter'), (False, 'Advanced Search Filter'))


class Pages(models.Model):
	page_title = models.CharField(max_length=255)
	slug = models.SlugField(max_length=255, unique=True)
	meta_title = models.CharField(max_length=255)
	description = RichTextUploadingField()
	is_filter = models.BooleanField(default=False)
	search_text = models.CharField(max_length=255, null=True, blank=True)
	status = models.CharField(max_length=50, choices=PUBLISH_STATUS, default='Draft')

	filter_type = models.BooleanField(choices=BOOL_CHOICES, default='True')

	model_name = models.CharField(max_length=200, blank=True, null=True)
	trim = models.CharField(max_length=200, blank=True, null=True)
	min_year = models.CharField(max_length=20, blank=True, null=True)
	max_year = models.CharField(max_length=20, blank=True, null=True)
	brands = models.ManyToManyField(ReviewBrand, db_index=True, related_name='pages_brand', blank=True)
	categories = models.ManyToManyField(ReviewCategory, db_index=True, related_name='pages_category', blank=True)
	min_price = models.IntegerField(default=0, blank=True, null=True)
	max_price = models.IntegerField(default=0, blank=True, null=True)
	suspension = models.CharField(max_length=255, blank=True, null=True)
	motor_type = models.CharField(max_length=255, blank=True, null=True)
	min_battery_capacity = models.IntegerField(default=0, blank=True, null=True)
	max_battery_capacity = models.IntegerField(default=0, blank=True, null=True)
	min_weight = models.IntegerField(default=0, blank=True, null=True)
	max_weight = models.IntegerField(default=0, blank=True, null=True)
	bike_class = models.CharField(max_length=255, null=True, blank=True)
	demo_page_bike_class = models.ManyToManyField(BikeClass, db_index=True, related_name='demo_page_bike_class_changes', blank=True)
	accessories = models.CharField(max_length=255, null=True, blank=True)
	keyword = models.CharField(max_length=255, null=True, blank=True)

	create_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
	create_at = models.DateTimeField(auto_now_add=True)
	update_at = models.DateTimeField(auto_now=True)

	def __str__(self):
		return str(self.page_title)

	def get_absolute_url(self):
		return f"/{self.slug}/"

	class Meta:
		db_table = "pages"
		verbose_name = "Page"
		verbose_name_plural = "Pages"
		indexes = [
			models.Index(fields=['id']),
			models.Index(fields=['slug']),
		]


# Here we are use signal for create slug.
def review_category_pre_save(sender, instance, *args, **kwargs):
	"""
		Pre save signal use for review category slug generate.
	"""
	# print('pre_save')
	if instance.slug is None or instance.slug == '':
		pages_slugify(instance, save=False)
	else:
		pages_slugify(instance, save=False, new_slug=instance.slug)
	if instance.meta_title is None or instance.meta_title == '':
		try:
			instance.meta_title = instance.page_title.title() + ' | ElectricBikeReview.com'
			instance.save()
		except:
			pass


pre_save.connect(review_category_pre_save, sender=Pages)


def review_category_post_save(sender, instance, created, *args, **kwargs):
	"""
		Post save signal use for review category slug generate.
	"""
	# print('post_save')
	if created:
		if instance.slug is None:
			pages_slugify(instance, save=False)
		else:
			pages_slugify(instance, save=False, new_slug=instance.slug)
	if instance.meta_title is None or instance.meta_title == '':
		try:
			instance.meta_title = instance.page_title.title() + ' | ElectricBikeReview.com'
			instance.save()
		except:
			pass


post_save.connect(review_category_post_save, sender=Pages)
