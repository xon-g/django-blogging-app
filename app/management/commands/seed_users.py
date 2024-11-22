from django.core.management.base import BaseCommand
from django.contrib.auth.hashers import make_password
from django.db import transaction
from django.utils import timezone
from faker import Faker
from tqdm import tqdm

from app.models import User
from blog.models import Author

import random

class Command(BaseCommand):
    help = "Seed users"

    def create_username(self, username):
        count = 0
        while User.objects.filter(username=username).exists():
            count += 1
            username = f"{username}.{count}"
        return username

    def create_email(self, username):
        return f"{username}@xon.com"

    def handle(self, *args, **options):
        fake = Faker()
        total_users = 1000
        with transaction.atomic():
            with tqdm(total=total_users, desc="Creating users") as pbar:
                for _ in range(total_users):
                    first_name = fake.first_name()
                    last_name = fake.last_name()
                    username = self.create_username(f"{first_name}.{last_name}")
                    email = self.create_email(username)

                    user = User.objects.create(
                        username=username,
                        first_name=first_name,
                        last_name=last_name,
                        email=email,
                        password=make_password('password'),
                        created_at=timezone.now(),
                        updated_at=timezone.now(),
                    )

                    pbar.update(1)
                    pbar.set_postfix({'user_id': user.id, 'username': username})

                    if random.random() < 0.5:
                        author = Author.objects.create(
                            user=user,
                            name=f"{first_name} {last_name}",
                            email=email,
                        )

                    pbar.update(1)
                    pbar.set_postfix({'user_id': user.id, 'username': username})
            print("Done")