from uuid import uuid4

from django_idom.components import static_css
from idom import component, hooks
from idom.html import _, a, button, div, h4, h5, li, ol, p

from conreq import config
from conreq._core.app_store.models import Category, Subcategory
from conreq._core.utils import tab_constructor


class PlaceholderApp:
    uuid = 0
    name = "My App Name"
    short_description = "This is a placeholder description. This will be removed in the future. Please pay no attention to this text. But what if the text gets too long? Who knows what will happen, but I can probably guess that it'll be great! Or maybe it won't be, only time will tell."
    author = "Author"
    version = "0.0.0"
    category = "Category"


@component
def app_store(websocket, state, set_state):
    # pylint: disable=unused-argument
    tab, set_tab = hooks.use_state(None)
    categories = hooks.use_state(get_categories)[0]
    ready, set_ready = hooks.use_state(False)

    @hooks.use_effect
    async def lag():
        if not ready:
            from random import randint
            from time import sleep

            sleep(randint(1, 3))
            set_ready(True)

    # TODO: Update app store entries every first load
    return _(
        static_css("conreq/app_store.css"),
        static_css("conreq/buttons.css"),
        tab(key=tab.__name__)
        if tab
        else div(
            {"className": "spotlight-region"},
            recently_added(set_tab),
            recently_updated(set_tab),
            most_popular(set_tab),
            top_downloaded(set_tab),
            our_favorites(set_tab),
            essentials(set_tab),
            random_selection(set_tab),
            key="spotlight-region",
        ),
        div({"className": "nav-region"}, nav_constructor(categories, set_tab)),
    )


def get_categories():
    query = Subcategory.objects.select_related("category").order_by("name").all()
    categories = {}
    for subcategory in query:
        categories.setdefault(subcategory.category, []).append(subcategory)
    return categories


def nav_constructor(categories: dict[Category, list[Subcategory]], set_tab) -> list:
    return [
        div(
            {"className": "nav-item"},
            a(
                {
                    "href": f"#{category.uuid}",
                    "onClick": lambda x: print("clicked"),
                },
                h5({"className": "nav-title"}, category.name),
            ),
            ol(
                {"className": "nav-sub"},
                [
                    li(
                        {"className": "nav-sub-item"},
                        a(
                            {
                                "className": "nav-sub-link",
                                "href": f"#{subcategory.uuid}",
                                "onClick": lambda x: print("clicked"),
                            },
                            subcategory.name,
                        ),
                        key=str(subcategory.uuid),
                    )
                    for subcategory in value
                ],
            ),
            key=str(category.uuid),
        )
        for category, value in categories.items()
    ]


def recently_added(set_tab):
    return spotlight("Recently Added", "The latest from our community.", set_tab)


def recently_updated(set_tab):
    return spotlight(
        "Recently Updated", "Actively maintained for all to enjoy.", set_tab
    )


def most_popular(set_tab):
    return spotlight(
        "Most Popular", "These have gained a serious amount lot of love.", set_tab
    )


def top_downloaded(set_tab):
    return spotlight("Top Downloaded", "Tons of downloads!", set_tab)


def our_favorites(set_tab):
    return spotlight("Our Favorites", "A curated list of our favorites.", set_tab)


def essentials(set_tab):
    return spotlight(
        "Essentials", "Something we think all users should consider.", set_tab
    )


def random_selection(set_tab):
    return spotlight("Random Selection", "Are you feeling lucky today?", set_tab)


def spotlight(title, description, set_tab, apps=None):
    return div(
        {"className": "spotlight"},
        a(
            {"href": "#", "onClick": lambda x: print("clicked")},
            h4({"className": "title"}, title),
            p({"className": "description"}, description),
        ),
        div(
            {"className": "card-stage"},
            [card(set_tab) for _ in range(8)],
        ),
    )


def card(set_tab, app: PlaceholderApp = PlaceholderApp()):
    return div(
        {"className": "card"},
        div(
            {"className": "top"},
            div(
                {"className": "text-region"},
                h5(
                    {"className": "card-title"},
                    a(
                        {"href": f"#{app.uuid}", "onClick": lambda x: print("clicked")},
                        app.name,
                    ),
                ),
                div(
                    {"className": "card-author"},
                    a(
                        {"href": "#", "onClick": lambda x: print("clicked")},
                        app.author,
                    ),
                ),
                div(
                    {"className": "card-category"},
                    a(
                        {"href": "#", "onClick": lambda x: print("clicked")},
                        app.category,
                    ),
                ),
            ),
            div({"className": "image"}),
        ),
        div(
            {"className": "btn-container"},
            button(
                {
                    "className": "btn btn-sm btn-secondary",
                    "onClick": lambda x: print("clicked"),
                },
                "Details",
            ),
            button(
                {
                    "className": "btn btn-sm btn-primary",
                    "onClick": lambda x: print("clicked"),
                },
                "Install",
            ),
        ),
        div({"className": "description"}, app.short_description),
        key=str(uuid4()),
    )


# pylint: disable=protected-access
config._homepage.admin_nav_tabs[1] = tab_constructor(
    "App Store", app_store, html_class="app-store"
)
