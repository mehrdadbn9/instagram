from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import ListView, CreateView
from pip._internal import self_outdated_check
from rest_framework import generics
from django.template import loader
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from content.forms import NewPostForm
from content.models import Post, Tag, Media, Like, Stream
from activity.models import Comment
from content.serializers import PostListSerializer, PostCreateSerializer, PostHyperlinkSerializer, PostDetailSerializer
from activity.forms import CommentForm

User = get_user_model()
"""
                                                API
"""


class PostListCreateAPIView(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostListSerializer

    def get_serializer_class(self):
        if self.request.method.lower() == 'post':
            return PostCreateSerializer
        return self.serializer_class

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


######################should complete##########
class MyFriendViewSet(ReadOnlyModelViewSet):
    queryset = Stream.objects.all().order_by('following')

    def get_serializer_class(self):
        if self.action == 'list':
            return PostHyperlinkSerializer
        elif self.action == 'retrieve':
            return PostDetailSerializer



"""
                                            class Base
"""


class PostListView(ListView):
    model = Post
    template_name = "Post_List.html"  # #   gozashte shavad!
    context_object_name = "post_list"
    paginate_by = 3

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)


# context['is_following'] = Relation.objects.filter(from_user=self.request.user, to_user=user).exists() ########



@login_required
def index(request):
    user = request.user
    posts = Stream.objects.filter(user=user)

    group_ids = []

    for post in posts:
        group_ids.append(post.post_id)

    post_items = Post.objects.filter(id__in=group_ids).all().order_by('-created_time')

    template = loader.get_template('index.html')
    print('hello')
    context = {

        'post_items': post_items,

    }
    return HttpResponse(template.render(context, request))

    # return HttpResponse(posts)
    # return HttpResponse(post_items)


def post_details(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    user = request.user
    profile = User.objects.get(username=user)
    # comment
    comments = Comment.objects.filter(post=post).order_by('created_time')

    if request.user.is_authenticated:
        profile = User.objects.get(username=user)

    # Comments Form
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.user = user
            comment.save()
            return HttpResponseRedirect(reverse('postdetails', args=[post_id]))
    else:
        form = CommentForm()

    template = loader.get_template('post_detail.html')

    context = {
        'post': post,
        'profile': profile,
        'form': form,
        'comments': comments,
    }

    return HttpResponse(template.render(context, request))


@login_required
def new_post(request):
    user = request.user
    tags_objs = []
    files_objs = []
    if request.method == 'POST':
        form = NewPostForm(request.POST, request.FILES)
        if form.is_valid():
            files = request.FILES.getlist('content')
            caption = form.cleaned_data.get('caption')
            tags_form = form.cleaned_data.get('tags')

            tags_list = list(tags_form.split(','))

            for tag in tags_list:
                t, created = Tag.objects.get_or_create(title=tag)
                tags_objs.append(t)

            for file in files:
                file_instance = Media(media_file=file, user=user)
                file_instance.save()
                files_objs.append(file_instance)

            p, created = Post.objects.get_or_create(caption=caption, user=user)
            p.tags.set(tags_objs)
            p.media.set(files_objs)
            p.save()
            return redirect('myfriend')
    else:
        form = NewPostForm()

    context = {
        'form': form,
    }

    return render(request, 'newpost.html', context)


def tags(request, tag_slug):
    tag = get_object_or_404(Tag, slug=tag_slug)
    posts = Post.objects.filter(tags=tag).order_by('-created_time')

    template = loader.get_template('tag.html')

    context = {
        'posts': posts,
        'tag': tag,
    }

    return HttpResponse(template.render(context, request))


@login_required
def like(request, post_pk):
    user = request.user
    post = Post.objects.get(pk=post_pk)
    current_likes = post.likes
    liked = Like.objects.filter(user=user, likes=Post.likes).count()

    if not liked:
        like = Like.objects.create(user=user, likes=Post.likes)
        like.save()
        current_likes = current_likes + 1

    else:
        Like.objects.filter(user=user, post=post).delete()
        current_likes = current_likes - 1

    post.likes = current_likes
    post.save()

    return HttpResponseRedirect(reverse('postdetails', args=[post_pk]))
