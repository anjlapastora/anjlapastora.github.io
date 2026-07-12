import datetime

from django.test import RequestFactory, TestCase
from django.utils import timezone

from home.models import PhotoPage

from .factories import add_musings_post, add_photo, add_tech_post, build_page_tree

factory = RequestFactory()


class HomePageContextTests(TestCase):
    def setUp(self):
        self.pages = build_page_tree()

    def test_sections_are_live_children_of_home(self):
        context = self.pages["home"].get_context(factory.get("/"))
        section_titles = {page.title for page in context["sections"]}
        self.assertEqual(section_titles, {"About", "Musings", "Tech", "Atelier"})

    def test_recent_posts_combines_tech_and_musings_sorted_by_date(self):
        add_musings_post(
            self.pages["musings"], "Musings A", "musings-a", datetime.date(2024, 1, 1)
        )
        add_tech_post(self.pages["tech"], "Tech A", "tech-a", datetime.date(2024, 1, 2))
        add_musings_post(
            self.pages["musings"], "Musings B", "musings-b", datetime.date(2024, 1, 3)
        )
        add_tech_post(self.pages["tech"], "Tech B", "tech-b", datetime.date(2024, 1, 4))
        add_tech_post(self.pages["tech"], "Tech C", "tech-c", datetime.date(2024, 1, 5))

        context = self.pages["home"].get_context(factory.get("/"))
        titles = [post.title for post in context["recent_posts"]]

        self.assertEqual(titles, ["Tech C", "Tech B", "Musings B"])

    def test_recent_posts_excludes_unpublished_posts(self):
        add_tech_post(
            self.pages["tech"],
            "Draft Post",
            "draft-post",
            datetime.date(2099, 1, 1),
            live=False,
        )
        add_musings_post(
            self.pages["musings"], "Live Post", "live-post", datetime.date(2020, 1, 1)
        )

        context = self.pages["home"].get_context(factory.get("/"))
        titles = [post.title for post in context["recent_posts"]]

        self.assertNotIn("Draft Post", titles)
        self.assertIn("Live Post", titles)

    def test_recent_photos_returns_up_to_four_most_recent_live_photos(self):
        now = timezone.now()
        photos = [
            add_photo(self.pages["atelier"], f"Photo {i}", f"photo-{i}")
            for i in range(5)
        ]
        # Force a deterministic, strictly increasing publish order.
        for offset, photo in enumerate(photos):
            PhotoPage.objects.filter(pk=photo.pk).update(
                first_published_at=now - datetime.timedelta(days=(5 - offset))
            )

        context = self.pages["home"].get_context(factory.get("/"))
        titles = [photo.title for photo in context["recent_photos"]]

        self.assertEqual(titles, ["Photo 4", "Photo 3", "Photo 2", "Photo 1"])

    def test_recent_photos_excludes_unpublished_photos(self):
        add_photo(self.pages["atelier"], "Draft Photo", "draft-photo", live=False)
        add_photo(self.pages["atelier"], "Live Photo", "live-photo")

        context = self.pages["home"].get_context(factory.get("/"))
        titles = [photo.title for photo in context["recent_photos"]]

        self.assertNotIn("Draft Photo", titles)
        self.assertIn("Live Photo", titles)


class MusingsPageTests(TestCase):
    def setUp(self):
        self.pages = build_page_tree()

    def test_get_posts_orders_by_date_descending_and_excludes_drafts(self):
        add_musings_post(
            self.pages["musings"], "Older", "older", datetime.date(2024, 1, 1)
        )
        add_musings_post(
            self.pages["musings"], "Newer", "newer", datetime.date(2024, 2, 1)
        )
        add_musings_post(
            self.pages["musings"],
            "Draft",
            "draft",
            datetime.date(2024, 3, 1),
            live=False,
        )

        posts = list(self.pages["musings"].get_posts())

        self.assertEqual([post.title for post in posts], ["Newer", "Older"])

    def test_get_context_paginates_four_per_page(self):
        for i in range(6):
            add_musings_post(
                self.pages["musings"],
                f"Post {i}",
                f"post-{i}",
                datetime.date(2024, 1, i + 1),
            )

        context = self.pages["musings"].get_context(factory.get("/musings/"))

        self.assertEqual(len(context["posts"]), 4)
        self.assertEqual(context["posts"].paginator.num_pages, 2)

    def test_get_context_falls_back_to_first_page_for_non_integer_page(self):
        for i in range(6):
            add_musings_post(
                self.pages["musings"],
                f"Post {i}",
                f"post-{i}",
                datetime.date(2024, 1, i + 1),
            )

        request = factory.get("/musings/", {"page": "not-a-number"})
        context = self.pages["musings"].get_context(request)

        self.assertEqual(context["posts"].number, 1)

    def test_get_context_falls_back_to_last_page_when_out_of_range(self):
        for i in range(6):
            add_musings_post(
                self.pages["musings"],
                f"Post {i}",
                f"post-{i}",
                datetime.date(2024, 1, i + 1),
            )

        request = factory.get("/musings/", {"page": "99"})
        context = self.pages["musings"].get_context(request)

        self.assertEqual(context["posts"].number, 2)


class TechPageTests(TestCase):
    def setUp(self):
        self.pages = build_page_tree()

    def test_get_posts_orders_by_date_descending_and_excludes_drafts(self):
        add_tech_post(self.pages["tech"], "Older", "older", datetime.date(2024, 1, 1))
        add_tech_post(self.pages["tech"], "Newer", "newer", datetime.date(2024, 2, 1))
        add_tech_post(
            self.pages["tech"], "Draft", "draft", datetime.date(2024, 3, 1), live=False
        )

        posts = list(self.pages["tech"].get_posts())

        self.assertEqual([post.title for post in posts], ["Newer", "Older"])

    def test_get_context_paginates_four_per_page(self):
        for i in range(5):
            add_tech_post(
                self.pages["tech"], f"Post {i}", f"post-{i}", datetime.date(2024, 1, i + 1)
            )

        context = self.pages["tech"].get_context(factory.get("/tech/"))

        self.assertEqual(len(context["posts"]), 4)
        self.assertEqual(context["posts"].paginator.num_pages, 2)


class AtelierPageTests(TestCase):
    def setUp(self):
        self.pages = build_page_tree()

    def test_get_context_paginates_twelve_per_page(self):
        for i in range(14):
            add_photo(self.pages["atelier"], f"Photo {i}", f"photo-{i}")

        context = self.pages["atelier"].get_context(factory.get("/atelier/"))

        self.assertEqual(len(context["photos"]), 12)
        self.assertEqual(context["photos"].paginator.num_pages, 2)

        context_page_2 = self.pages["atelier"].get_context(
            factory.get("/atelier/", {"page": "2"})
        )
        self.assertEqual(len(context_page_2["photos"]), 2)

    def test_get_context_ignores_invalid_page_without_raising(self):
        add_photo(self.pages["atelier"], "Only Photo", "only-photo")

        request = factory.get("/atelier/", {"page": "not-a-number"})
        context = self.pages["atelier"].get_context(request)

        self.assertEqual(len(context["photos"]), 1)

    def test_get_context_excludes_unpublished_photos(self):
        add_photo(self.pages["atelier"], "Draft", "draft-photo", live=False)
        add_photo(self.pages["atelier"], "Live", "live-photo")

        context = self.pages["atelier"].get_context(factory.get("/atelier/"))

        titles = [photo.title for photo in context["photos"]]
        self.assertEqual(titles, ["Live"])
