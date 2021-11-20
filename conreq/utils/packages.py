import functools
import logging
import os
import pkgutil

_logger = logging.getLogger(__name__)


@functools.cache
def _packages_dir():
    """Load the packages dir from a different context to avoid circular imports."""
    # pylint: disable=import-outside-toplevel
    from conreq import settings

    return getattr(settings, "PACKAGES_DIR")


@functools.cache
def _packages_dev_dir():
    """Load the dev packages dir from a different context to not cause exceptions on startup."""
    # pylint: disable=import-outside-toplevel
    from conreq import settings

    return getattr(settings, "PACKAGES_DEV_DIR")


def _duplicate_package_check(packages: set, packages_dev: set):
    seen = packages.intersection(packages_dev)

    for package in seen:
        _logger.warning(
            "\033[93mDuplicate package detected '%s'.\033[0m",
            package,
        )


def find_modules(folder_path: str, prefix: str = "") -> set[str]:
    """Returns all modules in a path"""
    return {name for _, name, _ in pkgutil.iter_modules([folder_path], prefix=prefix)}


def find_modules_with(
    folder_path: str, submodule_name: str, prefix: str = ""
) -> set[str]:
    """Returns a tuple of all modules containing module name and an importable path to 'example.module.urls'"""
    modules = find_modules(folder_path)
    modules_with = set()

    for module in modules:
        submodules = os.path.join(folder_path, module)
        if submodule_name in find_modules(submodules):
            modules_with.add(prefix + module)

    return modules_with


def find_packages() -> set[str]:
    """Returns all Conreq packages."""
    packages = find_modules(_packages_dir())
    packages_dev = find_modules(_packages_dev_dir())
    _duplicate_package_check(packages, packages_dev)
    return packages | packages_dev


def find_apps() -> set[str]:
    """Returns all Conreq apps within packages."""
    apps = set()
    user_packages = find_packages()

    for package in user_packages:
        apps_dir = os.path.join(_packages_dir(), package, "apps")
        apps_dev_dir = os.path.join(_packages_dev_dir(), package, "apps")
        all_modules = find_modules(apps_dir) | find_modules(apps_dev_dir)
        for app in all_modules:
            apps.add(f"{package}.apps.{app}")

    return apps


def find_apps_with(module_name: str) -> set[str]:
    """Returns all Conreq apps that contain a specific module name."""
    apps_with = set()
    apps = find_apps()

    for app in apps:
        package, apps_dir, app_name = app.split(".")
        apps_dir = os.path.join(_packages_dir(), package, apps_dir, app_name)
        apps_dev_dir = os.path.join(_packages_dev_dir(), package, apps_dir, app_name)
        all_modules = find_modules(apps_dir) + find_modules(apps_dev_dir)
        for module in all_modules:
            if module == module_name:
                apps_with.add(app)

    return apps_with
