from typing import Union

from accounts.models import User
from posts.models import Post


def create_post(
    author: User,
    is_reply: bool = False,
    parent: Union[Post, None] = None,
) -> Post:
    return Post.objects.create(
        author=author,
        content='content',
        is_reply=is_reply,
        parent=parent,
    )
