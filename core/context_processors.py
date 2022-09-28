from django.conf import settings


def settings_context(_request):
    return {
        "PROJECT_TITLE": settings.PROJECT_TITLE,
        "COPYRIGHT": settings.COPYRIGHT,
        "META_URL": settings.META_URL
    }
