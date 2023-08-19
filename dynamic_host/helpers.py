import importlib
from django.http.request import split_domain_port, validate_host
from django.conf import settings


def import_func(full_func_path: str):
    try:
        function_string = full_func_path
        mod_name, func_name = function_string.rsplit(".", 1)
        mod = importlib.import_module(mod_name)
        func = getattr(mod, func_name)
        return func
    except Exception as e:
        return None


def get_django_domain_sites():
    if "django.contrib.sites" in settings.INSTALLED_APPS:
        from django.contrib.sites.models import Site

        return Site.objects.all().iterator()
    return []


def is_a_registered_site(host: str) -> bool:
    """ "
    check if any registered site domain matches origin
    """

    raw_sites = get_django_domain_sites()
    domains = [split_domain_port(site.domain) for site in raw_sites]
    return any(split_domain_port(host)[0] == domain[0] for domain in domains)


def is_in_host_list(host: str, host_list: list) -> bool:
    return validate_host(split_domain_port(host)[0], host_list)
