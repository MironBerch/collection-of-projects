from http import HTTPStatus
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse_lazy
from yatube.forms import *
from yatube.models import *
from django.core.paginator import Paginator
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView


class SignUp(CreateView):
    form_class = CreationForm
    success_url = reverse_lazy('posts:index')
    template_name = 'users/signup.html'


def paginator(request, post_list):
    """Paginate function"""
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    return paginator.get_page(page_number)


def index(request):
    """Function for view main page"""
    post_list = Post.objects.select_related('author', 'group')

    context = {
        'page_objects': paginator(request, post_list),
    }

    return render(request, 'posts/index.html', context)


def group_posts(request, slug):
    """Function for view community page"""
    group = get_object_or_404(Group, slug=slug)
    post_list = group.posts.select_related('author')
    
    context = {
        'group': group,
        'page_obj': paginator(request, post_list),
    }

    return render(request, 'posts/group_list.html', context)


def profile(request, username):
    """Function for view user profile"""
    author = get_object_or_404(User, username=username)
    post_list = author.post.select_related('group')
    following = request.user.is_auntificated and (request.user.follower.filter(author=author).exists())
    
    context = {
        'author': author,
        'page_obj': paginator(request, post_list),
        'following': following,
    }

    return render(request, 'posts/profile.html', context)


def post_detail(request, post_id):
    """Function detail view post page"""
    post = get_object_or_404(Post, pk=post_id)
    form = CommentForm()
    comments = post.comments.all()

    context = {
        'post': post,
        'form': form,
        'comments': comments,
    }

    return render(request, 'posts/post_detail.html', context)


@login_required
def post_create(request):
    """Function for creating post"""
    form = PostForm(request.POST or None, files=request.FILES or None)

    context = {
        'form': form,
    }

    if form.is_valid():
        post = form.save(commit=False)
        post.author = request.user
        post.save()

        return redirect('profile', username=post.author)

    return render(request, 'posts/create_post.html', context)


@login_required
def post_edit(request, post_id):
    """Function for edit post"""
    post = get_object_or_404(Post, pk=post_id)
    
    if post.author != request.user: return redirect('post_detail', post_id=post_id)
    
    form = PostForm(request.POST or None, files=request.FILES or None, instance=post,)

    if form.is_valid():
        form.save()
        return redirect('post_detail', post_id=post_id)
    
    context = {
        'post': post,
        'form': form,
        'is_edit': True,
    }

    return render(request, 'posts/create_post.html', context)


@login_required
def add_comment(request, post_id):
    """Function for add comment"""
    post = get_object_or_404(Post, pk=post_id)
    form = CommentForm(request.POST or None)

    if form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user
        comment.post = post
        comment.save()

    return redirect('post_detail', post_id=post_id)


@login_required
def follow_index(request):
    """Function for view followers"""
    post_list = Post.objects.filter(author__following__user=request.user)
    
    context = {
        'page_obj': paginator(request, post_list),
    }

    return render(request, 'posts/follow.html', context)


@login_required
def profile_follow(request, username):
    """Function for follow user"""
    author = get_object_or_404(User, username=username)

    if request.user != author: Follow.objects.get_or_create(user=request.user, author=author)

    return redirect('profile', username=username)


@login_required
def profile_unfollow(request, username):
    """Function for unfollow user"""
    author = get_object_or_404(User, username=username)
    Follow.objects.filter(user=request.user, author=author).delete()
    return redirect('profile', username=username)


def page_not_found(request, exception):
    """Setting template for page with exception 404."""
    context = {
        'path': request.path
    }

    return render(request, 'core/404.html', context, status=HTTPStatus.NOT_FOUND)


def server_error(request):
    """Setting template for page with exception 500."""
    return render(request, 'core/500.html', status=HTTPStatus.INTERNAL_SERVER_ERROR)


def permission_denied(request, exception):
    """Setting template for page with error 403."""
    return render(request, 'core/403.html', status=HTTPStatus.FORBIDDEN)


def csrf_failure(request, reason=''):
    """Setting template for page with examination CSRF error, request rejected."""
    return render(request, 'core/403csrf.html')