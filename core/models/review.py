from django.db.models.signals import pre_save, post_save
from django.core.validators import MinValueValidator
from django.db import models
from . import User, ReviewCategory, ReviewBrand
from core.utils import review_slugify, resize_review_image
from ckeditor.fields import RichTextField
from .model_changes import ModelYear, BikeClass, FrameType, WheelSize, BreakType


PUBLISH_STATUS = (
	('Published', 'Published'),
	('Draft', 'Draft'),
)


class Review(models.Model):
	name = models.CharField(max_length=255)
	slug = models.SlugField(max_length=255, unique=True)
	meta_title = models.CharField(max_length=255, null=True, blank=True)
	description = RichTextField()
	status = models.CharField(max_length=50, choices=PUBLISH_STATUS, default='Draft')
	featured_image = models.ImageField(upload_to='review-featured-images/', null=True, blank=True)
	featured_image_web = models.ImageField(upload_to='review-featured-images-web/', null=True, blank=True)
	featured_image_thumbnail = models.ImageField(upload_to='review-featured-images-thumbnail/', null=True, blank=True)
	youtube_video = models.CharField(max_length=80)
	publish_date = models.DateField()

	model_name = models.CharField(max_length=150, null=True, blank=True)
	model_year = models.CharField(max_length=50, null=True, blank=True)
	demo_model_year = models.ManyToManyField(ModelYear, related_name='demo_model_year_changes', blank=True)
	trim = models.CharField(max_length=255, null=True, blank=True)

	categories = models.ManyToManyField(ReviewCategory, db_index=True, related_name='review_category')
	brands = models.ManyToManyField(ReviewBrand,  db_index=True,  related_name='review_brand')

	more_details = RichTextField(null=True, blank=True)

	create_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
	create_at = models.DateTimeField(auto_now_add=True)
	update_at = models.DateTimeField(auto_now=True)

	def __str__(self):
		return str(self.name)

	def get_absolute_url(self):
		return f"/{self.brands.all()[0].slug}/{self.slug}/"
		# return reverse("core:review-list")

	def save(self, *args, **kwargs):
		if self.featured_image:
			self.featured_image_web = resize_review_image(self.featured_image, (860, 570))
			self.featured_image_thumbnail = resize_review_image(self.featured_image, (430, 285))
		super().save(*args, *kwargs)

	class Meta:
		db_table = "review"
		verbose_name = "Review"
		verbose_name_plural = "Reviews"
		indexes = [
			models.Index(fields=['id']),
			models.Index(fields=['name']),
			models.Index(fields=['slug']),
		]


# Here we are use signal for create slug.
def review_pre_save(sender, instance, *args, **kwargs):
	"""
		Pre save signal use for review slug generate.
	"""
	# print('pre_save')
	model_year_list = instance.model_year.split(',')
	year = model_year_list[0].strip() if len(model_year_list) == 0 else model_year_list[-1].strip()

	if instance.slug is None or instance.slug == '':
		new_slug = f"{year} {instance.model_name.title()} {instance.trim.title()}"
		review_slugify(instance, save=False, new_slug=new_slug)
	else:
		review_slugify(instance, save=False, new_slug=instance.slug)
	if instance.meta_title is None or instance.meta_title == '':
		try:
			if instance.trim:
				instance.meta_title = f"{year} {instance.brands.all()[0].slug.title()} {instance.model_name.title()} {instance.trim.title()} Review | ElectricBikeReview.com"
			else:
				instance.meta_title = f"{year} {instance.brands.all()[0].slug.title()} {instance.model_name.title()} Review | ElectricBikeReview.com"
			instance.save()
		except:
			pass


pre_save.connect(review_pre_save, sender=Review)


def review_post_save(sender, instance, created, *args, **kwargs):
	"""
		Post save signal use for review slug generate.
	"""
	# print('post_save')
	model_year_list = instance.model_year.split(',')
	year = model_year_list[0].strip() if len(model_year_list) == 0 else model_year_list[-1].strip()
	if created:
		if instance.slug is None:
			new_slug = f"{year} {instance.model_name.title()} {instance.trim.title()}"
			review_slugify(instance, save=False, new_slug=new_slug)
		else:
			review_slugify(instance, save=False, new_slug=instance.slug)
	else:
		if instance.slug is None:
			new_slug = f"{year} {instance.model_name.title()} {instance.trim.title()}"
			review_slugify(instance, save=False, new_slug=new_slug)
		else:
			review_slugify(instance, save=False, new_slug=instance.slug)
	if instance.meta_title is None or instance.meta_title == '':
		try:
			if instance.trim:
				instance.meta_title = f"{year} {instance.brands.all()[0].slug.title()} {instance.model_name.title()} {instance.trim.title()} Review | ElectricBikeReview.com"
			else:
				instance.meta_title = f"{year} {instance.brands.all()[0].slug.title()} {instance.model_name.title()} Review | ElectricBikeReview.com"
			instance.save()
		except:
			pass


post_save.connect(review_post_save, sender=Review)


class ReviewHighlights(models.Model):
	highlight = models.TextField()
	review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name='review_highlight')
	create_at = models.DateTimeField(auto_now_add=True)
	update_at = models.DateTimeField(auto_now=True)

	class Meta:
		db_table = "review_highlight"
		verbose_name = "Review Highlight"
		verbose_name_plural = "Review Highlights"


class UpVoteReviewHighlights(models.Model):
	review_highlight_id = models.ForeignKey(ReviewHighlights, on_delete=models.CASCADE)
	ip = models.CharField(max_length=50, null=False, blank=False)
	create_at = models.DateTimeField(auto_now_add=True)
	update_at = models.DateTimeField(auto_now=True)

	class Meta:
		db_table = "upvote_review_highlight"
		verbose_name = "upvote_review_highlight"
		verbose_name_plural = "upvote_review_highlights"
		indexes = [
			models.Index(fields=['id']),
			models.Index(fields=['ip']),
		]


class ReviewGeneral(models.Model):
	msrp = models.FloatField(validators=[MinValueValidator(0.0)])
	bike_class = models.CharField(max_length=255, null=True, blank=True)
	demo_bike_class = models.ManyToManyField(BikeClass, db_index=True, related_name='demo_bike_class_changes', blank=True)
	frame_type = models.CharField(max_length=255, null=True, blank=True)
	demo_frame_type = models.ManyToManyField(FrameType, db_index=True, related_name='demo_frame_type_changes', blank=True)
	suspension = models.CharField(max_length=255, null=True, blank=True)
	wheel_size = models.CharField(max_length=255, null=True, blank=True)
	demo_wheel_size = models.ManyToManyField(WheelSize, db_index=True, related_name='demo_wheel_size_changes', blank=True)
	gears = models.CharField(max_length=255, null=True, blank=True)
	demo_gear = models.IntegerField(null=True, blank=True)		# demo gear ----------------------------
	brake_type = models.CharField(max_length=255, null=True, blank=True)
	demo_brake_type = models.ManyToManyField(BreakType, db_index=True, related_name='demo_brake_type_changes', blank=True)
	motor_type = models.CharField(max_length=255, null=True, blank=True)
	motor_nominal_output = models.CharField(max_length=255, null=True, blank=True)
	demo_motor_nominal_output = models.IntegerField(null=True, blank=True) 		# demo_motor_nominal_output ---------------------------
	battery_watt_hours = models.CharField(max_length=255, null=True, blank=True)
	demo_battery_watt_hours = models.FloatField(null=True, blank=True)		# demo_battery_watt_hours --------------------------------
	weight = models.CharField(max_length=255, null=True, blank=True)
	demo_weight = models.FloatField(null=True, blank=True)		# demo_weight ---------------------------------------

	review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name='review_general_review')
	create_at = models.DateTimeField(auto_now_add=True)
	update_at = models.DateTimeField(auto_now=True)

	class Meta:
		db_table = "review_general"
		verbose_name = "Review General"
		verbose_name_plural = "Review Generals"


class ReviewFrameset(models.Model):
	frameset_frame_type = models.CharField(max_length=255, null=True, blank=True)
	demo_frameset_frame_type = models.ManyToManyField(FrameType, db_index=True, related_name='demo_frameset_frame_type_changes', blank=True)
	frameset_weight = models.CharField(max_length=255, null=True, blank=True)
	demo_frameset_weight = models.FloatField(null=True, blank=True)		# demo_frameset_weight ---------------------------------
	load_capacity = models.CharField(max_length=255, null=True, blank=True)
	frameset_suspension = models.CharField(max_length=255, null=True, blank=True)
	suspension_travel = models.CharField(max_length=255, null=True, blank=True)
	demo_suspension_travel = models.IntegerField(null=True, blank=True)		# demo_suspension_travel ----------------------------
	fork = models.CharField(max_length=255, null=True, blank=True)
	rear_shock = models.CharField(max_length=255, null=True, blank=True)
	frameset_wheel_size = models.CharField(max_length=255, null=True, blank=True)
	demo_frameset_wheel_size = models.ManyToManyField(WheelSize, db_index=True, related_name='demo_frameset_wheel_size_changes', blank=True)
	front_wheel = models.CharField(max_length=255, null=True, blank=True)
	rear_wheel = models.CharField(max_length=255, null=True, blank=True)
	front_hub = models.CharField(max_length=255, null=True, blank=True)
	rear_hub = models.CharField(max_length=255, null=True, blank=True)
	tires = models.CharField(max_length=255, null=True, blank=True)

	review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name='review_frameset_review')
	create_at = models.DateTimeField(auto_now_add=True)
	update_at = models.DateTimeField(auto_now=True)

	class Meta:
		db_table = "review_frameset"
		verbose_name = "Review Frameset"
		verbose_name_plural = "Review Frameset"


class ReviewDrivetrain(models.Model):
	drivetrain_gears = models.CharField(max_length=255, null=True, blank=True)
	demo_drivetrain_gears = models.IntegerField(null=True, blank=True)		# demo_drivetrain_gears ----------------------------------------
	shift_levers = models.CharField(max_length=255, null=True, blank=True)
	front_derailleur = models.CharField(max_length=255, null=True, blank=True)
	crankset = models.CharField(max_length=255, null=True, blank=True)
	rear_derailleur = models.CharField(max_length=255, null=True, blank=True)
	electronic_shifting = models.CharField(max_length=255, null=True, blank=True)
	internally_geared_hub = models.CharField(max_length=255, null=True, blank=True)
	continually_variable_transmission = models.CharField(max_length=255, null=True, blank=True)
	cassette = models.CharField(max_length=255, null=True, blank=True)
	chainring = models.CharField(max_length=255, null=True, blank=True)
	belt_drive = models.CharField(max_length=255, null=True, blank=True)

	review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name='review_drivetrain_review')
	create_at = models.DateTimeField(auto_now_add=True)
	update_at = models.DateTimeField(auto_now=True)

	class Meta:
		db_table = "review_drivetrain"
		verbose_name = "Review Drivetrain"
		verbose_name_plural = "Review Drivetrains"


class ReviewComponents(models.Model):
	headset = models.CharField(max_length=255, null=True, blank=True)
	stem = models.CharField(max_length=255, null=True, blank=True)
	handlebar = models.CharField(max_length=255, null=True, blank=True)
	grips = models.CharField(max_length=255, null=True, blank=True)
	seatpost = models.CharField(max_length=255, null=True, blank=True)
	seatpost_diameter = models.CharField(max_length=255, null=True, blank=True)
	demo_seatpost_diameter = models.FloatField(null=True, blank=True)		# demo_seatpost_diameter ------------------------------
	saddle = models.CharField(max_length=255, null=True, blank=True)
	pedals = models.CharField(max_length=255, null=True, blank=True)
	components_brake_type = models.CharField(max_length=255, null=True, blank=True)
	demo_components_brake_type = models.ManyToManyField(BreakType, db_index=True, related_name='demo_components_brake_type_changes', blank=True)
	front_brake = models.CharField(max_length=255, null=True, blank=True)
	rear_brake = models.CharField(max_length=255, null=True, blank=True)

	review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name='review_components_review')
	create_at = models.DateTimeField(auto_now_add=True)
	update_at = models.DateTimeField(auto_now=True)

	class Meta:
		db_table = "review_components"
		verbose_name = "Review Component"
		verbose_name_plural = "Review Components"


class ReviewEbikeSystems(models.Model):
	systems_bike_class = models.CharField(max_length=255, null=True, blank=True)
	demo_systems_bike_class = models.ManyToManyField(BikeClass, db_index=True, related_name='demo_systems_bike_class_changes', blank=True)
	systems_motor_type = models.CharField(max_length=255, null=True, blank=True)
	motor = models.CharField(max_length=255, null=True, blank=True)
	additional_motors = models.CharField(max_length=255, null=True, blank=True)
	systems_motor_nominal_output = models.CharField(max_length=255, null=True, blank=True)
	demo_systems_motor_nominal_output = models.IntegerField(null=True, blank=True) 		 # demo_systems_motor_nominal_output -----------------------------
	display = models.CharField(max_length=255, null=True, blank=True)
	smart_bike = models.CharField(max_length=255, null=True, blank=True)
	theft_gps = models.CharField(max_length=255, null=True, blank=True)
	systems_battery_watt_hours = models.CharField(max_length=255, null=True, blank=True)
	demo_systems_battery_watt_hours = models.FloatField(null=True, blank=True)		# demo_systems_battery_watt_hours ---------------------------
	battery = models.CharField(max_length=255, null=True, blank=True)
	additional_battery = models.CharField(max_length=255, null=True, blank=True)
	charger = models.CharField(max_length=255, null=True, blank=True)

	review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name='review_ebike_systems_review')
	create_at = models.DateTimeField(auto_now_add=True)
	update_at = models.DateTimeField(auto_now=True)

	class Meta:
		db_table = "review_ebike_systems"
		verbose_name = "Review Ebike System"
		verbose_name_plural = "Review Ebike Systems"


class ReviewAccessories(models.Model):
	lights = models.CharField(max_length=255, null=True, blank=True)
	fenders = models.CharField(max_length=255, null=True, blank=True)
	front_rack = models.CharField(max_length=255, null=True, blank=True)
	rear_rack = models.CharField(max_length=255, null=True, blank=True)

	review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name='review_accessory_review')
	create_at = models.DateTimeField(auto_now_add=True)
	update_at = models.DateTimeField(auto_now=True)

	class Meta:
		db_table = "review_accessory"
		verbose_name = "Review 	Accessory"
		verbose_name_plural = "Review Accessories"


class ReviewGalley(models.Model):
	image = models.ForeignKey("core.ImageGallery", on_delete=models.CASCADE)
	order = models.IntegerField()
	review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name='review_galley_review')

	class Meta:
		db_table = "review_galley"
		verbose_name = "Review Galley"
		verbose_name_plural = "Review Galleys"
