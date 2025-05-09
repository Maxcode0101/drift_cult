from django.shortcuts import render, get_object_or_404
from .models import Post

def community_list(request):
    posts = Post.objects.order_by('-created_at')
    return render(request, 'community/community_list.html', {'posts': posts})

def community_detail(request, slug):
    post = get_object_or_404(Post, slug=slug)
    return render(request, 'community/community_detail.html', {'post': post})