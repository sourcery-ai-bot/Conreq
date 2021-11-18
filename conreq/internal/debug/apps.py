from django.apps import AppConfig
from django.contrib import admin
from django.urls import include

from conreq.app import register
from conreq.utils.environment import get_debug


DEBUG = get_debug()

# pylint: disable=import-outside-toplevel
class DebugConfig(AppConfig):
    name = "conreq.internal.debug"

    def ready(self) -> None:
        if not DEBUG:
            return

        performance_profiling()
        admin_panel()
        password_reset()
        api_docs()


def performance_profiling():
    register.url("silk/")(include("silk.urls", namespace="silk"))


def admin_panel():
    register.url("admin/docs/")(include("django.contrib.admindocs.urls"))
    register.url("admin/")(admin.site.urls)


def password_reset():
    from django.contrib.auth import views as auth_views

    register.url("password_reset/", name="password_reset_done")(
        auth_views.PasswordResetView
    )
    register.url("password_reset/done/", name="password_reset_done")(
        auth_views.PasswordResetDoneView
    )
    register.url("reset/<uidb64>/<token>/", name="password_reset_confirm")(
        auth_views.PasswordResetConfirmView
    )
    register.url("reset/done/", name="password_reset_complete")(
        auth_views.PasswordResetCompleteView
    )


def api_docs():
    from drf_yasg import openapi
    from drf_yasg.views import get_schema_view
    from rest_framework import permissions

    # Django Rest Framework documentation (Swagger and Redoc)
    SchemaView = get_schema_view(
        openapi.Info(
            title="Conreq API Endpoints",
            default_version="v1",
            description="""
            This page contains a lost of all endpoints available within this Conreq instance.

            Endpoints require an API key either in **HTTP Header (Authorization: Api-Key)** or in the **URL Parameter (apikey)**.

            Token Authentication is performed using **HTTP Header (Authorization: Token)**. Session Authentication can alternatively be performed.
            """,
            contact=openapi.Contact(email="archiethemonger@gmail.com"),
            license=openapi.License(name="GPL-3.0 License"),
        ),
        public=True,
        permission_classes=[permissions.AllowAny],
    )

    register.url(
        r"^swagger(?P<format>\.json|\.yaml)$", name="schema-json", use_regex=True
    )(SchemaView.without_ui(cache_timeout=0))
    register.url(r"^swagger/$", name="schema-swagger-ui", use_regex=True)(
        SchemaView.with_ui("swagger", cache_timeout=0)
    )
