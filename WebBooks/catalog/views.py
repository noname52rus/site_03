from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Book, Author, BookInstance


class BookListView(ListView):
    model = Book
    context_object_name = 'books'
    paginate_by = 3


class BookDetailView(DetailView):
    model = Book
    context_object_name = 'book'


class AuthorListView(ListView):
    model = Author
    paginate_by = 4


class AuthorDetailView(DetailView):
    model = Author


def contact(request):
    text_head = 'Сведения о компании'
    name = 'ООО "Интелектуальные информационные решения"'
    address = 'Москва, ул. Планерная, д. 20, к. 1'
    email = 'qwe@mail.ru'
    tel = '89433242342'
    context = {'text_head':text_head, 'name':name, 'address':address, 'email':email, 'tel':tel}
    return render(request, 'catalog/contact.html', context)


def about(request):
    text_head = 'Сведения о компании'
    name = 'ООО "Интелектуальные информационные решения"'
    rab1 = 'Разработка приложений на основе систем искусственного интелекта'
    rab2 = 'Распознавание объектов дорожной инфраструктуры'
    rab3 = 'Создание графических АРТ-объектов на основе систем искусственного интелпекта'
    rab4 = 'Создание цифровых интерактивных книг, учебных пособий автоматизированных обучащих систем'
    context = {'text_head':text_head, 'name':name, 'rab1':rab1,
               'rab2':rab2, 'rab3':rab3, 'rab4':rab4}
    # передача словаря context c данными в шаблон
    return render(request, 'catalog/about.html', context)


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

    # Чисол посещений этого view, подсчитанное в переменной session
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1

    context = {'text_head': text_head,
               'books':books, 'num_books':num_books, 'num_instances':num_instances,
               'num_instances_available':num_instances_available, 'authors':authors,
               'num_authors':num_authors, 'num_visits':num_visits}
    # передача словаря context c данными в шаблон
    return render(request, 'catalog/index.html', context)