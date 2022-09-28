from django.urls import path
from . import views

app_name = "frontend"


urlpatterns = [
	# Extra API for EBR.
	path('dashboard-integration/shops-nearby/', views.shops_nearby, name='shops_nearby'),
	path('dashboard-integration/shops-osm/', views.shops_osm, name='shops_osm'),
	path('ar/brands/', views.brand_json, name='brand_json'),
	path('wp-json/dashboard/brands/', views.dashboard_brands, name='dashboard_brands'),
	path('visitor_history/', views.visitor_history, name='visitor_history'),

	path('', views.index, name='dashboard'),
	path('category/', views.category, name='category'),
	path('category/<str:cat_slug>/', views.category_detail, name='category_detail'),
	path('search_filter/', views.search_filter, name='search-filter'),
	path('price-range/', views.price_range_filter, name='price-range-filter'),
	path('more-filter/', views.more_filter, name='more-filter'),
 
	path('display-comments/', views.display_comments, name='display-comments'),
	path('display-sub-comments/', views.display_sub_comments, name='display-sub-comments'),
 
	path('search/', views.category_filter, name='search-reviews'),

	path('category-count-ajax/', views.category_count_ajax, name='category-count-ajax' ),

	path('brand/', views.brand, name='brand'),
	path('brand/<str:brand_slug>/', views.brand_details, name='brand_details'),
	path('review_seo', views.review_seo, name='review_seo'),
 
 	path('send-message/', views.send_message, name='send_message'),
 	# path('send-message/<str:page_slug>/', views.send_message, name='send_message'),

	path('<str:brand_slug>/<str:slug>/', views.review_detail, name='review-detail'),
	path('add-new-comment/', views.add_new_comment, name='add-new-comment'),
	# path('add-new-comment/<str:brand_slug>/<str:slug>/', views.add_new_comment, name='add-new-comment'),
	path('compare/', views.compare, name='compare'),
 
 	# path('contact/', views.contact_us, name='contact'),
	# path('upvote-to-comment/', views.upvote_to_comment, name='upvote-to-comment'),

	path('highlights/update_vote', views.highlights_update_vote, name='highlights_update_vote'),
	path('highlights/get', views.get_review_highlights, name='get_review_highlights'),

	# path('<str:brand>/<str:slug>/', views.review_page, name='review'),
	path('<str:page_slug>/', views.page_view, name='page_view'),
	path('add_datas/<int:pk>', views.add_fields, name='add_datas'),
]
