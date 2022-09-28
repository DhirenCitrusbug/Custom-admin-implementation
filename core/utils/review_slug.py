from django.utils.text import slugify


def review_slugify(instance, save=False, new_slug=None):
    if new_slug is not None:
        slug = slugify(new_slug)
    else:
        slug = slugify(instance.name)
    Klass = instance.__class__
    qs = Klass.objects.filter(slug=slug).exclude(id=instance.id)
    if qs.exists():
        # auto generate new slug
        slug = f"{slug}-{qs.count()}"
        return review_slugify(instance, save=save, new_slug=slug)
    instance.slug = slug
    if save:
        instance.save()
    return instance


def review_view_slugify(model, instance=None, new_slug=None):
    slug = slugify(new_slug)
    qs = model.objects.filter(slug=slug).exclude(id=instance)
    if qs.exists():
        # auto generate new slug
        slug = f"{slug}-{qs.count()}"
        return review_view_slugify(model, new_slug=slug)
    return slug
