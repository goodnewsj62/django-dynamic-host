from django.conf import settings


class Settings:
    # DYNAMIC_HOST_ALLOW_ALL: bool = getattr(settings, "DYNAMIC_HOST_ALLOW_ALL", False)

    @property
    def DYNAMIC_HOST_DEFAULT_HOSTS(self) -> list:
        allowed_hosts = {*getattr(settings, "DYNAMIC_HOST_DEFAULT_HOSTS", [])}
        if settings.DEBUG:
            allowed_hosts = {
                *allowed_hosts,
                ".localhost",
                "127.0.0.1",
                "0.0.0.0",
                "[::1]",
            }

        return [*allowed_hosts]

    @property
    def DYNAMIC_HOST_ALLOW_SITES(self) -> bool:
        return getattr(settings, "DYNAMIC_HOST_ALLOW_SITES", False)

    @property
    def DYNAMIC_HOST_ALLOW_ALL(self) -> bool:
        return getattr(settings, "DYNAMIC_HOST_ALLOW_ALL", False)

    @property
    def DYNAMIC_HOST_RESOLVER_FUNC(self) -> str:
        return getattr(settings, "DYNAMIC_HOST_RESOLVER_FUNC", "")


conf = Settings()
