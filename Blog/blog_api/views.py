from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from .models import Post


class BlogList(ListView):
    queryset = Post.objects.all().order_by('-created_at')
    template_name = 'blog_detail.html'
    context_object_name = 'blog_list'


class BlogDetails(DetailView):
    model = Post
    template_name = "blog_detail.html"
    context_object_name = 'blog'


class BlogCreateView(LoginRequiredMixin, CreateView):
    model = Post
    template_name = 'blog_create.html'
    fields = ['title', 'thumbnail', 'author', 'description', 'body']


class BlogUpdateView(LoginRequiredMixin, UpdateView):
    model = Post
    template_name = "blog_edit.html"
    fields = ["title", "thumbnail", "author", "description", "body"]


class BlogDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = 'blog_delete.html'
    success_url = reverse_lazy('home')
    context_object_name = 'blog'
