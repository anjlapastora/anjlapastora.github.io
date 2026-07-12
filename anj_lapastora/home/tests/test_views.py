import datetime

from django.test import TestCase

from .factories import add_musings_post, add_photo, add_tech_post, build_page_tree


class HomePageViewTests(TestCase):
    def setUp(self):
        self.pages = build_page_tree()

    def test_home_page_renders(self):
        response = self.client.get("/")

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "anj lapastora")

    def test_home_page_lists_recent_post(self):
        add_tech_post(
            self.pages["tech"], "My Tech Post", "my-tech-post", datetime.date(2024, 1, 1)
        )

        response = self.client.get("/")

        self.assertContains(response, "My Tech Post")


class AboutPageViewTests(TestCase):
    def setUp(self):
        self.pages = build_page_tree()

    def test_about_page_renders_bio_and_placeholder(self):
        response = self.client.get("/about/")

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Hi, I&rsquo;m Anj. Thanks for being here.")
        self.assertContains(response, "portrait")


class TechPageViewTests(TestCase):
    def setUp(self):
        self.pages = build_page_tree()

    def test_listing_renders_posts(self):
        add_tech_post(self.pages["tech"], "First Post", "first-post", datetime.date(2024, 1, 1))

        response = self.client.get("/tech/")

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "First Post")

    def test_listing_paginates(self):
        for i in range(5):
            add_tech_post(
                self.pages["tech"], f"Post {i}", f"post-{i}", datetime.date(2024, 1, i + 1)
            )

        response = self.client.get("/tech/?page=2")

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "page 2 of 2")

    def test_post_detail_renders_with_main_image(self):
        from .factories import make_test_image

        post = add_tech_post(
            self.pages["tech"],
            "Post With Image",
            "post-with-image",
            datetime.date(2024, 1, 1),
            main_image=make_test_image(),
        )

        response = self.client.get(post.url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Post With Image")
        self.assertContains(response, "article-hero")

    def test_post_detail_renders_without_main_image(self):
        post = add_tech_post(
            self.pages["tech"], "Post Without Image", "post-without-image", datetime.date(2024, 1, 1)
        )

        response = self.client.get(post.url)

        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "article-hero")

    def test_post_detail_shows_next_sibling_link(self):
        first = add_tech_post(
            self.pages["tech"], "First", "first", datetime.date(2024, 1, 1)
        )
        add_tech_post(self.pages["tech"], "Second", "second", datetime.date(2024, 1, 2))

        response = self.client.get(first.url)

        self.assertContains(response, "Second")


class MusingsPageViewTests(TestCase):
    def setUp(self):
        self.pages = build_page_tree()

    def test_listing_renders_posts(self):
        add_musings_post(
            self.pages["musings"], "A Musing", "a-musing", datetime.date(2024, 1, 1)
        )

        response = self.client.get("/musings/")

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "A Musing")

    def test_post_detail_renders(self):
        post = add_musings_post(
            self.pages["musings"], "A Musing", "a-musing", datetime.date(2024, 1, 1)
        )

        response = self.client.get(post.url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "A Musing")
        self.assertContains(response, "MUSINGS")


class AtelierPageViewTests(TestCase):
    def setUp(self):
        self.pages = build_page_tree()

    def test_listing_renders_photos(self):
        add_photo(self.pages["atelier"], "A Photo", "a-photo", caption="A caption")

        response = self.client.get("/atelier/")

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "A caption")

    def test_listing_renders_with_no_photos(self):
        response = self.client.get("/atelier/")

        self.assertEqual(response.status_code, 200)


class MissingPageViewTests(TestCase):
    def setUp(self):
        build_page_tree()

    def test_unknown_path_returns_404(self):
        response = self.client.get("/this-page-does-not-exist/")

        self.assertEqual(response.status_code, 404)
