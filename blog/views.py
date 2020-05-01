from datetime import datetime

from django.shortcuts import render, redirect
from django.utils import timezone

from .models import *





def delete(request, post_id):
    blog_post = Post.objects.get(id=post_id)
    context = {
        'message': "Post has benn successfully deleted",
        'posts': Post.objects.order_by('-date_posted')

    }
    blog_post.delete()
    return render(request, 'blog/home.html', context)


def about(request, post_id):
    raw_comments = Comment.objects.filter(post_id=post_id)
    comments = []
    for raw_comment in raw_comments:
        raw_replies = Reply.objects.filter(comment_id=raw_comment.id)
        rep_ripe = []
        for rep in raw_replies:
            x = rep.user_id
            user_name = CustomUser.objects.get(id=x).username
            rep_ripe.append((rep, user_name))
        x = raw_comment.user_id
        user_name = CustomUser.objects.get(id=x).username
        comments.append((raw_comment, user_name, rep_ripe))

    post_t = Post.objects.get(id=post_id)

    context = {
        'post': post_t,
        'days': (datetime.now().date() - post_t.date_posted.date()).days,
        'comments': comments
    }
    return render(request, 'blog/about.html', context)


def add(request):
    if request.method == "POST":
        new_post = Post()
        new_post.author = request.user
        new_post.title = request.POST["title"]
        new_post.content = request.POST["content"]
        new_post.save()
        context = {
            'posts': Post.objects.order_by('-date_posted'),
            'message': "Post has benn successfully created",

        }
        return render(request, 'blog/home.html', context)
    else:
        return render(request, 'blog/add.html')


def update_blog(request, post_id):
    if request.method == "POST":
        post = Post.objects.get(id=post_id)
        post.title = request.POST["title"]
        post.content = request.POST["content"]
        post.save()
        context = {
            'posts': Post.objects.order_by('-date_posted'),
            'message': "Post has benn successfully updated",

        }
        return render(request, 'blog/home.html', context)
    else:
        context = {
            'post': Post.objects.get(id=post_id),
        }
        return render(request, 'blog/update.html', context)


def add_comment(request, post_id):
    if request.method == "POST":
        com = request.POST["comment"]
        new_comment = Comment()
        new_comment.post_id = post_id
        new_comment.user_id = request.user.id
        new_comment.com = com
        new_comment.user_name = request.user.username
        new_comment.save()

        raw_comments = Comment.objects.filter(post_id=post_id)
        comments = []
        for raw_comment in raw_comments:
            raw_replies = Reply.objects.filter(comment_id=raw_comment.id)
            rep_ripe = []
            for rep in raw_replies:
                x = rep.user_id
                user_name = CustomUser.objects.get(id=x).username
                rep_ripe.append((rep, user_name))
            x = raw_comment.user_id
            user_name = CustomUser.objects.get(id=x).username
            comments.append((raw_comment, user_name, rep_ripe))

        post_t = Post.objects.get(id=post_id)
        context = {
            'post': post_t,
            'days': (datetime.now().date() - post_t.date_posted.date()).days,
            'comments': comments
        }

        return render(request, 'blog/about.html', context)


def add_reply(request, comment_id):
    if request.method == "POST":
        new_rep = Reply()
        new_rep.comment_id = comment_id
        new_rep.user_id = request.user.id
        new_rep.reply_to = request.POST["reply_to"]
        new_rep.save()
        post_id = Comment.objects.get(id=comment_id).post_id
        raw_comments = Comment.objects.filter(post_id=post_id)
        comments = []
        for raw_comment in raw_comments:
            raw_replies = Reply.objects.filter(comment_id=raw_comment.id)
            rep_ripe = []
            for rep in raw_replies:
                x = rep.user_id
                user_name = CustomUser.objects.get(id=x).username
                rep_ripe.append((rep, user_name))
            x = raw_comment.user_id
            user_name = CustomUser.objects.get(id=x).username
            comments.append((raw_comment, user_name, rep_ripe))

        post_t = Post.objects.get(id=post_id)
        context = {
            'post': post_t,
            'days': (datetime.now().date() - post_t.date_posted.date()).days,
            'comments': comments
        }

        return render(request, 'blog/about.html', context)


def delete_comment(request, comment_id):
    reply_set = Reply.objects.filter(comment_id=comment_id)
    for rep in reply_set:
        rep.delete()
    com = Comment.objects.get(id=comment_id)
    post_id = com.post_id
    com.delete()
    raw_comments = Comment.objects.filter(post_id=post_id)
    comments = []
    for raw_comment in raw_comments:
        raw_replies = Reply.objects.filter(comment_id=raw_comment.id)
        rep_ripe = []
        for rep in raw_replies:
            x = rep.user_id
            user_name = CustomUser.objects.get(id=x).username
            rep_ripe.append((rep, user_name))
        x = raw_comment.user_id
        user_name = CustomUser.objects.get(id=x).username
        comments.append((raw_comment, user_name, rep_ripe))

    post_t = Post.objects.get(id=post_id)

    context = {
        'post': post_t,
        'days': (datetime.now().date() - post_t.date_posted.date()).days,
        'comments': comments
    }
    return render(request, 'blog/about.html', context)


def delete_reply(request, reply_id):
    rep = Reply.objects.get(id=reply_id)
    rep.delete()
    comment_id = rep.comment_id
    com = Comment.objects.get(id=comment_id)
    post_id = com.post_id
    raw_comments = Comment.objects.filter(post_id=post_id)
    comments = []
    for raw_comment in raw_comments:
        raw_replies = Reply.objects.filter(comment_id=raw_comment.id)
        rep_ripe = []
        for rep in raw_replies:
            x = rep.user_id
            user_name = CustomUser.objects.get(id=x).username
            rep_ripe.append((rep, user_name))
        x = raw_comment.user_id
        user_name = CustomUser.objects.get(id=x).username
        comments.append((raw_comment, user_name, rep_ripe))

    post_t = Post.objects.get(id=post_id)

    context = {
        'post': post_t,
        'days': (datetime.now().date() - post_t.date_posted.date()).days,
        'comments': comments
    }
    return render(request, 'blog/about.html', context)


def edit_comment(request, comment_id):
    if request.method == "POST":
        com = Comment.objects.get(id=comment_id)
        com.com = request.POST["com"]
        com.save()
        post_id = com.post_id

        raw_comments = Comment.objects.filter(post_id=post_id)
        comments = []
        for raw_comment in raw_comments:
            raw_replies = Reply.objects.filter(comment_id=raw_comment.id)
            rep_ripe = []
            for rep in raw_replies:
                x = rep.user_id
                user_name = CustomUser.objects.get(id=x).username
                rep_ripe.append((rep, user_name))
            x = raw_comment.user_id
            user_name = CustomUser.objects.get(id=x).username
            comments.append((raw_comment, user_name, rep_ripe))

        post_t = Post.objects.get(id=post_id)

        context = {
            'post': post_t,
            'days': (datetime.now().date() - post_t.date_posted.date()).days,
            'comments': comments
        }
        return render(request, 'blog/about.html', context)


def edit_reply(request, reply_id):

    if request.method == "POST":
        rep = Reply.objects.get(id=reply_id)
        rep.reply_to = request.POST["reply_to"]
        rep.save()
        print(rep)
        post_id = Comment.objects.get(id=rep.comment_id).post_id

        raw_comments = Comment.objects.filter(post_id=post_id)
        comments = []
        for raw_comment in raw_comments:
            raw_replies = Reply.objects.filter(comment_id=raw_comment.id)
            print(raw_replies)
            rep_ripe = []
            for rep in raw_replies:
                x = rep.user_id
                user_name = CustomUser.objects.get(id=x).username
                rep_ripe.append((rep, user_name))
            x = raw_comment.user_id
            user_name = CustomUser.objects.get(id=x).username
            comments.append((raw_comment, user_name, rep_ripe))

        post_t = Post.objects.get(id=post_id)
        print(comments)
        context = {
            'post': post_t,
            'days': (datetime.now().date() - post_t.date_posted.date()).days,
            'comments': comments
        }
        return render(request, 'blog/about.html', context)