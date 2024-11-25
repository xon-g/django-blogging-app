from . import seed_users, seed_posts, seed_comments


class Command(seed_users.Command, seed_posts.Command, seed_comments.Command):
    help = "Seed data"

    def handle(self, *args, **options):
        seed_users.Command.handle(self, *args, **options)
        seed_posts.Command.handle(self, *args, **options)
        seed_comments.Command.handle(self, *args, **options)
        print("Done")