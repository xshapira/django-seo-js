#! /usr/bin/env python
import os
from setuptools import setup, find_packages
from django_seo_js import VERSION

ROOT_DIR = os.path.dirname(__file__)
SOURCE_DIR = os.path.join(ROOT_DIR)


reqs = []
with open("requirements.txt", "r+") as f:
    reqs.extend(line.strip() for line in f)
test_reqs = []
with open("requirements.tests.txt", "r+") as f:
    test_reqs.extend(line.strip() for line in f)
try:
    import pypandoc
    long_description = pypandoc.convert('README.md', 'rst')
except (IOError, ImportError):
    long_description = ''

setup(
    name="django-seo-js",
    description="SEO support for angular, backbone, "
                "ember, famo.us, and other SPA apps "
                "built with django.",
    long_description=long_description,
    author="Steven Skoczen",
    author_email="steven@greenkahuna.com",
    url="https://github.com/skoczen/django-seo-js",
    version=VERSION,
    install_requires=reqs,
    tests_require=test_reqs,
    packages=find_packages(),
    include_package_data=True,
    keywords=["seo", "django", "ajax", "angular", "backbone",
              "ember", "famous", "google", "bing", "yahoo"],
    classifiers=[
        "Programming Language :: Python",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],

)
