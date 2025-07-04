from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
import json
from .models import Post, Comment

class BlogTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.post = Post.objects.create(
            author=self.user,
            title='Test Post',
            content='Test content'
        )

    def test_create_post_authenticated(self):
        self.client.login(username='testuser', password='testpass123')
        url = reverse('create_post')
        data = {
            "title": "New Post",
            "content": "New content"
        }
        response = self.client.post(
            url,
            data=json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Post.objects.count(), 2)

    def test_comment_creation(self):
        self.client.login(username='testuser', password='testpass123')
        url = reverse('create_comment', args=[self.post.id])
        data = {"text": "Test comment"}
        response = self.client.post(
            url,
            data=json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Comment.objects.count(), 1)