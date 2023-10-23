from django.http import HttpResponseRedirect, HttpResponseNotFound
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView, ListView
from django.views import generic
from django.urls import reverse
from .forms import Form_add_author, Form_edit_author
from .models import Book, Author, BookInstance


class LoanedBooksByUserListView(LoginRequiredMixin, generic.ListView):
    #  Универсальный класс представления книг,
    #  находящихся в заказе у текущего пользователя
    model = BookInstance
    template_name = 'catalog/bookinstance_list_borrowed_user.html'
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(
            borrower=self.request.user).filter(
            status__exact='2').order_by('due_back')


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
    context = {'text_head': text_head, 'name': name, 'address': address, 'email': email, 'tel': tel}
    return render(request, 'catalog/contact.html', context)


def about(request):
    text_head = 'Сведения о компании'
    name = 'ООО "Интелектуальные информационные решения"'
    rab1 = 'Разработка приложений на основе систем искусственного интелекта'
    rab2 = 'Распознавание объектов дорожной инфраструктуры'
    rab3 = 'Создание графических АРТ-объектов на основе систем искусственного интелпекта'
    rab4 = 'Создание цифровых интерактивных книг, учебных пособий автоматизированных обучащих систем'
    context = {'text_head': text_head, 'name': name, 'rab1': rab1,
               'rab2': rab2, 'rab3': rab3, 'rab4': rab4}
    # передача словаря context c данными в шаблон
    return render(request, 'catalog/about.html', context)


def index(request):
    text_head = 'На нашем сайте вы можете получть книги в электроном виде'  # Словарь для передачи данных в шаблон

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
               'books': books, 'num_books': num_books, 'num_instances': num_instances,
               'num_instances_available': num_instances_available, 'authors': authors,
               'num_authors': num_authors, 'num_visits': num_visits}
    # передача словаря context c данными в шаблон
    return render(request, 'catalog/index.html', context)


# вызов страницы для редактирования авторов
def edit_authors(request):
    author = Author.objects.all()
    context = {'author': author}
    return render(request, "catalog/edit_authors.html", context)


# Создание нового автора в БД
def add_author(request):
    if request.method == 'POST':
        form = Form_add_author(request.POST, request.FILES)
        if form.is_valid():
            # получить данные из формы
            first_name = form.cleaned_data.get("first_name")
            last_name = form.cleaned_data.get("last_name")
            date_of_birth = form.cleaned_data.get("date_of_birth")
            about = form.cleaned_data.get("about")
            photo = form.cleaned_data.get("photo")
            # создать объект для записи в БД
            obj = Author.objects.create(
                first_name=first_name,
                last_name=last_name,
                date_of_birth=date_of_birth,
                about=about,
                photo=photo)
            obj.save()
            # загрузить страницу со списком авторов
            return HttpResponseRedirect(reverse('authors-list'))
    else:
        form = Form_add_author()
        context = {"form": form}
        return render(request, "catalog/authors_add.html", context)


# удаление авторов из БД
def delete(request, id):
    try:
        author = Author.objects.get(id=id)
        author.delete()
        return HttpResponseRedirect("/edit_authors/")
    except:
        return HttpResponseNotFound("<h2>Автор не найден</h2>")


# изменение данных об авторах книг
def edit_author(request, id):
    author = Author.objects.get(id=id)
    if request.method == "POST":
        instance = Author.objects.get(pk=id)
        form = Form_edit_author(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("/edit_authors/")
    else:
        form=Form_edit_author(instance=author)
        content = {"form": form}
        return render(request, "catalog/edit_author.html", content)
