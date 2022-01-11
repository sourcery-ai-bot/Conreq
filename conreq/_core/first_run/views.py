from django.contrib.auth import authenticate, login
from django.shortcuts import redirect, render

from conreq._core.first_run.forms import InitializationForm
from conreq._core.first_run.models import Initialization

INITIALIZED = False


def initialize(request):
    # pylint: disable=global-statement
    # Check cached value if we've already initialized
    global INITIALIZED
    if INITIALIZED:
        return None

    # Run the first time initialization if needed
    initialization = Initialization.get_solo()
    if initialization.initialized:
        INITIALIZED = True
        return None

    # User submitted the first time setup form
    if request.method == "POST":
        form = InitializationForm(request.POST)

        # Create the superuser and set up the database if the form is valid
        if form.is_valid():
            return _first_run_setup(form, request, initialization)

        # Form data wasn't valid, so return the error codes
        return render(
            request, "conreq/registration/initialization.html", {"form": form}
        )

    # User needs to fill out the first time setup
    return render(request, "conreq/registration/initialization.html")


def _first_run_setup(form, request, initialization):
    form.save()
    username = form.cleaned_data.get("username")
    password = form.cleaned_data.get("password1")
    user = authenticate(username=username, password=password)
    user.is_staff = True
    user.is_admin = True
    user.is_superuser = True
    user.save()
    login(request, user)
    initialization.initialized = True
    initialization.save()
    return redirect("landing")
