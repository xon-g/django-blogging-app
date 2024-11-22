from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone
from faker import Faker
from tqdm import tqdm

from blog.models import Author, Post

import random


class Command(BaseCommand):
    help = "Seed posts"

    def random_date(self, start_date, end_date):
        delta = end_date - start_date
        int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
        random_second = random.randrange(int_delta)
        return start_date + timezone.timedelta(seconds=random_second)

    def handle(self, *args, **options):
        fake = Faker()
        total_posts = sum(random.randint(1, 20) for _ in Author.objects.all())

        with transaction.atomic():
            with tqdm(total=total_posts, desc="Creating posts") as pbar:
                for author in Author.objects.all():
                    for _ in range(random.randint(1, 20)):
                        post = Post.objects.create(
                            author=author,
                            title=fake.sentence(),
                            content=fake.text(),
                            published_date=self.random_date(
                                timezone.now() - timezone.timedelta(days=365*5), timezone.now()
                            )
                        )
                        pbar.update(1)
                        pbar.set_postfix({'post_id': post.id, 'title': post.title, 'author': post.author})
        print("Done")