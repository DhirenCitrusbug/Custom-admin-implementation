from django.db import models
from . import User

MAIN_MENU = (
	('main_menu', 'Main Menu'),
	('best_electric_bikes', 'Best Electric Bikes'),
	('popular_brands', 'Popular Brands'),
	('popular_categories', 'Popular Categories'),
	('popular_searches', 'Popular Searches'),
	('popular_topics', 'Popular Topics'),
	('footer_links', 'Footer Links'),
)


class Menus(models.Model):
	name = models.CharField(max_length=255)
	link = models.CharField(max_length=255)
	menu_location = models.CharField(max_length=255, choices=MAIN_MENU, default='main_menu')
	order = models.IntegerField()
	parent_menu = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)

	create_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
	create_at = models.DateTimeField(auto_now_add=True)
	update_at = models.DateTimeField(auto_now=True)

	def __str__(self):
		return str(self.name)

	# def get_absolute_url(self):
	# 	return f"{self.slug}"
	# 	# return reverse("core:review-list")

	class Meta:
		db_table = "menus"
		verbose_name = "Menu"
		verbose_name_plural = "Menus"
		indexes = [
			models.Index(fields=['id']),
			models.Index(fields=['name', 'order']),
		]
