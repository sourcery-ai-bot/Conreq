from django.apps import AppConfig
from django_idom.views import web_modules_file
from django_idom.websocket_consumer import IdomAsyncWebsocketConsumer
from idom.html import i

from conreq.app import register


class BaseConfig(AppConfig):
    name = "conreq.internal.base"

    def ready(self):
        # pylint: disable=import-outside-toplevel
        from django_idom.config import IDOM_WEB_MODULES_URL, IDOM_WEBSOCKET_URL

        register.websocket(IDOM_WEBSOCKET_URL + "<view_id>/")(
            IdomAsyncWebsocketConsumer
        )
        register.url(IDOM_WEB_MODULES_URL + "<path:file>")(web_modules_file)
        # TODO: Remove this later
        register.nav_group("User", i({"className": "fas fa-users icon-left"}))
        register.nav_tab("User", "Settings")(lambda X: None)
        register.nav_tab("User", "Sign Out")(lambda X: None)
        register.nav_group("Admin", i({"className": "fas fa-cogs icon-left"}))
        register.nav_tab("Admin", "Manage Users")(lambda X: None)
        register.nav_tab("Admin", "Server Config")(lambda X: None)
