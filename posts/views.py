import uuid
from urllib.parse import urlencode

from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Count, F, Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from comments.models import Comment
from likes.models import Like
from .models import Post

VISITOR_COOKIE_NAME = 'news_visitor_id'


def get_client_ip(request):
    forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if forwarded_for:
        return forwarded_for.split(',')[0].strip()
    return request.META.get('REMOTE_ADDR', '0.0.0.0')


def get_or_create_visitor_id(request):
    visitor_id = request.COOKIES.get(VISITOR_COOKIE_NAME)
    if visitor_id:
        return visitor_id, False
    return uuid.uuid4().hex, True


def set_visitor_cookie(response, visitor_id):
    response.set_cookie(
        VISITOR_COOKIE_NAME,
        visitor_id,
        max_age=60 * 60 * 24 * 365,
        samesite='Lax',
    )


def post_list(request):
    search_query = request.GET.get('q', '').strip()
    selected_category = request.GET.get('category', '').strip()

    posts = Post.objects.filter(is_published=True)

    if search_query:
        posts = posts.filter(
            Q(title__icontains=search_query) | Q(content__icontains=search_query)
        )

    available_categories = dict(Post.CATEGORY_CHOICES)
    if selected_category in available_categories:
        posts = posts.filter(category=selected_category)
    else:
        selected_category = ''

    posts = posts.annotate(
        total_likes=Count('likes', distinct=True),
        total_comments=Count('comments', distinct=True),
    ).order_by('-is_pinned', '-created_at')
    paginator = Paginator(posts, 6)
    page_obj = paginator.get_page(request.GET.get('page'))
    query_string = urlencode(
        {
            key: value
            for key, value in {
                'q': search_query,
                'category': selected_category,
            }.items()
            if value
        }
    )

    return render(
        request,
        'posts/list.html',
        {
            'page_obj': page_obj,
            'search_query': search_query,
            'selected_category': selected_category,
            'categories': Post.CATEGORY_CHOICES,
            'query_string': query_string,
        },
    )


def post_detail(request, pk):
    post = get_object_or_404(
        Post.objects.annotate(
            total_likes=Count('likes', distinct=True),
            total_comments=Count('comments', distinct=True),
        ),
        pk=pk,
        is_published=True,
    )
    Post.objects.filter(pk=post.pk).update(views_count=F('views_count') + 1)
    post.refresh_from_db(fields=['views_count'])

    visitor_id, should_set_cookie = get_or_create_visitor_id(request)
    liked_by_user = Like.objects.filter(post=post, visitor_id=visitor_id).exists()
    related_posts = Post.objects.filter(
        is_published=True,
        category=post.category,
    ).exclude(pk=post.pk).annotate(
        total_likes=Count('likes', distinct=True),
        total_comments=Count('comments', distinct=True),
    ).order_by('-is_pinned', '-created_at')[:3]

    if len(related_posts) < 3:
        fallback_ids = [related_post.pk for related_post in related_posts]
        fallback_posts = Post.objects.filter(
            is_published=True,
        ).exclude(pk__in=[post.pk, *fallback_ids]).annotate(
            total_likes=Count('likes', distinct=True),
            total_comments=Count('comments', distinct=True),
        ).order_by('-is_pinned', '-created_at')[:3 - len(related_posts)]
        related_posts = list(related_posts) + list(fallback_posts)

    response = render(
        request,
        'posts/detail.html',
        {
            'post': post,
            'comments': post.comments.all(),
            'liked_by_user': liked_by_user,
            'related_posts': related_posts,
            'was_updated': (post.updated_at - post.created_at).total_seconds() > 1,
        },
    )
    if should_set_cookie:
        set_visitor_cookie(response, visitor_id)
    return response


@require_POST
def add_comment(request, pk):
    post = get_object_or_404(Post, pk=pk, is_published=True)
    author_name = request.POST.get('author_name', '').strip() or 'Аноним'
    content = request.POST.get('content', '').strip()

    if content:
        Comment.objects.create(
            post=post,
            author_name=author_name,
            content=content,
        )
        messages.success(request, 'Комментарий добавлен.')
    else:
        messages.error(request, 'Комментарий не может быть пустым.')

    return redirect('posts:detail', pk=post.pk)


@require_POST
def toggle_like(request, pk):
    post = get_object_or_404(Post, pk=pk, is_published=True)
    ip_address = get_client_ip(request)
    visitor_id, should_set_cookie = get_or_create_visitor_id(request)
    like, created = Like.objects.get_or_create(
        post=post,
        visitor_id=visitor_id,
        defaults={'ip_address': ip_address},
    )

    if created:
        messages.success(request, 'Лайк поставлен.')
        liked = True
    else:
        like.delete()
        messages.info(request, 'Лайк убран.')
        liked = False

    total_likes = Like.objects.filter(post=post).count()

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        response = JsonResponse(
            {
                'liked': liked,
                'likes_count': total_likes,
                'button_text': 'Убрать лайк' if liked else 'Поставить лайк',
            }
        )
        if should_set_cookie:
            set_visitor_cookie(response, visitor_id)
        return response

    next_url = request.POST.get('next')
    response = redirect(next_url) if next_url else redirect('posts:detail', pk=post.pk)
    if should_set_cookie:
        set_visitor_cookie(response, visitor_id)
    if next_url:
        return response
    return response
