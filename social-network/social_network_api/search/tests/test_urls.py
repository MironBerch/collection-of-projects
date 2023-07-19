from django.urls import resolve, reverse
from django.test import SimpleTestCase

from search.views import SearchAPIView


class SearchUrlsTests(SimpleTestCase):

    def test_search_api_view_is_resolved(self):
        """Test that SearchAPIView url works correctly."""
        url = reverse('search')
        self.assertEquals(
            resolve(url).func.view_class, SearchAPIView,
        )
