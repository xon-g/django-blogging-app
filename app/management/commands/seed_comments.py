from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone
from faker import Faker
from tqdm import tqdm

import random

from blog.models import Author, Post, Comment

class Command(BaseCommand):
    def handle(self, *args, **options):
        fake = Faker()
        posts = Post.objects.all()
        total_comments = sum(random.randint(1, 15) for _ in posts)

        with transaction.atomic():
            with tqdm(total=total_comments, desc="Creating comments") as pbar:
                for post in posts:
                    for _ in range(random.randint(1, 15)):
                        comment = Comment.objects.create(
                            post=post,
                            author=Author.objects.order_by('?').first(),
                            body=fake.text(),
                        )
                        pbar.update(1)
                        pbar.set_postfix({'comment_id': comment.id})
        print("Done")