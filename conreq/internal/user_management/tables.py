from django.contrib.auth import get_user_model
from django_tables2 import Table, TemplateColumn


class UsersTable(Table):
    edit = TemplateColumn(
        template_name="conreq/user_management/edit_btn.html",
        orderable=False,
    )

    class Meta:
        model = get_user_model()
        # TODO: PR a template for Bootstrap 5
        template_name = "django_tables2/bootstrap-responsive.html"
        fields = (
            "username",
            "email",
            "date_joined",
            "last_login",
            "is_staff",
            "edit",
        )
        order_by = "date_joined"
