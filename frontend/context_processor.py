from core.models import Menus, ReviewCategory, Review, TrustedAccessories, ModelYear
from django.db.models import Q

from core.models.comment import UpVote
from .views import float_to_value
import requests
import json


def footer_links(request):
	qry_footer_menu = Menus.objects.filter(menu_location='footer_links', parent_menu=None).order_by('order')

	qry_best_electric_bikes = Menus.objects.filter(menu_location='best_electric_bikes', parent_menu=None).order_by('order')

	qry_popular_brands = Menus.objects.filter(menu_location='popular_brands', parent_menu=None).order_by('order')

	qry_popular_categories = Menus.objects.filter(menu_location='popular_categories', parent_menu=None).order_by('order')

	qry_popular_searches = Menus.objects.filter(menu_location='popular_searches', parent_menu=None).order_by('order')

	qry_popular_topics = Menus.objects.filter(menu_location='popular_topics', parent_menu=None).order_by('order')

	qry_main_menu = Menus.objects.filter(menu_location='main_menu', parent_menu=None).order_by('order').values('id', 'name', 'link')
	main_menus = qry_main_menu
	for main_menu in main_menus:
		qry_main_menu_child = Menus.objects.filter(menu_location='main_menu', parent_menu=main_menu['id']).order_by('order')
		main_menu['child_menus'] = qry_main_menu_child

	# qry_bike_category = ReviewCategory.objects.filter(parent_category=None, status='Published').order_by('id').values('id', 'name', 'slug', 'short_description', 'icon_image')

	# for bike_category in qry_bike_category:
	# 	qry_parent_review_count = Review.objects.filter(Q(categories=bike_category['id']) | Q(categories__parent_category=bike_category['id'])).count()
	# 	bike_category['total_review'] = float_to_value(qry_parent_review_count)

	qry_review = Review.objects.all().count()

	qry_trusted = TrustedAccessories.objects.filter(status='Published')

	context = {
		'main_menus': main_menus,
		'best_electric_bikes': qry_best_electric_bikes,
		'popular_brands': qry_popular_brands,
		'popular_categories': qry_popular_categories,
		'popular_searches': qry_popular_searches,
		'popular_topics': qry_popular_topics,
		'footer_menus': qry_footer_menu,
		'trusted': qry_trusted,
		# 'categories': qry_bike_category,
		'total_review': qry_review,
	}

	return context


def navbar_data(request):

	qry_bike_category = ReviewCategory.objects.filter(parent_category=None, status='Published').order_by('id').values('id', 'name', 'slug', 'short_description', 'icon_image')

	for bike_category in qry_bike_category:
		qry_parent_review_count = Review.objects.filter(Q(categories=bike_category['id']) & Q(categories__parent_category=None)).distinct('id').count()
		bike_category['total_review'] = float_to_value(qry_parent_review_count)
	
	compare_review_ids = [int(i) for i in request.COOKIES.get('id', '').split('%2C') if i != '']

	qry_bike_review = Review.objects.all().order_by('-id')
	qry_hub_motors = qry_bike_review.filter(review_general_review__motor_type = 'Hub')
	qry_mid_drive_motors = qry_bike_review.filter(review_general_review__motor_type = 'Mid-Drive')
	qry_class_1 = qry_bike_review.filter(review_general_review__bike_class__contains = 'Class 1')
	qry_class_2 = qry_bike_review.filter(review_general_review__bike_class__contains = 'Class 2')
	qry_class_3 = qry_bike_review.filter(review_general_review__bike_class__contains = 'Class 3')
	qry_class_other = qry_bike_review.filter(review_general_review__bike_class__contains = 'Other')
	qry_suspension_rigid = qry_bike_review.filter(review_general_review__suspension = 'None')
	qry_suspension_hardtail = qry_bike_review.filter(review_general_review__suspension = 'Front Suspension')
	qry_suspension_softail = qry_bike_review.filter(review_general_review__suspension = 'Rear Suspension')
	qry_suspension_full_suspension = qry_bike_review.filter(review_general_review__suspension = 'Full Suspension')
	qry_accessories_lights = qry_bike_review.filter(review_accessory_review__lights = 'Yes')
	qry_accessories_fenders = qry_bike_review.filter(review_accessory_review__fenders = 'Yes')
	qry_accessories_rack = qry_bike_review.filter(Q(review_accessory_review__front_rack = 'Yes') | Q(review_accessory_review__rear_rack = 'Yes'))
	min_model_year = min(list(ModelYear.objects.all().order_by('year').values_list('year', flat=True)))
	max_model_year = max(list(ModelYear.objects.all().order_by('year').values_list('year', flat=True)))

	qry_review_model_year = []
	for year in range(min_model_year, max_model_year+1):
		qry_review_model_year.append(year)

	context = {
		'bike_categories': qry_bike_category,
		'bike_reviews': qry_bike_review,
		'hub_motors': qry_hub_motors,
		'mid_drive_motors': qry_mid_drive_motors,
		'review_class_1': qry_class_1,
		'review_class_2': qry_class_2,
		'review_class_3': qry_class_3,
		'review_class_other': qry_class_other,
		'suspension_rigid':qry_suspension_rigid,
		'suspension_hardtail':qry_suspension_hardtail,
		'suspension_softail':qry_suspension_softail,
		'suspension_full_suspension':qry_suspension_full_suspension,
		'accessories_lights':qry_accessories_lights,
		'accessories_fenders':qry_accessories_fenders,
		'accessories_rack':qry_accessories_rack,
		'review_year_range':qry_review_model_year,
		'compare_review':compare_review_ids,
	}

	return context