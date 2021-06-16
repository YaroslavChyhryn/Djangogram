from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import UserPassesTestMixin
from django.http import JsonResponse, HttpResponseRedirect, HttpResponseForbidden, Http404
from django.views import generic
from django.views.generic.edit import DeleteView
from .forms import PostCreateForm, NewCommentForm
from .models import Post
from django.contrib import messages
from functools import wraps
from django.urls import reverse_lazy
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def users_that_finish_registration(function):

    @wraps(function)
    def wrap(request, *args, **kwargs):
        if request.user.profile.is_finnish_registration:
            return function(request, *args, **kwargs)
        else:
            messages.info(request, 'Закончите регистрацию.')
            return redirect('accounts:settings')

    return wrap


class FinishRegistrationMixin(UserPassesTestMixin):
    # redirect to setting page if user has not finished registration
    login_url = reverse_lazy('accounts:settings')

    def handle_no_permission(self):
        if self.raise_exception or self.request.user.is_authenticated:
            messages.info(self.request, 'Закончите регистрацию.')
            return redirect('accounts:settings')
        return redirect('account_login')

    def test_func(self):
        if self.request.user.is_authenticated:
            return self.request.user.profile.is_finnish_registration is True
        return False


class ExploreView(FinishRegistrationMixin, generic.ListView):
    """
    All posts
    """
    template_name = 'posts/feed.html'
    context_object_name = 'posts'

    def get_queryset(self):
        return Post.objects.order_by('-created')


@login_required
@users_that_finish_registration
def post_create(request):
    if request.method == 'POST':
        form = PostCreateForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = User.objects.get(pk=request.user.id)
            post.save()
            messages.success(request, f'Post Created!')
            return redirect('posts:feed')
    else:
        form = PostCreateForm()
    return render(request,
                  'posts/create.html',
                  {'form': form})


@login_required
@users_that_finish_registration
def post_delete(request):
    if request.method == "POST" and request.is_ajax():
        uuid = request.POST['post_uuid']
        post = get_object_or_404(Post, uuid=uuid)

        if post.author.id is not request.user.id:
            messages.error(request, f'You trying to delete not your post!')
            return HttpResponseForbidden()

        post.delete()
        message = 'Post has been deleted!'
        return JsonResponse({'message': message,
                             'post_uuid': uuid},
                            status=200)
    else:
        raise Http404


@login_required
@users_that_finish_registration
def post_like(request):
    if request.method == "POST" and request.is_ajax():
        uuid = request.POST['post_uuid']
        post = Post.objects.get(uuid=uuid)

        if request.POST['action'] == 'like':
            post.likes.add(request.user)
            message = 'You liked this'
            like_count = post.total_likes
            return JsonResponse({'message': message,
                                 'like_count': like_count,
                                 'post_uuid': uuid},
                                status=200)
        elif request.POST['action'] == 'dislike':
            if post.likes.filter(id=request.user.id):
                post.likes.remove(request.user)
                message = 'You disliked this'
                like_count = post.total_likes
                return JsonResponse({'message': message,
                                     'like_count': like_count,
                                     'post_uuid': uuid},
                                    status=200)
    raise Http404


@login_required
@users_that_finish_registration
def feed(request):
    """
    Show request.user posts and post from users that this user is following
    """
    followers = request.user.profile.followers.values_list('pk', flat=True)
    posts = Post.objects.filter(author_id__in=followers)

    return render(request,
                  'posts/feed.html',
                  {'posts': posts})


@login_required
@users_that_finish_registration
def user_profile(request, slug):
    """
    Show user profile page with his posts and additional info from user.profile
    """
    posts = Post.objects.filter(author__username=slug)

    following = request.user.profile.followers.filter(username=slug)
    return render(request,
                  'posts/profile.html',
                  {'posts': posts,
                   'author': User.objects.get(username=slug),
                   'following': following})


@login_required
@users_that_finish_registration
def post_view(request, uuid):
    """
    DetailView for post
    """
    post = get_object_or_404(Post, uuid=uuid)

    allcomments = post.comments.filter(status=True)
    page = request.GET.get('page', 1)

    paginator = Paginator(allcomments, 10)
    try:
        comments = paginator.page(page)
    except PageNotAnInteger:
        comments = paginator.page(1)
    except EmptyPage:
        comments = paginator.page(paginator.num_pages)

    user_comment = None

    if request.method == 'POST':
        comment_form = NewCommentForm(request.POST)
        if comment_form.is_valid():
            user_comment = comment_form.save(commit=False)
            user_comment.post = post
            user_comment.user = request.user
            user_comment.save()
            return HttpResponseRedirect(post.get_absolute_url())
    else:
        comment_form = NewCommentForm()
    return render(request,
                  'posts/detail.html',
                  {'post': post,
                   'comments': user_comment,
                   'comments': comments,
                   'comment_form': comment_form,
                   'allcomments': allcomments})
