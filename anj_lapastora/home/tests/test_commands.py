import io
from unittest import mock

from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.test import TestCase

from home.models import HomePage
from wagtail.models import Site

User = get_user_model()


def run_bootstrap():
    call_command("bootstrap_site", stdout=io.StringIO())


class BootstrapSiteCommandTests(TestCase):
    def test_creates_homepage_and_updates_default_site(self):
        run_bootstrap()

        self.assertEqual(HomePage.objects.count(), 1)
        homepage = HomePage.objects.first()
        self.assertEqual(homepage.title, "Home")

        site = Site.objects.get(is_default_site=True)
        self.assertEqual(site.root_page_id, homepage.id)

    def test_is_idempotent(self):
        run_bootstrap()
        run_bootstrap()

        self.assertEqual(HomePage.objects.count(), 1)
        self.assertEqual(Site.objects.filter(is_default_site=True).count(), 1)

    def test_uses_domain_env_var_for_site_hostname(self):
        with mock.patch.dict("os.environ", {"DOMAIN": "example.com"}):
            run_bootstrap()

        site = Site.objects.get(is_default_site=True)
        self.assertEqual(site.hostname, "example.com")

    def test_creates_superuser_when_env_vars_present(self):
        env = {
            "DJANGO_SUPERUSER_USERNAME": "admin",
            "DJANGO_SUPERUSER_EMAIL": "admin@example.com",
            "DJANGO_SUPERUSER_PASSWORD": "supersecret",
        }
        with mock.patch.dict("os.environ", env):
            run_bootstrap()

        user = User.objects.get(username="admin")
        self.assertTrue(user.is_superuser)
        self.assertEqual(user.email, "admin@example.com")

    def test_skips_superuser_creation_when_env_vars_missing(self):
        run_bootstrap()

        self.assertEqual(User.objects.count(), 0)

    def test_does_not_duplicate_superuser_on_second_run(self):
        env = {
            "DJANGO_SUPERUSER_USERNAME": "admin",
            "DJANGO_SUPERUSER_EMAIL": "admin@example.com",
            "DJANGO_SUPERUSER_PASSWORD": "supersecret",
        }
        with mock.patch.dict("os.environ", env):
            run_bootstrap()
            run_bootstrap()

        self.assertEqual(User.objects.filter(username="admin").count(), 1)
