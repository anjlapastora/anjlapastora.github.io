from django.test import TestCase

from home.tests.factories import build_page_tree


class SearchViewTests(TestCase):
    def setUp(self):
        self.pages = build_page_tree()

    def test_no_query_returns_200_with_no_results(self):
        response = self.client.get("/search/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context["search_results"]), [])

    def test_query_matching_a_live_page_returns_it(self):
        response = self.client.get("/search/", {"query": "Atelier"})

        self.assertEqual(response.status_code, 200)
        titles = [page.title for page in response.context["search_results"]]
        self.assertIn("Atelier", titles)

    def test_query_records_a_search_hit(self):
        from wagtail.contrib.search_promotions.models import Query

        self.client.get("/search/", {"query": "Atelier"})

        query = Query.get("Atelier")
        self.assertEqual(query.hits, 1)

    def test_non_integer_page_falls_back_to_first_page(self):
        response = self.client.get(
            "/search/", {"query": "Atelier", "page": "not-a-number"}
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["search_results"].number, 1)

    def test_out_of_range_page_falls_back_to_last_page(self):
        response = self.client.get("/search/", {"query": "Atelier", "page": "999"})

        self.assertEqual(response.status_code, 200)
        results = response.context["search_results"]
        self.assertEqual(results.number, results.paginator.num_pages)
