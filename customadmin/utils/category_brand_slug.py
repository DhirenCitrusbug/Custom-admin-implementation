from django.utils.text import slugify


def category_brand_slugify(instance, save=False, new_slug=None):
    if new_slug is not None:
        slug = slugify(new_slug)
    else:
        slug = slugify(instance.name)
    Klass = instance.__class__
    qs = Klass.objects.filter(slug=slug).exclude(id=instance.id)
    if qs.exists():
        # auto generate new slug
        slug = f"{slug}-{qs.count()}"
        return category_brand_slugify(instance, save=save, new_slug=slug)
    instance.slug = slug
    if save:
        instance.save()
    return instance


def pages_slugify(instance, save=False, new_slug=None):
    if new_slug is not None:
        slug = slugify(new_slug)
    else:
        slug = slugify(instance.page_title)
    Klass = instance.__class__
    qs = Klass.objects.filter(slug=slug).exclude(id=instance.id)
    if qs.exists():
        # auto generate new slug
        slug = f"{slug}-{qs.count()}"
        return pages_slugify(instance, save=save, new_slug=slug)
    instance.slug = slug
    if save:
        instance.save()
    return instance
