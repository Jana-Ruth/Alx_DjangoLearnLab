from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import CreateView, UpdateView, DeleteView
from .models import Post, Comment, Tag
from .forms import CommentForm
from .forms import PostForm
from django.db.models import Q
from .forms import RegisterForm, UserUpdateForm, ProfileUpdateForm

def register(request):
    """
    Handle user registration. If successful, logs the user in and redirects to profile.
    """
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # optional: auto-login after registration
            messages.success(request, "Registration successful. Welcome!")
            return redirect('profile')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = RegisterForm()
    return render(request, 'blog/register.html', {'form': form})


@login_required
def profile(request):
    """
    View and edit user profile. Handles user and profile forms.
    """
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, "Your profile has been updated.")
            return redirect('profile')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }
    return render(request, 'blog/profile.html', context)

# List view: public
class PostListView(ListView):
    model = Post
    template_name = 'blog/post_list.html'  # templates/blog/post_list.html
    context_object_name = 'posts'
    paginate_by = 10  # optional
    
    


# Detail view: public
class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'  # templates/blog/post_detail.html
    context_object_name = 'post'


# Create view: only authenticated users
class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'  # templates/blog/post_form.html

    def form_valid(self, form):
        # set author before saving
         form.instance.author = self.request.user
         tags = form.cleaned_data.get('tags_field', [])
         response = super().form_valid(form)  # saves Post
         # attach tags (create if needed)
         for tag_name in tags:
            tag_obj, _ = Tag.objects.get_or_create(name=tag_name)
            self.object.tags.add(tag_obj)
         return response
        


# Update view: only author can edit
class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'
    
    def form_valid(self, form):
        tags = form.cleaned_data.get('tags_field', [])
        response = super().form_valid(form)
        # update tags: clear existing and set new ones
        self.object.tags.clear()
        for tag_name in tags:
            tag_obj, _ = Tag.objects.get_or_create(name=tag_name)
            self.object.tags.add(tag_obj)
        return response

    def test_func(self):
        post = self.get_object()
        return post.author == self.request.user


# Delete view: only author can delete
class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'blog/post_confirm_delete.html'
    success_url = reverse_lazy('post-list')

    def test_func(self):
        post = self.get_object()
        return post.author == self.request.user
    
# Create a comment tied to a post (URL will include post_pk)
class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm
    template_name = 'blog/comment_form.html'  # optional standalone template

    def form_valid(self, form):
        post = get_object_or_404(Post, pk=self.kwargs.get('post_pk'))
        form.instance.author = self.request.user
        form.instance.post = post
        return super().form_valid(form)

    def get_success_url(self):
        return self.object.post.get_absolute_url()

# View that lists posts by a tag (optional - helpful for /tags/<tag_name>/)
class TagPostListView(ListView):
    model = Post
    template_name = 'blog/posts_by_tag.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        tag_name = self.kwargs.get('tag_name')
        return Post.objects.filter(tags__name__iexact=tag_name).distinct()
    
    def search_posts(request):
        query = request.GET.get('q')  # the text from the search bar
        results = []

        if query:
            results = Post.objects.filter(
                Q(title__icontains=query) |            # ✅ check title
                Q(content__icontains=query) |          # ✅ check content
                Q(tags__name__icontains=query)         # ✅ check tags
        ).distinct()

        return render(request, 'blog/search_results.html', {'query': query, 'results': results})


class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Comment
    form_class = CommentForm
    template_name = 'blog/comment_form.html'

    def test_func(self):
        comment = self.get_object()
        return comment.author == self.request.user

    def get_success_url(self):
        return self.object.post.get_absolute_url()


class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment
    template_name = 'blog/comment_confirm_delete.html'

    def test_func(self):
        comment = self.get_object()
        return comment.author == self.request.user

    def get_success_url(self):
        return self.object.post.get_absolute_url()    