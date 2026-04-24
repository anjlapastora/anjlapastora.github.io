from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from wagtail.models import Page, Site
import os

from home.models import HomePage  # adjust if your app name differs


class Command(BaseCommand):
    help = "Bootstrap initial Wagtail site (homepage, site config, superuser)"

    def handle(self, *args, **options):
        self.stdout.write("Starting bootstrap...")

        # -------------------------
        # 1. Ensure homepage exists
        # -------------------------
        root = Page.get_first_root_node()
        homepage = HomePage.objects.live().first()

        if not homepage:
            self.stdout.write("Creating homepage...")

            homepage = HomePage(
                title="Home",
                slug="home",
            )
            root.add_child(instance=homepage)
            homepage.save_revision().publish()

        else:
            self.stdout.write("Homepage already exists.")

        # -------------------------
        # 2. Ensure Site is configured
        # -------------------------
        hostname = os.environ.get("DOMAIN", "localhost")

        site = Site.objects.first()

        if not site:
            self.stdout.write("Creating site configuration...")

            Site.objects.create(
                hostname=hostname,
                root_page=homepage,
                is_default_site=True,
            )
        else:
            self.stdout.write("Updating existing site...")

            site.hostname = hostname
            site.root_page = homepage
            site.save()

        # -------------------------
        # 3. Ensure superuser exists
        # -------------------------
        User = get_user_model()

        username = os.environ.get("DJANGO_SUPERUSER_USERNAME")
        email = os.environ.get("DJANGO_SUPERUSER_EMAIL")
        password = os.environ.get("DJANGO_SUPERUSER_PASSWORD")

        if username and password:
            if not User.objects.filter(username=username).exists():
                self.stdout.write("Creating superuser...")

                User.objects.create_superuser(
                    username=username,
                    email=email,
                    password=password,
                )
            else:
                self.stdout.write("Superuser already exists.")
        else:
            self.stdout.write("Superuser env vars not set. Skipping.")

        self.stdout.write(self.style.SUCCESS("Bootstrap complete."))
