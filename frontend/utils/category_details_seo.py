import re
from django.conf import settings
from .brand_details_seo import brand_details_schema
from core.models import ReviewHighlights, Comments


def striphtml(data):
    p = re.compile(r'<.*?>')
    return p.sub('', data)


def review_schema(category, review):
    host_url = settings.SCHEMA_URL
    qry_review_highlight = ReviewHighlights.objects.filter(review=review)
    qry_comments_count = Comments.objects.filter(comment_type='Review', comment_type_id=review.id, is_approved=True).count()
    brand = review.brands.all()[0] if review.brands.all() else None
    dict = {
            "@context": "https://schema.org/",
            "@type": "Product",
            "name": review.name,
            "image": settings.AWS_IMAGE_URL + str(review.featured_image) if review.featured_image else '',
            "description": "The "+review.model_name+" is an electric bike manufactured by "+brand.name,
            "brand": {
               "@type": "Brand",
               "@id": "{}/brand/{}/#Brand".format(host_url, brand.slug),
               "name": brand.name,
               "url": "{}/brand/{}/".format(host_url, brand.slug),
               "logo": settings.AWS_IMAGE_URL+str(brand.brand_image_full) if brand.brand_image_full else '',
               "description": brand.description
            },
            "model": review.name,
            "review": {
               "@type": "Review",
               "@id": "{}/{}/{}/#Review".format(host_url, brand.slug, review.slug),
               "name": review.name,
               "url": "{}/{}/{}/".format(host_url, brand.slug, review.slug),
               "headline": review.name,
               "reviewBody": ".".join([rh.highlight for rh in qry_review_highlight]),
               "video": "https://youtube.com/watch?v={}".format(review.youtube_video),
               "commentCount": str(qry_comments_count),
               "author": {
                  "@type": "Person",
                  "@id": "https://electricbikereview.com/#Court",
                  "name": "Court Rye",
                  "url": "https://electricbikereview.com/",
                  "affiliation":{
                     "@type": "Organization",
                     "@id": "https://electricbikereview.com/#Organization",
                     "name": "Electric Bike Review",
                     "url": "https://electricbikereview.com/"
                  }
               },
               "contributor": {
                  "@type": "Person",
                  "@id": "https://electricbikereview.com/#Tyson",
                  "name": "Tyson Roehrkasse",
                  "url": "https://twirltech.solutions/",
                  "affiliation": {
                     "@type": "Organization",
                     "@id": "https://electricbikereview.com/#Organization",
                     "name": "Electric Bike Review",
                     "url": "https://electricbikereview.com/"
                  }
               },
               "publisher": {
                  "@type": "Organization",
                  "@id": "https://electricbikereview.com/#Organization",
                  "name": "Electric Bike Review",
                  "url": "https://electricbikereview.com/"
               },
               "datePublished": review.publish_date.strftime("%b %d, %Y"),
               "sameAs": "{}/{}/{}/".format(host_url, brand.slug, review.slug),
            }
         }
    return dict


def category_details_schema(category, featured_reviews, reviews):
    host_url = settings.SCHEMA_URL

    brand_details_dict = {
       "@context": "http://schema.org",
       "@type": "CollectionPage",
       "@id": "{}/{}/#WebPage".format(host_url, category.slug),
       "mainEntity": {
          "@type": "ItemList",
          "itemListElement": []
       },
       "isPartOf": {
          "@type": "WebSite",
          "@id": "{}/#WebSite".format(host_url),
          "name": "ElectricBikeReview.com",
          "url": host_url
       },
       "name": category.name,
       "about": category.name,
       "description": category.name,
       "publisher": {
          "@type": "Organization",
          "@id": "{}/#Organization".format(host_url),
          "name": "Electric Bike Review",
          "url": host_url
       },
       "breadcrumb": {
          "@type": "BreadcrumbList",
          "itemListElement": [
             {
                "@type": "ListItem",
                "position": 1,
                "item": {
                   "@id": host_url,
                   "name": "Home",
                   "url": host_url
                }
             },
             {
                "@type": "ListItem",
                "position": 2,
                "item": {
                   "@id": "https://electricbikereview.com/category/bikes/",
                   "name": "Reviews",
                   "url": "https://electricbikereview.com/category/bikes/"
                }
             },
             {
                "@type": "ListItem",
                "position": 3,
                "item": {
                   "@id": "https://electricbikereview.com/category/{}/".format(category.slug),
                   "name": category.name,
                   "url": "https://electricbikereview.com/category/{}/".format(category.slug)
                }
             }
          ]
       }
    }
    itemListElement = []
    if featured_reviews is not None:
        for review in featured_reviews:
            itemListElement.append(review_schema(category, review))
    for review in reviews:
        itemListElement.append(review_schema(category, review))

    brand_details_dict['mainEntity']['itemListElement'] = itemListElement
    print(brand_details_dict)
    return brand_details_dict