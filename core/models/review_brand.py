from django.db.models.signals import pre_save, post_save
from django.db import models
from .users import User
from core.utils import category_brand_slugify, resize_image

PUBLISH_STATUS = (
	('Published', 'Published'),
	('Draft', 'Draft'),
)


class ReviewBrand(models.Model):
	name = models.CharField(max_length=255)
	slug = models.SlugField(max_length=255, unique=True)
	meta_title = models.CharField(max_length=255, null=True, blank=True)
	description = models.TextField()
	short_description = models.TextField()
	brand_image_full = models.ImageField(upload_to='brand-images/', null=True, blank=True)
	brand_image_web = models.ImageField(upload_to='brand-web-images/', null=True, blank=True)
	brand_image_mobile = models.ImageField(upload_to='brand-mobile-images/', null=True, blank=True)

	brand_image_grayscale_full = models.ImageField(upload_to='brand-grayscale-images/', null=True, blank=True)
	brand_image_grayscale_web = models.ImageField(upload_to='brand-web-grayscale-images/', null=True, blank=True)
	brand_image_grayscale_mobile = models.ImageField(upload_to='brand-mobile-grayscale-images/', null=True, blank=True)

	brand_image_darkmode_full = models.ImageField(upload_to='brand-darkmode-images/', null=True, blank=True)
	brand_image_darkmode_web = models.ImageField(upload_to='brand-web-darkmode-images/', null=True, blank=True)
	brand_image_darkmode_mobile = models.ImageField(upload_to='brand-mobile-darkmode-images/', null=True, blank=True)

	parent_brand = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)
	status = models.CharField(max_length=50, choices=PUBLISH_STATUS, default='Draft')
	featured_review = models.CharField(max_length=100, null=True, blank=True)
	create_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
	create_at = models.DateTimeField(auto_now_add=True)
	update_at = models.DateTimeField(auto_now=True)

	def __str__(self):
		return str(self.name)

	def save(self, *args, **kwargs):
		if self.brand_image_full:
			self.brand_image_web = resize_image(self.brand_image_full, (432, 239))
			self.brand_image_mobile = resize_image(self.brand_image_full, (97, 52))

		if self.brand_image_grayscale_full:
			self.brand_image_grayscale_web = resize_image(self.brand_image_grayscale_full, (432, 239))
			self.brand_image_grayscale_mobile = resize_image(self.brand_image_grayscale_full, (97, 52))

		if self.brand_image_darkmode_full:
			self.brand_image_darkmode_web = resize_image(self.brand_image_darkmode_full, (432, 239))
			self.brand_image_darkmode_mobile = resize_image(self.brand_image_darkmode_full, (97, 52))
		super().save(*args, *kwargs)

	def get_absolute_url(self):
		return f'/brand/{self.slug}/'

	class Meta:
		db_table = "review_brand"
		verbose_name = "Review brand"
		verbose_name_plural = "Review brands"
		indexes = [
			models.Index(fields=['id']),
			models.Index(fields=['name']),
			models.Index(fields=['slug']),
		]


# Here we are use signal for create slug.
def review_brand_pre_save(sender, instance, *args, **kwargs):
	"""
		Pre save signal use for review brand slug generate.
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


pre_save.connect(review_brand_pre_save, sender=ReviewBrand)


def review_brand_post_save(sender, instance, created, *args, **kwargs):
	"""
		Post save signal use for review brand slug generate.
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


post_save.connect(review_brand_post_save, sender=ReviewBrand)
