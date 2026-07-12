"""Shared helpers for building a Wagtail page tree in tests."""
from wagtail.images.models import Image
from wagtail.images.tests.utils import get_test_image_file
from wagtail.models import Page, Site

from home.models import (
    AboutPage,
    AtelierPage,
    HomePage,
    MusingsPage,
    MusingsPostPage,
    PhotoPage,
    TechPage,
    TechPostPage,
)


def make_test_image(title="test.png"):
    return Image.objects.create(title=title, file=get_test_image_file())


def build_page_tree():
    """Create Home > (About, Musings, Tech, Atelier) and point the default Site at it.

    Returns a dict of the created page instances for use in tests.
    """
    root = Page.get_first_root_node()

    # A fresh Wagtail install seeds a demo page ("Welcome to your new
    # Wagtail site!") at slug "home" under root, which would otherwise
    # collide with our own homepage's slug.
    root.get_children().filter(slug="home").delete()
    root.refresh_from_db()

    home = HomePage(title="Home", slug="home")
    root.add_child(instance=home)
    home.save_revision().publish()

    about = AboutPage(title="About", slug="about")
    home.add_child(instance=about)
    about.save_revision().publish()

    musings = MusingsPage(title="Musings", slug="musings")
    home.add_child(instance=musings)
    musings.save_revision().publish()

    tech = TechPage(title="Tech", slug="tech")
    home.add_child(instance=tech)
    tech.save_revision().publish()

    atelier = AtelierPage(title="Atelier", slug="atelier")
    home.add_child(instance=atelier)
    atelier.save_revision().publish()

    # Deleting the demo page above cascades to its Site row, so the
    # default site may or may not still exist at this point.
    site, _ = Site.objects.update_or_create(
        is_default_site=True,
        defaults={"hostname": "testserver", "root_page": home},
    )

    return {
        "root": root,
        "home": home,
        "about": about,
        "musings": musings,
        "tech": tech,
        "atelier": atelier,
        "site": site,
    }


def add_musings_post(musings, title, slug, post_date, body="Body text.", live=True, main_image=None):
    post = MusingsPostPage(
        title=title,
        slug=slug,
        date=post_date,
        body=body,
        main_image=main_image,
        live=live,
    )
    musings.add_child(instance=post)
    if live:
        post.save_revision().publish()
    return post


def add_tech_post(tech, title, slug, post_date, body="Body text.", live=True, main_image=None):
    post = TechPostPage(
        title=title,
        slug=slug,
        date=post_date,
        body=body,
        main_image=main_image,
        live=live,
    )
    tech.add_child(instance=post)
    if live:
        post.save_revision().publish()
    return post


def add_photo(atelier, title, slug, caption="", photo=None, live=True):
    photo_page = PhotoPage(
        title=title,
        slug=slug,
        photo=photo or make_test_image(title=f"{slug}.png"),
        caption=caption,
        live=live,
    )
    atelier.add_child(instance=photo_page)
    if live:
        photo_page.save_revision().publish()
    return photo_page
