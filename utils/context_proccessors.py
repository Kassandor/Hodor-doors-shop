from django.conf import settings


def sitename(request):
    """
    SITE_NAME в контексте шаблонов
    """
    return {
        'sitename': settings.SITE_NAME,
    }
