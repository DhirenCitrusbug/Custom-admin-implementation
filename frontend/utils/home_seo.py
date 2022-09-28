def home_seo():
    home_seo_dict = {
        "@context": "http://schema.org",
        "@type": "WebSite",
        "@id": "https://electricbikereview.com/#WebSite",
        "name": "ElectricBikeReview.com",
        "url": "https://electricbikereview.com/",
        "about":
        {
            "@type": "Thing",
            "description": "Electric Bike Reviews - Prices, Specs, Videos, Photos"
        },
        "publisher":
        {
            "@type": "Organization",
            "@id": "https://electricbikereview.com/#Organization",
            "name": "Electric Bike Review",
            "url": "https://electricbikereview.com/"
        },
        "sameAs": ["https://www.facebook.com/ElectricBikeReview",
                "https://twitter.com/ebikereview"],
        "potentialAction":
        {
            "@type": "SearchAction",
            "target": "https://electricbikereview.com/?s={search_term}",
            "query-input": "required name=search_term"
        }
    }
    return home_seo_dict
