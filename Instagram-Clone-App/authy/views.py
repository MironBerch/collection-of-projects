from django.urls import resolve
from django.shortcuts import render, redirect, get_object_or_404
from authy.forms import SignupForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from authy.models import Profile
from post.models import Post, Follow, Stream
from django.db import transaction
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.core.paginator import Paginator
from django.http import Http404


def UserProfile(request, username):
	user = get_object_or_404(User, username=username)
	profile = Profile.objects.get(user=user)
	url_name = resolve(request.path).url_name
	
	if url_name == 'profile':
		posts = Post.objects.filter(user=user).order_by('-posted')

	else:
		posts = profile.favorites.all()
	posts_count = Post.objects.filter(user=user).count()
	following_count = Follow.objects.filter(follower=user).count()
	followers_count = Follow.objects.filter(following=user).count()
	follow_status = Follow.objects.filter(following=user, follower=request.user).exists()
	paginator = Paginator(posts, 8)
	page_number = request.GET.get('page')
	posts_paginator = paginator.get_page(page_number)
	template = loader.get_template('profile/view.html')
	context = {
		'posts': posts_paginator,
		'profile':profile,
		'following_count':following_count,
		'followers_count':followers_count,
		'posts_count':posts_count,
		'follow_status':follow_status,
		'url_name':url_name,
	}
	return HttpResponse(template.render(context, request))


def UserProfileFavorites(request, username):
	user = get_object_or_404(User, username=username)
	profile = Profile.objects.get(user=user)
	posts = profile.favorites.all()
	posts_count = Post.objects.filter(user=user).count()
	following_count = Follow.objects.filter(follower=user).count()
	followers_count = Follow.objects.filter(following=user).count()
	paginator = Paginator(posts, 8)
	page_number = request.GET.get('page')
	posts_paginator = paginator.get_page(page_number)
	template = loader.get_template('profile/favorite.html')
	context = {
		'posts': posts_paginator,
		'profile':profile,
		'following_count':following_count,
		'followers_count':followers_count,
		'posts_count':posts_count,
	}
	return HttpResponse(template.render(context, request))


def signup(request):
	if request.method == 'POST':
		form = SignupForm(request.POST)
		if form.is_valid():
			username = form.cleaned_data.get('username')
			email = form.cleaned_data.get('email')
			password = form.cleaned_data.get('password')
			User.objects.create_user(username=username, email=email, password=password)
			return redirect('index')
	else:
		form = SignupForm()
	context = {
		'form':form,
	}
	return render(request, 'authy/signup.html', context)


@login_required
def edit_profile(request):
	user = request.user.id
	profile = Profile.objects.get(user__id=user)
	try:
		user_profile = Profile.objects.get(user=request.user)
	except Profile.DoesNotExist:
		raise Http404
	context = {
        'user_profile': user_profile
    }
	if request.method == 'POST':
		if request.FILES.get('picture') == None:
			picture = user_profile.picture
			first_name = request.POST['first_name']
			last_name = request.POST['last_name']
			url = request.POST['url']
			profile_info = request.POST['profile_info']

			user_profile.picture = picture
			user_profile.first_name = first_name
			user_profile.last_name = last_name
			user_profile.url = url
			user_profile.profile_info = profile_info
			user_profile.save()
		if request.FILES.get('picture') != None:
			picture = request.FILES.get('picture')
			first_name = request.POST['first_name']
			last_name = request.POST['last_name']
			url = request.POST['url']
			profile_info = request.POST['profile_info']
			user_profile.picture = picture
			user_profile.first_name = first_name
			user_profile.last_name = last_name
			user_profile.url = url
			user_profile.profile_info = profile_info
			user_profile.save()

		return redirect('edit-profile')
	return render(request, 'profile/edit.html', context)


@login_required
def follow(request, username, option):
	following = get_object_or_404(User, username=username)
	try:
		f, created = Follow.objects.get_or_create(follower=request.user, following=following)
		if int(option) == 0:
			f.delete()
			Stream.objects.filter(following=following, user=request.user).all().delete()
		else:
			posts = Post.objects.all().filter(user=following)[:25]
			with transaction.atomic():
				for post in posts:
					stream = Stream(post=post, user=request.user, date=post.posted, following=following)
					stream.save()

		return HttpResponseRedirect(reverse('profile', args=[username]))
	except User.DoesNotExist:
		return HttpResponseRedirect(reverse('profile', args=[username]))