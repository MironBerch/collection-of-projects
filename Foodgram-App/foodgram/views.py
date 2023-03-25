from django.shortcuts import get_object_or_404, render, redirect
from django.views.generic import CreateView
from django.urls import reverse_lazy
from foodgram.forms import CreationForm, RecipeForm
from foodgram.helper import tag_collect
from foodgram.models import Recipe, RecipeIngredient, Favorites, Wishlist, Follow
from django.core.paginator import Paginator
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User


class SignUp(CreateView):
    """SignUp view class"""
    form_class = CreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'


def index(request):
    """Main page view"""
    tags, tags_filter = tag_collect(request)
    if tags_filter:
        recipes = Recipe.objects.filter(tags_filter).all()
    else:
        recipes = Recipe.objects.all()

    paginator = Paginator(recipes, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    context = {
        'page': page,
        'paginator': paginator,
        'tags': tags,
    }

    return render(request, 'foodgram/index.html', context)


def user_page(request, username):
    """User page veiw"""
    author = get_object_or_404(User, username=username)
    tags, tags_filter = tag_collect(request)
    if tags_filter:
        recipes = Recipe.objects.filter(tags_filter).filter(author_id=author.id).all()
    else:
        recipes = Recipe.objects.filter(author_id=author.id)
    
    paginator = Paginator(recipes, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    context = {
        'page': page,
        'paginator': paginator,
        'tags': tags,
        'author': author,
    }

    return render(request, 'foodgram/user_page.html', context)


def recipe_page(request, username, recipe_id):
    author = get_object_or_404(User, username=username)
    recipe = get_object_or_404(
        Recipe, id=recipe_id, author_id=author.id
    )
    ingredients = RecipeIngredient.objects.filter(recipe_id=recipe_id)

    context = {
        'author': author,
        'recipe': recipe,
        'ingredients': ingredients,
    }
    
    return render(request, 'foodgram/recipe_page.html', context)


@login_required()
def feed(request):
    user = request.user
    authors = User.objects.filter(following__subscriber=user).prefetch_related('recipes')
    
    paginator = Paginator(authors, 3)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    context = {
        'authors': authors,
        'page': page,
        'paginator': paginator,
    }

    return render(request, 'foodgram/feed.html', context)


@login_required
def follow(request, username):
    subscriber = get_object_or_404(User, username=username)
    follow = Follow.objects.filter(subscriber=request.user, following=subscriber)
    if follow:
        follow.delete()
    else:
        follow.create(subscriber=request.user, following=subscriber)

    return redirect('user', username=username)


@login_required
def new_recipe(request):
    form_title = 'Создание рецепта'
    btn_caption = 'Создать рецепт'

    form = RecipeForm(request.POST or None, files=request.FILES or None)

    if request.method == 'POST':
        if form.is_valid():
            ingredients_names = request.POST.getlist('nameIngredient')
            ingredients_values = request.POST.getlist('valueIngredient')
            if len(ingredients_names) == len(ingredients_values):
                count = len(ingredients_names)
            else:
                return redirect('new')
            
            new_recipe = form.save(commit=False)
            new_recipe.author = request.user
            new_recipe.save()

            for ingredient in range(count):
                RecipeIngredient.add_ingredient(
                    RecipeIngredient, new_recipe.id, ingredients_names[ingredient], ingredients_values[ingredient]
                )

            return redirect('index')
        return redirect('index')
    form = RecipeForm()

    context = {
        'form_title': form_title,
        'btn_caption': btn_caption,
        'form': form,
    }

    return render(request, 'foodgram/form_recipe.html', context)


@login_required
def edit_recipe(request, username, recipe_id):
    form_title = 'Редактирование рецепта'
    btn_caption = 'Сохранить'
    recipe = get_object_or_404(Recipe, id=recipe_id)
    user = get_object_or_404(User, username=username)
    recipe_redirect = redirect(
        'recipe', username=user.username, recipe_id=recipe_id
    )
    is_breakfast = 'breakfast' in recipe.tags
    is_lunch = 'lunch' in recipe.tags
    is_dinner = 'dinner' in recipe.tags
    ingredients = RecipeIngredient.objects.filter(recipe_id=recipe_id)

    if request.user != user:
        return recipe_redirect
    form = RecipeForm(request.POST or None, files=request.FILES or None, instance=recipe)

    if request.method == 'POST' and form.is_valid():
        ingredients_names = request.POST.getlist('nameIngredient')
        ingredients_values = request.POST.getlist('valueIngredient')
        if len(ingredients_names) == len(ingredients_values):
            count = len(ingredients_names)
        else:
            return redirect('edit_recipe', username=username, recipe_id=recipe_id)

        form.save()
            
        RecipeIngredient.objects.filter(recipe_id=recipe.id).delete()

        for recipe_ingredient in range(count):
            RecipeIngredient.add_ingredient(
                RecipeIngredient, recipe.id, ingredients_names[recipe_ingredient], ingredients_values[recipe_ingredient]
            )
        return recipe_redirect

    context = {
        'form_title': form_title,
        'btn_caption': btn_caption,
        'form': form,
        'recipe': recipe,
        'is_breakfast': is_breakfast,
        'is_lunch': is_lunch,
        'is_dinner': is_dinner,
        'ingredients': ingredients,
    }

    return render(request, 'foodgram/form_recipe.html', context)


@login_required
def remove_recipe(request, username, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)

    if (recipe.author == request.user) and Recipe.objects.filter(id=recipe_id).exists():
            recipe.delete()
            return redirect('index')
    else:
        return redirect('edit_recipe', username=username, recipe_id=recipe_id)


@login_required
def favorites(request):
    user = request.user
    tags, tags_filter = tag_collect(request)
    if tags_filter:
        recipes = Recipe.objects.filter(tags_filter).filter(
            favorite_recipe__user=user
        ).all()
    else:
        recipes = Recipe.objects.filter(
            favorite_recipe__user=user
        ).all()
    
    paginator = Paginator(recipes, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    context = {
        'page': page,
        'paginator': paginator,
        'tags': tags,
    }

    return render(request, 'foodgram/favorites.html', context)


@login_required
def add_to_favorite(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    favorite = Favorites.objects.filter(user=request.user, recipe=recipe)

    if not favorite:
        favorite.create(user=request.user, recipe=recipe)
    else:
        favorite.delete()

    return redirect('recipe', recipe_id=recipe_id, username=recipe.author)


@login_required
def wishlist(request):
    """Return user recipes"""
    user = request.user
    recipes = Recipe.objects.filter(
        wishlist_recipe__user=user
    ).all

    context = {
        'recipes': recipes,
    }

    return render(request, 'foodgram/wishlist.html', context)


@login_required
def add_wishlist(request, username, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    wishlist_recipe = Wishlist.objects.filter(user=request.user, recipe=recipe)

    if not wishlist_recipe:
        wishlist_recipe.create(user=request.user, recipe=recipe)
    else:
        wishlist_recipe.delete()

    #return redirect('index')
    return redirect('recipe', recipe_id=recipe_id, username=recipe.author)


def page_not_found(request, exception):
    return render(request, "misc/404.html", {"path": request.path}, status=404)


def server_error(request):
    return render(request, "misc/500.html", status=500)


def download_wishlist(request):
    return redirect('wishlist')