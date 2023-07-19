from os import path, listdir
from typing import Any
from random import randrange, randint

from django.conf import settings
from django.core.management.base import BaseCommand

from faker import Faker

from accounts.models import User, Profile
from posts.models import Post


BASE_DIR = settings.BASE_DIR

faker = Faker()


def get_gender() -> str:
    """
    Return random gender.
    """

    gender: list = ['M', 'F']
    return gender[randrange(2)]


def create_fake_user(
        email: str,
        username: str,
        first_name: str,
        last_name: str,
        password: str,
) -> User:
    """
    Create `User` use fake data.
    """

    user = User.objects.create_user(
        email=email,
        username=username,
        first_name=first_name,
        last_name=last_name,
        password=password,
    )

    return user


def setup_fake_profile_image() -> str:
    """
    Setup fake profile image.
    """

    profile_images_dir_path = BASE_DIR / 'media' / 'fake' / 'avatars'
    profile_images_dir = listdir(profile_images_dir_path)
    random_profile_image = profile_images_dir[randrange(len(profile_images_dir))]

    return path.join(profile_images_dir_path, random_profile_image)


def edit_fake_user_profile(
        user: User,
        gender: str,
        description: str,
) -> None:
    """
    Edit user `Profile` use fake data.
    """

    profile = Profile.objects.get(user=user)
    profile.gender = gender
    profile.description = description
    profile.profile_image = setup_fake_profile_image()
    profile.save()


def create_fake_posts(
    author: User,
) -> None:
    """
    Create fake `Post`.
    """
    for _ in range(randint(0, 10)):
        Post.objects.create(
            author=author,
            content=faker.paragraph(),
        )


def create_users_and_edit_profiles_with_fake_data(
        number: int = 100,
) -> None:
    """
    Create `number` of users and edit their profiles with fake data.
    """

    for _ in range(number):
        gender = get_gender()
        if gender == 'M':
            first_name = faker.first_name_male()
            last_name = faker.last_name_male()
        else:
            first_name = faker.first_name_female()
            last_name = faker.last_name_female()

        user = create_fake_user(
            email=faker.ascii_free_email(),
            username=faker.user_name(),
            first_name=first_name,
            last_name=last_name,
            password=faker.lexify(text='????????'),
        )
        edit_fake_user_profile(
            user=user,
            gender=gender,
            description=faker.paragraph(),
        )
        create_fake_posts(
            author=user,
        )


def create_reply_posts() -> None:
    """
    Create reply posts.
    """

    users = User.objects.all()
    post_ids = (
        Post.objects.filter(
            is_reply=False,
        ).values_list(
            'id',
            flat=True,
        )
    )
    post_ids_length = len(post_ids)

    for user in users:
        for _ in range(randint(0, 3)):
            id = randint(1, post_ids_length - 1)
            parent = Post.objects.get(id=id)
            Post.objects.create(
                author=user,
                content=faker.paragraph(),
                is_reply=True,
                parent=parent,
            )


def create_reposts() -> None:
    """
    Create `Post` reposts.
    """

    users = User.objects.all()
    post_ids = (
        Post.objects.filter(
            is_reply=False,
        ).values_list(
            'id',
            flat=True,
        )
    )
    post_ids_length = len(post_ids)

    for user in users:
        for _ in range(randint(0, 3)):
            id = randint(1, post_ids_length - 1)
            parent = Post.objects.get(id=id)
            body = '' if randint(0, 1) else faker.paragraph()
            Post.objects.create(
                author=user,
                content=body,
                parent=parent,
            )


def create_likes() -> None:
    """
    Create likes to posts by fake users.
    """

    users = User.objects.all()
    post_ids = (
        Post.objects
        .values_list(
            'id',
            flat=True,
        )
    )
    post_ids_length = len(post_ids)

    for user in users:
        for _ in range(randint(0, 35)):
            id = randint(1, post_ids_length - 1)
            post = Post.objects.get(id=id)
            post.liked.add(user)


def create_followers() -> None:
    """
    Create followers for fake users.
    """

    users = User.objects.all()
    user_ids = (
        User.objects
        .values_list(
            'id',
            flat=True,
        )
    )
    user_ids_length = len(user_ids)

    for user in users:
        for _ in range(0, 15):
            id = randint(1, user_ids_length - 1)
            followed_user = User.objects.get(id=id)
            user.follow(followed_user)


class Command(BaseCommand):
    """
    Fake content command. Fills the database with fake data.
    """

    def add_arguments(self, parser) -> None:
        parser.add_argument(
            'number',
            type=int,
            help='Indicates the number of users to be created'
        )

    def handle(self, *args: Any, **kwargs: Any) -> None:
        number = kwargs['number']

        Faker.seed(0)

        create_users_and_edit_profiles_with_fake_data(
            number=number,
        )
        create_reply_posts()
        create_reposts()
        create_likes()
        create_followers()
