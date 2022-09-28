import re


def striphtml(data):
    p = re.compile(r'<.*?>')
    return p.sub('', data)


def review_dict(review):
    brand = review.brands.all().values('name', 'slug')[0]
    dict = {
            "@context": "http://schema.org/",
            "@type": "Review",
            "@id": "https://electricbikereview.com/"+brand['slug']+"/"+review.slug+"/#Review",
            "url": "https://electricbikereview.com/"+brand['slug']+"/"+review.slug+"/",
            "headline": review.name,
            "itemReviewed":
            {
                "@type": "Product",
                "name": review.name,
                "image": review.featured_image.url if review.featured_image else '',
                "description": striphtml(review.description)[:150],
                "model": review.model_name,
                "review":
                {
                    "@type": "Review",
                    "@id": "https://electricbikereview.com/"+brand['slug']+"/"+review.slug+"/#Review",
                    "name": review.name,
                    "url": "https://electricbikereview.com/"+brand['slug']+"/"+review.slug+"/"
                }
            },
            "author":
            {
                "@type": "Person",
                "@id": "https://electricbikereview.com/#Court",
                "name": "Court Rye",
                "url": "https://electricbikereview.com/",
                "affiliation":
                {
                    "@type": "Organization",
                    "@id": "https://electricbikereview.com/#Organization",
                    "name": "Electric Bike Review",
                    "url": "https://electricbikereview.com/"
                }

            },
            "contributor":
            {
                "@type": "Person",
                "@id": "https://electricbikereview.com/#Tyson",
                "name" : "Tyson Roehrkasse",
                "url": "https://twirltech.solutions/",
                "affiliation":
                {
                    "@type": "Organization",
                    "@id": "https://electricbikereview.com/#Organization",
                    "name": "Electric Bike Review",
                    "url": "https://electricbikereview.com/"
                }
            },
            "publisher":
            {
                "@type": "Organization",
                "@id": "https://electricbikereview.com/#Organization",
                "name": "Electric Bike Review",
                "url": "https://electricbikereview.com/"
            },
            "datePublished": review.publish_date.strftime("%b %d, %Y"),
            "sameAs": "https://electricbikereview.com/"+brand['slug']+"/"+review.slug+"/"
        }
    return dict
