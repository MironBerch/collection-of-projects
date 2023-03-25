from django.db import models
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

from multiselectfield import MultiSelectField


TAG_CHOICES = (
    ('breakfast', 'Завтрак'),
    ('lunch', 'Обед'),
    ('dinner', 'Ужин'),
)


class Recipe(models.Model):
    """Recipe model"""
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='recipes', verbose_name='Author'
    )
    title = models.CharField(
        max_length=50, verbose_name='Recipe name'
    )
    publication_date = models.DateTimeField(
        auto_now_add=True, verbose_name='Publication_date'
    )
    tags = MultiSelectField(
        max_length=50, choices=TAG_CHOICES, blank=True, null=True, verbose_name='Tags', max_choices=3
    )
    description = models.TextField(
        blank=True, null=True, verbose_name='Description'
    )
    time = models.PositiveIntegerField(verbose_name='Time for preparing')
    image = models.ImageField(
        upload_to='recipes/', blank=True, null=True, verbose_name='Image'
    )

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-publication_date']
        verbose_name = 'Recipe'
        verbose_name_plural = 'Recipes'


class Ingredient(models.Model):
    """Ingredients model"""
    title = models.CharField(
        max_length=50, verbose_name='Ingredient name'
    )
    dimension = models.CharField(
        max_length=25, verbose_name='Unit of measurement'
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Ingredient'
        verbose_name_plural = 'Ingredients'


class RecipeIngredient(models.Model):
    """Recipe Ingredient description"""
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, verbose_name='Recipe'
    )
    ingredient = models.ForeignKey(
        Ingredient, on_delete=models.CASCADE, verbose_name='Ingredient'
    )
    amount = models.PositiveIntegerField(verbose_name="Amount")

    def add_ingredient(self, recipe_id, title, amount):
        ingredient = get_object_or_404(Ingredient, title=title)
        return self.objects.get_or_create(
            recipe_id=recipe_id, ingredient=ingredient, amount=amount
        )


class Follow(models.Model):
    """Follow user-follower"""
    follow_id = models.AutoField(auto_created=True, primary_key=True)
    subscriber = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='subscriber'
    )
    following = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='following'
    )


class Favorites(models.Model):
    """Favorite user recipes"""
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='favorite_subscriber'
    )
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, related_name='favorite_recipe'
    )


class Wishlist(models.Model):
    """Wish list"""
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='wishlist_subscriber'
    )
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, related_name='wishlist_recipe'
    )