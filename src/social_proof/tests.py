from django.test import TestCase
from django.urls import reverse

from src.social_proof.models import Review


class ReviewsCarouselTests(TestCase):
    def test_home_renders_reviews_carousel(self):
        for index in range(5):
            Review.objects.create(
                author=f"Author {index}",
                quote_uk=f"Цитата {index}",
                quote_en=f"Quote {index}",
                flag="flag",
                order=index,
                is_published=True,
            )
        response = self.client.get(reverse("pages:home"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "data-reviews-carousel")
        self.assertContains(response, "data-reviews-track")
        self.assertContains(response, 'data-reviews-count="5"')
        self.assertContains(response, "Цитата 0")
        self.assertContains(response, "Цитата 4")
        self.assertContains(response, 'data-reviews-dot="4"')
        self.assertContains(response, "Lardi-Trans")
        self.assertContains(
            response,
            "https://lardi-trans.com/log/user/15009884246/responses/?scopeType=POSITIVE",
        )
