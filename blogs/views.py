from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import Http404

from blogs.models import BlogPost
from blogs.forms import PostForm

def index(request):
    """For when users are not logged in"""
    return render(request, 'blogs/index.html')

@login_required
def homepage(request):
    """User's homepage."""
    posts = BlogPost.objects.filter(owner=request.user).order_by('date_added')
    context = {'posts': posts}
    return render(request, 'blogs/homepage.html', context)

@login_required
def new_post(request):
    """Adds a new blog post."""
    if request.method != 'POST':
        # No data submitted; create a blank form.
        form = PostForm()
    else:
        # POST data submitted; process data.
        form = PostForm(data=request.POST)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.owner = request.user
            new_post.save()
            return redirect('blogs:homepage') # redirects to the homepage.

    # Display a blank or invalid form.
    context = {'form': form}
    return render(request, 'blogs/new_post.html', context)

@login_required
def edit_post(request, post_id):
    """Edit an existing blog post"""
    post = get_object_or_404(BlogPost, id=post_id)
    # Make sure the post belongs to the user
    check_post_owner(post.owner, request)


    if request.method != 'POST':
        # Initail reqiest; pre-fill form with the current entry.
        form = PostForm(instance=post)
    else:
        # POST data submitted; process data.
        form = PostForm(instance=post, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('blogs:homepage')
    
    context = {'post': post, 'form': form}
    return render(request, 'blogs/edit_post.html', context)

def check_post_owner(owner, request):
    if owner != request.user:
        raise Http404