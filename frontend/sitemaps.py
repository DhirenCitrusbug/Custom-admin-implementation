from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from core.models import Review, ReviewCategory, ReviewBrand, Pages
from datetime import datetime


class StaticViewSitemap(Sitemap):
    changefreq = "Weekly"
    priority = 0.6

    def items(self):
        print("###################")
        return [
            'frontend:dashboard',
            'frontend:category',
            'frontend:brand',
            'frontend:compare',

        ]

    def location(self, item):
        return reverse(item)

    def lastmod(self, obj):
        return None


class ReviewCategorySitemap(Sitemap):
    changefreq = "Weekly"
    priority = 0.6

    def items(self):
        print("-------------------------")
        return ReviewCategory.objects.filter(status='Published').order_by('-id')

    def lastmod(self, obj):
        print(obj.update_at)
        return obj.update_at


class ReviewBrandSitemap(Sitemap):
    changefreq = "Weekly"
    priority = 0.6

    def items(self):
        print("-------------------------")
        return ReviewBrand.objects.filter(status='Published').order_by('-id')

    def lastmod(self, obj):
        return obj.update_at


class ReviewSitemap(Sitemap):
    changefreq = "Weekly"
    priority = 0.6

    def items(self):
        print("-------------------------")
        return Review.objects.filter(status='Published').order_by('-id')

    def lastmod(self, obj):
        return obj.update_at


class PagesSitemap(Sitemap):
    changefreq = "Weekly"
    priority = 0.6

    def items(self):
        print("-------------------------")
        return Pages.objects.filter(status='Published').order_by('-id')

    def lastmod(self, obj):
        return obj.update_at
