from setuptools import find_packages, setup

setup(
    name = "Voltaire",
    version = "alpha 0.0.1"
    packages = find_packages(),
    include_package_data = True,
    install_requires = [
    "flask",
    "google-api-python-client",
    ],
)