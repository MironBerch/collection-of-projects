from django.db import models


def get_character_image_upload_path(instance: 'Character', filename: str) -> str:
    return f'upload/character/{instance.full_name}/{filename}'


def get_default_character_image() -> str:
    return f'default/default_character_image.png'


class Character(models.Model):
    """Anime characters"""
    full_name = models.CharField(max_length=100)
    character_image = models.ImageField(
        upload_to=get_character_image_upload_path,
        default=get_default_character_image,
    )
    description = models.TextField(max_length=5000)