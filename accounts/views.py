from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect, Http404, JsonResponse
from .models import UserProfile
from .forms import ProfileSettingForm, AvatarForm
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy


@login_required
def user_subscribe(request):
    if request.method == 'POST' and request.is_ajax():
        user_id = request.POST['user_id']
        user = get_object_or_404(User, pk=user_id)

        if request.POST['action'] == 'subscribe':
            request.user.profile.followers.add(user)
            message = f'You subscribe {user.username}!'
            return JsonResponse({'message': message,
                                 'user_id': user_id},
                                status=200)
        elif request.POST['action'] == 'unsubscribe':
            if request.user.profile.followers.filter(id=user_id):
                request.user.profile.followers.remove(user)
                message = f'You Unsubscribe from {user.username}!'
                return JsonResponse({'message': message,
                                     'user_id': user_id},
                                    status=200)
    raise Http404


@login_required
def user_settings(request):
    """
    Change user profile fields
    """
    if request.method == 'POST':
        settings_form = ProfileSettingForm(request.POST, request.FILES)
        if settings_form.is_valid():
            settings_form = settings_form.cleaned_data

            request.user.first_name = settings_form['first_name']
            request.user.last_name = settings_form['last_name']
            request.user.username = settings_form['user_name']
            request.user.profile.bio = settings_form['bio']
            request.user.profile.date_of_birth = settings_form['date_of_birth']
            request.user.profile.is_finnish_registration = True
            request.user.profile.save()
            request.user.save()

            messages.success(request, f'Profile changed!')
            return HttpResponseRedirect(request.path_info)
    else:
        settings_form = ProfileSettingForm(initial={'first_name': request.user.first_name,
                                                    'last_name': request.user.last_name,
                                                    'user_name': request.user.username,
                                                    'bio': request.user.profile.bio,
                                                    'date_of_birth': request.user.profile.date_of_birth})
    return render(request,
                  'accounts/settings.html',
                  {'form': settings_form})


@login_required
def user_avatar(request):
    """
    Upload new avatar
    """
    if request.method == 'POST':
        form = AvatarForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            messages.success(request, f'Avatar Changed!')
            return redirect('posts:feed')
    else:
        form = AvatarForm()
    return render(request,
                  'accounts/avatar.html',
                  {'form': form})
