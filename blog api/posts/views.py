from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
import json
from .models import Post, Comment

@csrf_exempt
def register(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user = User.objects.create_user(
                username=data['username'],
                email=data['email'],
                password=data['password']
            )
            return JsonResponse({
                'id': user.id,
                'username': user.username,
                'email': user.email
            }, status=201)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse({'error': 'Method not allowed'}, status=405)

@csrf_exempt
def user_login(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user = authenticate(
                username=data['username'],
                password=data['password']
            )
            if user:
                login(request, user)
                return JsonResponse({
                    'message': 'Login successful',
                    'user_id': user.id,
                    'username': user.username
                }, status=200)
            return JsonResponse({'error': 'Invalid credentials'}, status=401)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse({'error': 'Method not allowed'}, status=405)

@csrf_exempt
def user_logout(request):
    if request.method == 'POST':
        logout(request)
        return JsonResponse({'message': 'Logout successful'}, status=200)
    return JsonResponse({'error': 'Method not allowed'}, status=405)

@csrf_exempt
def create_post(request):
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Authentication required'}, status=401)
    
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            post = Post.objects.create(
                author=request.user,
                title=data['title'],
                content=data['content']
            )
            return JsonResponse({
                'id': post.id,
                'title': post.title,
                'author': post.author.username,
                'created_at': post.created_at
            }, status=201)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse({'error': 'Method not allowed'}, status=405)

def list_posts(request):
    if request.method == 'GET':
        posts = Post.objects.all().select_related('author')
        posts_data = [{
            'id': post.id,
            'title': post.title,
            'author': post.author.username,
            'created_at': post.created_at
        } for post in posts]
        return JsonResponse(posts_data, safe=False)
    return JsonResponse({'error': 'Method not allowed'}, status=405)

def post_detail(request, id):
    if request.method == 'GET':
        post = get_object_or_404(Post, id=id)
        comments = Comment.objects.filter(post=post).select_related('user')
        return JsonResponse({
            'post': {
                'title': post.title,
                'content': post.content,
                'author': post.author.username,
                'created_at': post.created_at
            },
            'comments': [{
                'user': comment.user.username,
                'text': comment.text,
                'created_at': comment.created_at
            } for comment in comments]
        })
    return JsonResponse({'error': 'Method not allowed'}, status=405)

@csrf_exempt
def create_comment(request, id):
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Authentication required'}, status=401)
    
    if request.method == 'POST':
        try:
            post = get_object_or_404(Post, id=id)
            data = json.loads(request.body)
            comment = Comment.objects.create(
                post=post,
                user=request.user,
                text=data['text']
            )
            return JsonResponse({
                'message': 'Comment added',
                'comment_id': comment.id
            }, status=201)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse({'error': 'Method not allowed'}, status=405)