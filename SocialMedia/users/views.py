from typing import Any

from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404, HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.template.context_processors import request
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import DetailView, UpdateView

from .forms import ProfileForm, ProfileEditForm
from .models import Profile, Follow

from posts.models import Post

User = get_user_model()


class GetProfileView(LoginRequiredMixin, DetailView):
    # /profile/<slug:username>/
    template_name = "profile.html"
    queryset = Profile.objects.all()
    pk_url_kwarg = "username"

    def get_object(self, queryset=None):
        profile = self.queryset.filter(user__username=self.kwargs.get(self.pk_url_kwarg), user__is_active=True).first()
        if profile is None:
            raise Http404("Not Found")
        return profile

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        response = super().get(request, *args, **kwargs)
        if response.status_code == 200:
            follower_count = Follow.objects.filter(followee__username=self.kwargs["username"]).count()
            followee_count = Follow.objects.filter(follower__username=self.kwargs["username"]).count()
            post_count = Post.objects.filter(user__username=self.kwargs["username"]).count()
            response.context_data["follower_count"] = follower_count
            response.context_data["followee_count"] = followee_count
            response.context_data["post_count"] = post_count
            user_followee = Follow.objects.filter(follower=request.user, followee__username=kwargs["username"])
            if request.user.username != kwargs["username"] and user_followee.exists() is True:
                response.context_data["is_following"] = True
            else:
                response.context_data["is_following"] = False
        return response


class FollowView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        followee_username = kwargs["username"]
        if Follow.objects.filter(follower=request.user, followee__username=followee_username).exists():
            pass
        else:
            followee = User.objects.filter(username=followee_username).first()
            if followee is None:
                raise Http404("Not Found")
            Follow.objects.create(
                followee=followee,
                follower=request.user
            )
        return redirect(reverse_lazy("profile", kwargs={"username": followee_username}))


class UnfollowView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        followee_username = kwargs["username"]
        if Follow.objects.filter(follower=request.user, followee__username=followee_username).exists():
            Follow.objects.filter(follower=request.user, followee__username=followee_username).delete()
        else:
            pass
        return redirect(reverse_lazy("profile", kwargs={"username": followee_username}))

'''
class ProfileEditView(LoginRequiredMixin, UpdateView):
    pk_url_kwarg = "username"
    form_class = ProfileEditForm
    template_name = 'edit_profile.html'
    success_url = "/"

    # success_url = reverse_lazy('post-detail')

    def get(self, request, *args, **kwargs):
        response = super(ProfileEditView, self).get(request, *args, **kwargs)
        # print(response.context_data)
        return response

    def get_queryset(self):
        # print(Post.objects.filter(user=self.request.user))
        profile_user = Profile.objects.filter(user__username=self.kwargs.get(self.pk_url_kwarg))
        return profile_user


    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
'''