from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from .models import Post
from .forms import PostForm

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
        return super().form_valid(form)


# Update view: only author can edit
class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'

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