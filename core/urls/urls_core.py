from django.urls import path
from .. import views

app_name = "core"

urlpatterns = [
	path("", views.IndexView.as_view(), name="index"),

	# User Module
	path("users/<int:pk>/update/", views.UserUpdateView.as_view(), name="user-update"),
	path("users/<int:pk>/password/", views.UserPasswordView.as_view(), name="user-password"),

	# Review Category Module
	path("review-category/", views.ReviewCategoryListView.as_view(), name="reviewcategory-list"),
	path("review-category/<int:pk>/details/", views.ReviewCategoryDetailView.as_view(), name="reviewcategory-detailview"),
	path("review-category/create/", views.ReviewCategoryCreateView.as_view(), name="reviewcategory-create"),
	path("review-category/<int:pk>/update/", views.ReviewCategoryUpdateView.as_view(), name="reviewcategory-update"),
	path("review-category/<int:pk>/delete/", views.ReviewCategoryDeleteView.as_view(), name="reviewcategory-delete"),
	path("ajax-review-category", views.ReviewCategoryAjaxPagination.as_view(), name="reviewcategory-list-ajax"),

	# Review Brand Module
	path("review-brand/", views.ReviewBrandListView.as_view(), name="reviewbrand-list"),
	path("review-brand/create/", views.ReviewBrandCreateView.as_view(), name="reviewbrand-create"),
	path("review-brand/<int:pk>/update/", views.ReviewBrandUpdateView.as_view(), name="reviewbrand-update"),
	path("review-brand/<int:pk>/delete/", views.ReviewBrandDeleteView.as_view(), name="reviewbrand-delete"),
	path("ajax-review-brand", views.ReviewBrandAjaxPagination.as_view(), name="reviewbrand-list-ajax"),

	# Review Module
	path("review/", views.ReviewListView.as_view(), name="review-list"),
	path("review/create/", views.ReviewCreateView.as_view(), name="review-create"),
	path("review/<int:pk>/update/", views.ReviewUpdateView.as_view(), name="review-update"),
	path("review/<int:pk>/delete/", views.ReviewDeleteView.as_view(), name="review-delete"),
	path("ajax-review", views.ReviewAjaxPagination.as_view(), name="review-list-ajax"),

	# Image gallery
	path("get-image-gallery", views.get_image_gallery, name="get_image_gallery"),
	path("upload-image-gallery", views.upload_image_gallery, name="upload_image_gallery"),
	path("gallery-image-details", views.gallery_image_details, name="gallery_image_details"),
	path("gallery-image-delete", views.gallery_image_delete, name="gallery_image_delete"),
	path("gallery-image-edit", views.gallery_image_edit, name="gallery_image_edit"),
	path("review-slug/check", views.review_slug_check, name="review_slug_check"),

	# Pages Module
	path("pages/", views.PagesListView.as_view(), name="pages-list"),
	path("pages/create/", views.PagesCreateView.as_view(), name="pages-create"),
	path("pages/<int:pk>/update/", views.PagesUpdateView.as_view(), name="pages-update"),
	path("pages/<int:pk>/delete/", views.PagesDeleteView.as_view(), name="pages-delete"),
	path("ajax-pages", views.PagesAjaxPagination.as_view(), name="pages-list-ajax"),

	# Menus Module
	path("menus/", views.MenusListView.as_view(), name="menus-list"),
	path("menus/create/", views.MenusCreateView.as_view(), name="menus-create"),
	path("menus/<int:pk>/update/", views.MenusUpdateView.as_view(), name="menus-update"),
	path("menus/<int:pk>/delete/", views.MenusDeleteView.as_view(), name="menus-delete"),
	path("ajax-menus", views.MenusAjaxPagination.as_view(), name="menus-list-ajax"),

	# TrustedAccessories Module
	# path("trusted-accessories/", views.TrustedAccessoriesListView.as_view(), name="trustedaccessories-list"),
	# path("trusted-accessories/create/", views.TrustedAccessoriesCreateView.as_view(), name="trustedaccessories-create"),
	# path("trusted-accessories/<int:pk>/update/", views.TrustedAccessoriesUpdateView.as_view(), name="trustedaccessories-update"),
	# path("trusted-accessories/<int:pk>/delete/", views.TrustedAccessoriesDeleteView.as_view(), name="trustedaccessories-delete"),
	# path("ajax-trusted-accessories", views.TrustedAccessoriesAjaxPagination.as_view(), name="trustedaccessories-list-ajax"),

	# Comment Module
	path("comments/", views.CommentsListView.as_view(), name="comments-list"),
	path("comments/create/", views.CommentsCreateView.as_view(), name="comments-create"),
	path("comments/<int:pk>/update/", views.CommentsUpdateView.as_view(), name="comments-update"),
	path("comments/<int:pk>/delete/", views.CommentsDeleteView.as_view(), name="comments-delete"),
	path("ajax-comments", views.CommentsAjaxPagination.as_view(), name="comments-list-ajax"),

	# Comment Action Module
	path("comments/approve_disapprove", views.approve_disapprove_comment, name="approve_disapprove_comment"),
	path("comments/spam_unspam", views.spam_unspam_comment, name="spam_unspam_comment"),
	path("comments/empty_spam", views.empty_spam_comment, name="empty_spam_comment"),
	path("unsubscribe/<int:pk>/", views.unsubscribe_comment, name="unsubscribe-comments"),

]
