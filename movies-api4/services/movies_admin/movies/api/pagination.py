from collections import OrderedDict

from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class ResultsSetPagination(PageNumberPagination):
    """Pagination with custom field names."""

    page_size = 20

    def get_paginated_response(self, data):
        return Response(
            OrderedDict(
                [
                    ('count', self.page.paginator.count),
                    ('total_pages', self.page.paginator.num_pages),
                    ('prev', self._get_previous_page_number()),
                    ('next', self._get_next_page_number()),
                    ('results', data),
                ],
            ),
        )

    def get_paginated_response_schema(self, schema) -> dict:
        return {
            'type': 'object',
            'properties': {
                'count': {
                    'type': 'integer',
                    'example': 100,
                },
                'total_pages': {
                    'type': 'integer',
                    'example': 5,
                },
                'next': {
                    'type': 'integer',
                    'nullable': True,
                    'example': 4,
                },
                'previous': {
                    'type': 'integer',
                    'nullable': True,
                    'example': 2,
                },
                'results': schema,
            },
        }

    def _get_next_page_number(self) -> int | None:
        if not self.page.has_next():
            return None
        return self.page.next_page_number()

    def _get_previous_page_number(self) -> int | None:
        if not self.page.has_previous():
            return None
        return self.page.previous_page_number()
