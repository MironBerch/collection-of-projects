from typing import Optional, Type

from rest_framework.serializers import Serializer


class MultiSerializerViewSetMixin:
    """Mixin для выбора подходящего сериализатора из `serializer_classes`."""

    serializer_classes: Optional[dict[str, Type[Serializer]]] = None

    def get_serializer_class(self):
        try:
            return self.serializer_classes[self.action]
        except KeyError:
            return super().get_serializer_class()
