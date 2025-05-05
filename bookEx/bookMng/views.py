from django.http import HttpResponse, HttpResponseRedirect
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import CreateView
from django.contrib.auth.forms import UserCreationForm
from django.db.models import Avg# Path: bookEx/bookMng/views.py
from .models import MainMenu, Book, Comment, Rating, Favorite
from .forms import BookForm, CommentForm, RatingForm


@login_required(login_url=reverse_lazy('login'))
def search_books(request):
    query = request.GET.get('q', '')  # Get the search query from the URL
    if query:
        books = Book.objects.filter(Q(name__icontains=query))  # Filter books by name
    else:
        books = Book.objects.all()  # Return all books if no query

    for b in books:
        b.pic_path = b.picture.url[14:]

    return render(request, 'bookMng/search_results.html', {
        'item_list': MainMenu.objects.all(),
        'books': books,
        'query': query
    })

@login_required(login_url=reverse_lazy('login'))
def index(request):
    return render(request,
                  'bookMng/index.html',
                  {
                      'item_list': MainMenu.objects.all()
                  }
                  )

def aboutus(request):
    return render(request,
                  'bookMng/aboutus.html',
                  {
                      'item_list': MainMenu.objects.all()
                  }
                  )

@login_required(login_url=reverse_lazy('login'))
def postbook(request):
    submitted = False
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            book = form.save(commit=False)
            try:
                book.username = request.user
            except Exception:
                pass
            book.save()
            return HttpResponseRedirect('/postbook?submitted=True')
    else:
        form = BookForm()
        if 'submitted' in request.GET:
            submitted = True
    return render(request,
                  'bookMng/postbook.html',
                  {
                      'item_list': MainMenu.objects.all(),
                      'form': form,
                      'submitted': submitted
                  }
                  )

@login_required(login_url=reverse_lazy('login'))
def displaybooks(request):
    books = Book.objects.all()
    for b in books:
        b.pic_path = b.picture.url[14:]
    return render(request,
                  'bookMng/displaybooks.html',
                  {
                      'item_list': MainMenu.objects.all(),
                      'books': books
                  }
                  )

@login_required(login_url=reverse_lazy('login'))
def mybooks(request):
    books = Book.objects.filter(username=request.user)
    for b in books:
        b.pic_path = b.picture.url[14:]
    return render(request,
                  'bookMng/mybooks.html',
                  {
                       'item_list': MainMenu.objects.all(),
                       'books': books
                  }
                  )

@login_required(login_url=reverse_lazy('login'))
def book_detail(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    comments = Comment.objects.filter(book=book)  # Fetch comments for the book
    new_comment = None

    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        print(data)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.book = book
            new_comment.author = request.user  # Set the comment author
            new_comment.save()
            return redirect('book_detail', book_id=book.id)
    else:
        comment_form = CommentForm()

    return render(request, 'bookMng/book_detail.html', {
        'item_list': MainMenu.objects.all(),
        'book': book,
        'comments': comments,
        'new_comment': new_comment,
        'comment_form': comment_form
    })

def book_delete(request, book_id):
    book = Book.objects.get(id=book_id)
    book.delete()
    return render(request,
                  'bookMng/book_delete.html',
                  {
                      'item_list': MainMenu.objects.all(),
                      'book': book
                  }
                  )

class Register(CreateView):
    template_name = 'registration/register.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('register-success')

    def form_valid(self, form):
        form.save()
        return HttpResponseRedirect(self.success_url)

@login_required(login_url=reverse_lazy('login'))
def book_detail(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    comments = Comment.objects.filter(book=book)
    comment_form = CommentForm()  # Initialize comment_form here
    rating_form = RatingForm()    # Initialize rating_form here

    if request.method == 'POST':
        if 'comment' in request.POST:
            comment_form = CommentForm(data=request.POST)
            if comment_form.is_valid():
                new_comment = comment_form.save(commit=False)
                new_comment.book = book
                new_comment.author = request.user
                new_comment.save()
                return redirect('book_detail', book_id=book.id)

        elif 'rating' in request.POST:
            rating_form = RatingForm(data=request.POST)
            if rating_form.is_valid():
                score = rating_form.cleaned_data['score']

                try:
                    rating = Rating.objects.get(user=request.user)
                    rating.book = book
                    rating.score = score
                    rating.save()
                except Rating.DoesNotExist:
                    rating = Rating.objects.create(user=request.user, book=book, score=score)


                average = Rating.objects.filter(book=book).aggregate(Avg('score'))['score__avg']
                book.average_rating = average
                book.save()


    return render(request, 'bookMng/book_detail.html', {
        'item_list': MainMenu.objects.all(),
        'book': book,
        'comments': comments,
        'comment_form': comment_form,
        'rating_form': rating_form
    })

@login_required
def add_to_favorites(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    Favorite.objects.get_or_create(user=request.user, book=book)
    return redirect('book_detail', book_id=book_id)

@login_required
def remove_from_favorites(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    Favorite.objects.filter(user=request.user, book=book).delete()
    return redirect('book_detail', book_id=book_id)

@login_required
def view_favorites(request):
    # Fetching the favorited books for the user
    favorites = Favorite.objects.filter(user=request.user).select_related('book')
    favorited_books = [favorite.book for favorite in favorites]

    return render(request, 'bookMng/favorites.html', {
        'item_list': MainMenu.objects.all(),
        'favorites': favorited_books
    })

