from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import permission_required, login_required
from .models import Book
from .forms import BookForm, SearchForm
from .forms import ExampleForm
from django.views.decorators.http import require_http_methods


@permission_required("bookshelf.can_view", raise_exception=True)
def book_list(request):
    form = SearchForm(request.GET or None)
    books = Book.objects.all()

    if form.is_valid():
        q = form.cleaned_data.get("q")
        if q:
            # Use ORM lookup (parameterized) - safe from SQL injection
            books = books.filter(title__icontains=q)

    context = {"books": books, "search_form": form}
    return render(request, "bookshelf/book_list.html", context)


@permission_required("bookshelf.can_create", raise_exception=True)
@require_http_methods(["GET", "POST"])
def book_create(request):
    if request.method == "POST":
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("book_list")
    else:
        form = BookForm()
    return render(request, "bookshelf/form_example.html", {"form": form})


@permission_required("bookshelf.can_edit", raise_exception=True)
@require_http_methods(["GET", "POST"])
def book_edit(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == "POST":
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return redirect("book_list")
    else:
        form = BookForm(instance=book)
    return render(request, "bookshelf/form_example.html", {"form": form, "book": book})


@permission_required("bookshelf.can_delete", raise_exception=True)
@require_http_methods(["POST"])
def book_delete(request, pk):
    book = get_object_or_404(Book, pk=pk)
    book.delete()
    return redirect("book_list")
