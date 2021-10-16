from django.contrib.auth import authenticate, login, get_user_model, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.template import loader
from django.urls import resolve
from django.views.decorators.http import require_POST
from django.views.generic import FormView, UpdateView, DetailView

from content.models import Post
from relation.models import Relation
from user.forms import RegistrationForm, LoginForm, SignupForm, ChangePasswordForm, EditProfileForm

User = get_user_model()


#   #   #      #   #   #      #   #   #  register first method: class base  #   #   ##   #   ###   #   #   #   #
class RegisterView(FormView):
    form_class = RegistrationForm
    template_name = 'user/register.html'
    success_url = '/'

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


#   #   #   # #   #   #       #  #   register second method: function base #   #   ##   #   ##   #   #
# @require_POST
def sign_up(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            User.objects.create_user(username=username, email=email, password=password)
            return redirect('myfriend')
    else:
        form = SignupForm()

    context = {
        'form': form,
    }

    return render(request, 'signup.html', context)


# @require_POST
@login_required
def password_change(request):
    user = request.user
    if request.method == 'POST':
        form = ChangePasswordForm(request.POST)
        if form.is_valid():
            new_password = form.cleaned_data.get('new_password')
            user.set_password(new_password)
            user.save()
            update_session_auth_hash(request, user)
            return redirect('change_password_done')
    else:
        form = ChangePasswordForm(instance=user)

    context = {
        'form': form,
    }

    return render(request, 'change_password.html', context)


def password_change_done(request):
    return render(request, 'change_password_done.html')


class LoginView(FormView):
    form_class = LoginForm
    template_name = 'user/login.html'
    success_url = '/'

    def form_valid(self, form):
        login(self.request, form.cleaned_data['user'])
        return super().form_valid(form)


class ProfileUpdateView(UpdateView):
    model = User
    fields = ('username', 'avatar', 'bio', 'website')
    template_name = 'user/profile.html'
    success_url = '/'

    def get_object(self, queryset=None):
        return self.request.user


class ProfileDetailView(DetailView):
    model = User
    slug_url_kwarg = 'username'
    slug_field = 'username'
    # for class base
    # template_name = 'user/profile.html'

    # for function base
    template_name = 'profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.get_object()
        context['posts_count'] = user.posts.count()
        context['followers_count'] = user.follower.count()
        context['followings_count'] = user.following.count()
        # context['likes'] = Post.likes.objects.all()
        context['is_following'] = Relation.objects.filter(following=self.request.user, follower=user).exists()

        return context


@login_required
def EditProfile(request):
    user = request.user
    profile = User.objects.get(username=user)
    BASE_WIDTH = 400

    if request.method == 'POST':
        form = EditProfileForm(request.POST, request.FILES)
        if form.is_valid():
            profile.avatar = form.cleaned_data.get('avatar')
            profile.username = form.cleaned_data.get('username')
            profile.website = form.cleaned_data.get('url')
            # profile.location = form.cleaned_data.get('location')
            profile.bio = form.cleaned_data.get('bio')
            profile.save()
            return redirect('myfriend')
    else:
        form = EditProfileForm()

    context = {
        'form': form,
    }

    return render(request, 'edit_profile.html', context)


# function base
@login_required
def search(request):
    query = request.GET.get("q")
    context = {}

    if query:
        users = User.objects.filter(username__icontains=query)

        # Pagination
        paginator = Paginator(users, 7)
        page_number = request.GET.get('page')
        users_paginator = paginator.get_page(page_number)

        context = {
            'users': users_paginator,
        }

    template = loader.get_template('search.html')

    return HttpResponse(template.render(context, request))

# # class base
# class SearchResultsView(ListView):
#     model = User
#     template_name = 'search_people.html'
#
#     def get_queryset(self):
#         query = self.request.GET.get('p')
#         return User.objects.filter(user__username__icontains=query)
