from django.shortcuts import render
from django.views.generic import ListView
from .models import Book, Author, BookInstance


class BookListView(ListView):
    model = Book
    context_object_name = 'books'


def index(request):
    text_head = 'На нашем сайте вы можете получть книги в электроном виде' # Словарь для передачи данных в шаблон

    # данные о книгах и их количестве
    books = Book.objects.all()
    num_books = Book.objects.all().count()

    # данные об экземлярах книг в БД
    num_instances = BookInstance.objects.all().count()

    # Доступные книги (со статусом = "На складе")
    num_instances_available = BookInstance.objects.filter(status__exact=2).count()

    # Данные об авторах книг
    authors = Author.objects
    num_authors = Author.objects.count()

    context = {'text_head': text_head,
               'books':books, 'num_books':num_books, 'num_instances':num_instances,
               'num_instances_available':num_instances_available, 'authors':authors,
               'num_authors':num_authors}
    # передача словаря context c данными в шаблон
    return render(request, 'catalog/index.html', context)