from django.http import HttpResponse, HttpResponseRedirect
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import CreateView
from django.contrib.auth.forms import UserCreationForm
from django.db.models import Avg
from .models import MainMenu, Book, Comment, Rating, Favorite
from .forms import BookForm, CommentForm, RatingForm
from django.contrib.auth import get_user_model


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
            print("comment_form is valid")
            new_comment = Comment()#comment_form.save(commit=False)
            new_comment = comment_form.save(commit=False)
            new_comment.book = book
            new_comment.author = request.user  # Set the comment author
            new_comment.text = comment_form.cleaned_data['text']
            new_comment.save()
            comments = Comment.objects.filter(book=book)
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
'''
@login_required(login_url=reverse_lazy('login'))
def book_detail(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    comments = Comment.objects.filter(book=book)
    comment_form = CommentForm()  # Initialize comment_form here
    rating_form = RatingForm()    # Initialize rating_form here
    new_comment = Comment()

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
                rating = rating_form.save(commit=False)
                rating.book = book
                rating.user = request.user
                rating.save()
                # Update average rating
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
'''

@login_required(login_url=reverse_lazy('login'))
def book_detail(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    comments = Comment.objects.filter(book=book)
    comment_form = CommentForm()
    rating_form = RatingForm()

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

                rating, created = Rating.objects.get_or_create(
                    user=request.user,
                    book=book,
                    defaults={'score': score}
                )
                if not created:
                    rating.score = score
                    rating.save()

                # 更新平均分
                average = Rating.objects.filter(book=book).aggregate(Avg('score'))['score__avg']
                book.average_rating = average
                book.save()

                # ⚡关键：打分后，redirect到自己，这样会重新加载最新的book数据
                return redirect('book_detail', book_id=book.id)

    # 打开页面时也重新算一次最新平均分，确保每次打开都是最新
    average = Rating.objects.filter(book=book).aggregate(Avg('score'))['score__avg']
    if average:
        book.average_rating = average
    else:
        book.average_rating = 0

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

@login_required(login_url=reverse_lazy('login'))
def requestbook(request):
    # return HttpResponse("<h1 align='center'>Hello World</h1>")
    # return render(request, 'bookMng/displaybooks.html')
    return render(request,
                  'bookMng/requestbook.html',
                  {
                      'item_list': MainMenu.objects.all()
                  }
                  )

@login_required(login_url=reverse_lazy('login'))
def user_detail(request, user_id):
    User = get_user_model()
    user = User.objects.get(id=user_id)
    return render(request,
                  'bookMng/user_detail.html',
                  {
                      'item_list': MainMenu.objects.all(),
                      'user': user
                  })

@login_required(login_url=reverse_lazy('login'))
def displayusers(request):
    User = get_user_model()
    users = User.objects.all()
    return render(request,
                  'bookMng/displayusers.html',
                  {
                      'item_list': MainMenu.objects.all(),
                      'users': users
                  })

@login_required(login_url=reverse_lazy('login'))
def myprofile(request):
    User = get_user_model()
    user = request.user
    return render(request,
                  'bookMng/myprofile.html',
                  {
                      'item_list': MainMenu.objects.all(),
                      'user': user
                  })