from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APIClient

from app.models import User
from blog.models import Post, Comment, Author

from faker import Faker
from pprint import pprint

class TestPostAPI(TestCase):
    user: User = None
    faker = Faker()

    def seed_posts(self, author: Author, number_of_posts: int = 10):
        # seed faker data
        for _ in range(number_of_posts):
            Post.objects.create(
                author=author,
                title=self.faker.sentence(),
                content=self.faker.text(),
                published_date=timezone.now()
            )

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user('testuser', 'testuser@example.com', 'password', first_name='Test', last_name='User')
        self.author = Author.objects.create(user=self.user)
        self.client.force_authenticate(user=self.user)

    def test_create_post(self):
        data = {
            'title': 'Test Post',
            'content': 'Test Content',
            'published_date': timezone.now(),
            'author': self.author.id
        }
        response = self.client.post(reverse('post-list'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['title'], 'Test Post')
        self.assertEqual(response.data['content'], 'Test Content')
        self.assertEqual(response.data['author'], self.author.id)

    def test_post_list(self):
        # Test empty post list count
        response = self.client.get(reverse('post-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 0)

        # Seed posts
        self.seed_posts(self.author, 100)

        # Test seeded post list count
        response = self.client.get(reverse('post-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 100)

    def test_post_detail(self):
        self.post = Post.objects.create(
            author=self.author,
            title='Test Post',
            content='Test Content',
            published_date=timezone.now()
        )
        response = self.client.get(reverse('post-detail', args=[self.post.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], self.post.id)
        self.assertEqual(response.data['title'], 'Test Post')
        self.assertEqual(response.data['content'], 'Test Content')
        self.assertEqual(response.data['author']['id'], self.author.id)

    def test_filter_by_title(self):
        post1 = Post.objects.create(title='Test Post 1', content='This is a test post', author=self.author)
        post2 = Post.objects.create(title='Test Post 2', content='This is another test post', author=self.author)
        post3 = Post.objects.create(title='Test Post 3', content='This is yet another test post', author=self.author)

        response = self.client.get(reverse('post-list'), {'title': 'Test Post 1'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(response.data['results'][0]['title'], 'Test Post 1')

    def test_filter_by_author_name(self):
        author1 = Author.objects.create(
            user=User.objects.create_user('author1', 'author1@example.com', 'password', first_name='Author', last_name='One')
        )
        author2 = Author.objects.create(
            user=User.objects.create_user('author2', 'author2@example.com', 'password', first_name='Author', last_name='Two')
        )

        post1 = Post.objects.create(title='Test Post 1', content='This is a test post', author=author1)
        post2 = Post.objects.create(title='Test Post 2', content='This is another test post', author=author2)
        post3 = Post.objects.create(title='Test Post 3', content='This is yet another test post', author=author1)

        response = self.client.get(reverse('post-list'), {'author__name': 'Author One'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 2)
        self.assertEqual(response.data['results'][0]['author'], 'Author One')
        self.assertEqual(response.data['results'][1]['author'], 'Author One')

    def test_filter_by_title_and_author_name(self):
        author1 = Author.objects.create(
            user=User.objects.create_user('author1', 'author1@example.com', 'password', first_name='Author', last_name='One')
        )
        author2 = Author.objects.create(
            user=User.objects.create_user('author2', 'author2@example.com', 'password', first_name='Author', last_name='Two')
        )

        post1 = Post.objects.create(title='Test Post 1', content='This is a test post', author=author1)
        post2 = Post.objects.create(title='Test Post 2', content='This is another test post', author=author2)
        post3 = Post.objects.create(title='Test Post 3', content='This is yet another test post', author=author1)

        response = self.client.get(reverse('post-list'), {'title': 'Test Post 3', 'author__name': 'Author One'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(response.data['results'][0]['title'], 'Test Post 3')
        self.assertEqual(response.data['results'][0]['author'], 'Author One')

    def test_create_comment(self):
        # Seed a post
        self.seed_posts(self.author, 1)
        self.post = Post.objects.first()

        # Test post detail without comments
        post_detail_response = self.client.get(reverse('post-detail', args=[self.post.id]))
        self.assertEqual(post_detail_response.status_code, status.HTTP_200_OK)
        self.assertEqual(post_detail_response.data['id'], self.post.id)
        self.assertEqual(post_detail_response.data['comments']['count'], 0)


        # Create comment
        data = {
            'body': 'Test Comment',
            'post': self.post.id
        }
        response = self.client.post(reverse('comment-list'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Test post detail with comments
        post_detail_response = self.client.get(reverse('post-detail', args=[self.post.id]))
        self.assertEqual(post_detail_response.status_code, status.HTTP_200_OK)
        self.assertEqual(post_detail_response.data['id'], self.post.id)
        self.assertEqual(post_detail_response.data['comments']['count'], 1)

        # Test comment detail
        comment = Comment.objects.first()
        comment_detail_response = self.client.get(reverse('post-detail', args=[self.post.id]))
        self.assertEqual(comment_detail_response.status_code, status.HTTP_200_OK)
        self.assertEqual(comment_detail_response.data['id'], self.post.id)
        self.assertEqual(comment_detail_response.data['comments']['count'], 1)
        self.assertEqual(comment_detail_response.data['comments']['results'][0]['id'], comment.id)
        self.assertEqual(comment_detail_response.data['comments']['results'][0]['body'], 'Test Comment')

