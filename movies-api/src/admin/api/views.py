from __future__ import annotations

from typing import Optional, Type

from rest_framework.serializers import Serializer


class MultiSerializerViewSetMixin:
    """Mixin for selecting an appropriate serializer from `serializer_classes`."""

    serializer_classes: Optional[dict[str, Type[Serializer]]] = None

    def get_serializer_class(self):
        try:
            return self.serializer_classes[self.action]
        except KeyError:
            return super().get_serializer_class()
