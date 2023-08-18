DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
    }
}

INSTALLED_APPS = [
    "django.contrib.contenttypes",
    "django.contrib.sites",
    "django_dyanmic_hosts",
]

DYNAMIC_HOST_RESOLVER_FUNC = "middleware.tests.test_resolver.resolver_func"

DEBUG = True

SITE_ID = 1

SECRET_KEY = "hdkkdurenrkrjruuren"

USE_TZ = True
