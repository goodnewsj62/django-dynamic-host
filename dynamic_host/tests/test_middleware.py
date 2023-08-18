from django.http import HttpResponse
from django.test import TestCase, override_settings, RequestFactory
from django.contrib.sites.models import Site
from django.core.exceptions import DisallowedHost

from ..middleware import AllowedHostMiddleWare

# test allow all short circuit
# test if no options is set and no contrib.site
# test for when no options is set but contrib.sites is set
# test host_list site
# test for regisetered contrib.sites
# test for when call is false
# test for when call is true


def get_response_empty(request):
    return HttpResponse()


class BaseTestCase(TestCase):
    def setUp(self):
        super().setUp()
        # will be called for every test if test class inherit
        # this class
        self.factory = RequestFactory()


class AllowAllHostTestCase(BaseTestCase):
    @override_settings(
        DYNAMIC_HOST_ALLOW_ALL=True,
        DEBUG=False,
        DYNAMIC_HOST_DEFAULT_HOSTS=[],
        ALLOWED_HOSTS=[],
    )
    def test_allow_all_host_flag(self):
        request = RequestFactory(headers={"Host": "any.you.com"})
        request = request.get("/")
        resp = AllowedHostMiddleWare(get_response_empty)(request)
        self.assertIsInstance(resp, HttpResponse)


class DebugTrueTestCase(BaseTestCase):
    @override_settings(
        DEBUG=True,
        DYNAMIC_HOST_DEFAULT_HOSTS=[],
        ALLOWED_HOSTS=[],
    )
    def test_auto_adittion_of_localhost(self):
        factory = type(self.factory)
        request = factory(headers={"Host": "localhost"})
        request = request.get("/")
        resp = AllowedHostMiddleWare(get_response_empty)(request)
        self.assertIsInstance(resp, HttpResponse)

        request = factory(headers={"Host": "127.0.0.1"})
        request = request.get("/")
        resp = AllowedHostMiddleWare(get_response_empty)(request)
        self.assertIsInstance(resp, HttpResponse)

        request = factory(headers={"Host": "0.0.0.0"})
        request = request.get("/")
        resp = AllowedHostMiddleWare(get_response_empty)(request)
        self.assertIsInstance(resp, HttpResponse)


class DjangoSitesTestCase(BaseTestCase):
    @override_settings(
        DEBUG=False,
        DYNAMIC_HOST_DEFAULT_HOSTS=[],
        ALLOWED_HOSTS=[],
    )
    def test_allow_for_registered_sites(self):
        site = Site.objects.create(domain="web.site.com", name="site")
        request = RequestFactory(headers={"Host": site.domain})
        request = request.get("/")
        resp = AllowedHostMiddleWare(get_response_empty)(request)
        self.assertIsInstance(resp, HttpResponse)

        with self.assertRaises(DisallowedHost):
            request = RequestFactory(headers={"Host": "sudo.mydomain.com"})
            request = request.get("/")
            resp = AllowedHostMiddleWare(get_response_empty)(request)
            self.assertIsInstance(resp, HttpResponse)


class CallFunctionTestCase(BaseTestCase):
    @override_settings(
        DEBUG=False,
        DYNAMIC_HOST_DEFAULT_HOSTS=[],
        ALLOWED_HOSTS=[],
    )
    def test_validated_host_name(self):
        request = RequestFactory(headers={"Host": "example.com"})
        request = request.get("/")
        resp = AllowedHostMiddleWare(get_response_empty)(request)
        self.assertIsInstance(resp, HttpResponse)

        with self.assertRaises(DisallowedHost):
            request = RequestFactory(headers={"Host": "egg.example.com"})
            request = request.get("/")
            resp = AllowedHostMiddleWare(get_response_empty)(request)
            self.assertIsInstance(resp, HttpResponse)


class DefaultHostTestCase(BaseTestCase):
    @override_settings(
        DEBUG=False,
        DYNAMIC_HOST_DEFAULT_HOSTS=["dude.com"],
        ALLOWED_HOSTS=[],
    )
    def test_allow_host_in_host_default_setting(self):
        request = RequestFactory(headers={"Host": "dude.com"})
        request = request.get("/")
        resp = AllowedHostMiddleWare(get_response_empty)(request)
        self.assertIsInstance(resp, HttpResponse)

    @override_settings(
        DEBUG=False,
        DYNAMIC_HOST_DEFAULT_HOSTS=[],
        ALLOWED_HOSTS=["dude.com"],
    )
    def test_allow_host_in_allowedhosts_setting(self):
        request = RequestFactory(headers={"Host": "dude.com"})
        request = request.get("/")
        resp = AllowedHostMiddleWare(get_response_empty)(request)
        self.assertIsInstance(resp, HttpResponse)
