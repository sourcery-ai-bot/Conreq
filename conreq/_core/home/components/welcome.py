from django_idom.components import django_css
from idom import component, hooks, html

from conreq import config
from conreq.types import HomepageStateContext


@component
def welcome():
    state = hooks.use_context(HomepageStateContext)

    async def on_click(_):
        # pylint: disable=protected-access
        state.viewport_intent = config._homepage.admin_sidebar_tabs[1].viewport
        state.set_state(state)

    return html.div(
        django_css("conreq/welcome.css"),
        html.h1("Welcome to Conreq"),
        html.p("Looks like you don't have any custom tabs yet."),
        html.p("Head over to the App Store and install some!"),
        html.button(
            "Go to App Store ",
            html.i(class_name="fas fa-arrow-right"),
            class_name="btn btn-primary",
            on_click=on_click,
        ),
        class_name="welcome",
    )
