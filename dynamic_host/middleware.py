from django.http import HttpResponse, HttpRequest
from django.core.exceptions import DisallowedHost

from .helpers import (
    import_func,
    is_a_registered_site,
    is_in_host_list
)
from .conf import conf


class AllowedHostMiddleWare:
    """
    Checks if the incoming host(e.g example.com) is part of the listed known
    host or  passes check  as a green(good to go) host by user defined function

    NOTE: calling check function/is_a_registered_site should be the last resort in the conditional as it may
    trigger database read action which may not be necessay when the domain is listed in allowed_hosts.
    """

    def __init__(self, get_response) -> None:
        self.get_response = get_response

    def __call__(self, request) -> HttpResponse:
        host = request._get_raw_host()

        if conf.DYNAMIC_HOST_ALLOW_ALL:
            return self.get_response(request)

        check_func = import_func(conf.DYNAMIC_HOST_RESOLVER_FUNC)

        if (
            not check_func
            and not conf.DYNAMIC_HOST_ALLOW_SITES
            and not conf.DYNAMIC_HOST_DEFAULT_HOSTS
        ):
            raise DisallowedHost(f"Invalid HTTP_HOST header {host}")

        if not (
            is_in_host_list(host, conf.DYNAMIC_HOST_DEFAULT_HOSTS)
            or is_a_registered_site(host)
            or (check_func(host, request) if check_func else False)
        ):
            raise DisallowedHost(f"Invalid HTTP_HOST header {host}")
        else:
            return self.get_response(request)
