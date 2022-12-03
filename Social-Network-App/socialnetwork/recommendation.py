from django.contrib.auth.models import User
from .models import Profile, Post, FollowersCount
from itertools import chain
import random


def user_following_list_create(request):
    user_following_list = []

    user_following = FollowersCount.objects.filter(follower=request.user.username)

    for users in user_following:
        user_following_list.append(users.user)

    return user_following_list


def feed_recommendation(request):
    user_following_list = user_following_list_create(request)
    feed = []

    for usernames in user_following_list:
        feed_lists = Post.objects.filter(user=usernames)
        feed.append(feed_lists)

    feed_list = list(chain(*feed))

    return feed_list


def user_recommendation(request):
    user_following = FollowersCount.objects.filter(follower=request.user.username)

    all_users = User.objects.all()
    user_following_all = []

    for user in user_following:
        user_list = User.objects.get(username=user.user)
        user_following_all.append(user_list)

    new_suggestions_list = []

    for suggestion in range(len(all_users)):
        if (suggestion not in list(user_following_all)):
            new_suggestions_list.append(suggestion)

    current_user = User.objects.filter(username=request.user.username)

    final_suggestions_list = []

    for final_suggestion in range(len(new_suggestions_list)):
        if (final_suggestion not in list(current_user)):
            final_suggestions_list.append(final_suggestion)

    random.shuffle(final_suggestions_list)

    username_profile = []
    username_profile_list = []

    for users in username_profile:
        username_profile.append(users.id)

    for ids in username_profile:
        profile_lists = Profile.objects.filter(id_user=ids)
        username_profile_list.append(profile_lists)

    suggestions_username_profile_list = list(chain(*username_profile_list))

    return suggestions_username_profile_list