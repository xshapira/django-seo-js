import os
import tempfile
from django_seo_js import VERSION
from fabric.api import *

SITE_DIR = "site"
WHITELIST_DIRS = [".git", ]
WHITELIST_FILES = [".gitignore", ]

SANITY_CHECK_PROJECT_FILES = ["fabfile.py", "setup.py", "mkdocs.yml"]
SANITY_CHECK_BUILD_FILES = ["index.html", "js", "css"]


def _splitpath(path):
    path = os.path.normpath(path)
    return path.split(os.sep)


def tag_release():
    # Tag the release:
    local(f"git tag {VERSION}")
    local("git push --tags")


def upload_release():
    local("python setup.py sdist upload")


def release():
    # deploy_docs()
    upload_release()
    tag_release()


def deploy_docs():
    # For someday move to mkdocs.  Stolen verbatim from will.
    # Sanity check dir.
    root_dir = os.getcwd()
    assert all(
        os.path.exists(os.path.join(root_dir, f))
        for f in SANITY_CHECK_PROJECT_FILES
    )


    local(f"rm -rf {SITE_DIR}")
    local("mkdocs build")
    tempdir = tempfile.mkdtemp()

    local(f"mv {SITE_DIR}/* {tempdir}")

    current_branch = local("git rev-parse --abbrev-ref HEAD", capture=True)
    last_commit = local("git log -1 --pretty=\%B", capture=True)

    # Add the new site to build
    local("git checkout gh-pages")

    # Sanity check dir.
    root_dir = os.getcwd()
    assert all(
        os.path.exists(os.path.join(root_dir, f))
        for f in SANITY_CHECK_BUILD_FILES
    )


    for root, dirs, files in os.walk(root_dir, topdown=False):
        for name in files:
            if name not in WHITELIST_FILES and all(
                r not in WHITELIST_DIRS for r in _splitpath(root)
            ):
                # print "removing %s" % (os.path.join(root, name))
                os.remove(os.path.join(root, name))
        for name in dirs:
            if name not in WHITELIST_DIRS and all(
                r not in WHITELIST_DIRS for r in _splitpath(root)
            ):
                # print "removing %s" % (os.path.join(root, name))
                os.rmdir(os.path.join(root, name))

    local(f"cp -rv {tempdir}/* .")
    with settings(warn_only=True):
        result = local("git diff --exit-code")

        result = local("git diff --exit-code")

    if result.return_code != 0:
        local("git add -A .")
        local("git commit -m 'Auto-update of docs: %s'" % last_commit)
        local("git push")
    local(f"git checkout {current_branch}")
