from django.test import TestCase
from django.urls import reverse

from comments.models import Comment
from likes.models import Like
from posts.models import Post


class PostViewsTests(TestCase):
    def test_post_list_shows_paginated_preview_and_media_placeholder(self):
        for number in range(7):
            Post.objects.create(
                title=f'Новость {number}',
                content='Подробный текст новости',
                video='posts/videos/news.mp4',
            )

        response = self.client.get(reverse('posts:list'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['page_obj']), 6)
        self.assertContains(response, 'Последние новости')
        self.assertContains(response, 'Видео')
        self.assertNotContains(response, '<video')
        self.assertContains(response, 'Вперед')

    def test_post_list_filters_search_category_and_published_posts(self):
        Post.objects.create(
            title='Футбольный матч',
            content='Результаты тура',
            category=Post.CATEGORY_SPORT,
        )
        Post.objects.create(
            title='Новая библиотека',
            content='Технологический обзор',
            category=Post.CATEGORY_TECH,
        )
        Post.objects.create(
            title='Черновик спорта',
            content='Не должен быть виден',
            category=Post.CATEGORY_SPORT,
            is_published=False,
        )

        response = self.client.get(
            reverse('posts:list'),
            {'q': 'матч', 'category': Post.CATEGORY_SPORT},
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Футбольный матч')
        self.assertNotContains(response, 'Новая библиотека')
        self.assertNotContains(response, 'Черновик спорта')

    def test_post_detail_shows_full_post_comments_and_video(self):
        post = Post.objects.create(
            title='Большая новость',
            content='Первая строка\nВторая строка',
            video='posts/videos/news.mp4',
        )
        Comment.objects.create(post=post, author_name='Алина', content='Хороший материал')
        Like.objects.create(
            post=post,
            ip_address='127.0.0.1',
            visitor_id='visitor-123',
        )
        self.client.cookies['news_visitor_id'] = 'visitor-123'

        response = self.client.get(
            reverse('posts:detail', args=[post.pk]),
            REMOTE_ADDR='127.0.0.1',
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Большая новость')
        self.assertContains(response, '<video')
        self.assertContains(response, 'Убрать лайк')
        self.assertContains(response, 'Хороший материал')
        post.refresh_from_db()
        self.assertEqual(post.views_count, 1)

    def test_add_comment_accepts_anonymous_user(self):
        post = Post.objects.create(title='Новость', content='Текст')

        response = self.client.post(
            reverse('posts:add_comment', args=[post.pk]),
            {'author_name': '', 'content': 'Комментарий без регистрации'},
        )

        self.assertRedirects(response, reverse('posts:detail', args=[post.pk]))
        comment = Comment.objects.get(post=post)
        self.assertEqual(comment.author_name, 'Аноним')
        self.assertEqual(comment.content, 'Комментарий без регистрации')

    def test_toggle_like_creates_and_removes_one_like_per_cookie(self):
        post = Post.objects.create(title='Новость', content='Текст')
        url = reverse('posts:toggle_like', args=[post.pk])
        self.client.cookies['news_visitor_id'] = 'visitor-123'

        first_response = self.client.post(url, REMOTE_ADDR='203.0.113.10')
        self.assertRedirects(first_response, reverse('posts:detail', args=[post.pk]))
        self.assertEqual(Like.objects.filter(post=post).count(), 1)

        second_response = self.client.post(url, REMOTE_ADDR='203.0.113.10')
        self.assertRedirects(second_response, reverse('posts:detail', args=[post.pk]))
        self.assertEqual(Like.objects.filter(post=post).count(), 0)

    def test_ajax_like_returns_updated_state(self):
        post = Post.objects.create(title='Новость', content='Текст')
        self.client.cookies['news_visitor_id'] = 'visitor-ajax'

        response = self.client.post(
            reverse('posts:toggle_like', args=[post.pk]),
            HTTP_X_REQUESTED_WITH='XMLHttpRequest',
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            {
                'liked': True,
                'likes_count': 1,
                'button_text': 'Убрать лайк',
            },
        )
