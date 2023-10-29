from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from datetime import date


class Author(models.Model):
    first_name = models.CharField(max_length=120, verbose_name='Имя автора', help_text='Введите Имя автора')
    last_name = models.CharField(max_length=120, verbose_name='Фамилия автора', help_text='Введите Фамилию автора')
    date_of_birth = models.DateField(help_text='Введите дату рождения', verbose_name='Дата рождения', null=True,
                                     blank=True)
    about = models.TextField(verbose_name='Сведения об авторе', help_text='Введите Сведения об авторе')
    photo = models.ImageField(upload_to='images', help_text='Загрузите фото автора', verbose_name='Фото автора',
                              null=True, blank=True)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return self.last_name

    def get_absolute_url(self):
        return reverse('author-detail', args=[str(self.id)])


class Publisher(models.Model):
    name = models.CharField(max_length=20, verbose_name='Издательство', help_text='Введите наименование издательства')

    def __str__(self):
        return self.name


class Language(models.Model):
    name = models.CharField(max_length=20, verbose_name='Язык книги', help_text='Введите язык книги')

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length=200, verbose_name='Жанр книги', help_text='Введите жанр книги')

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=200,
                             help_text='Введите название книги',
                             verbose_name='Название книги')
    genre = models.ForeignKey('Genre', on_delete=models.CASCADE,
                              help_text='Выберите жанр книги',
                              verbose_name='Жанр книги', null=True)
    language = models.ForeignKey('Language', on_delete=models.CASCADE,
                                 help_text='Выберите язык книги',
                                 verbose_name='Язык книги', null=True)
    publisher = models.ForeignKey('Publisher', on_delete=models.CASCADE,
                                  help_text='Выберите издательство',
                                  verbose_name='Издательство', null=True)
    year = models.CharField(max_length=4,
                            help_text='Введите год издания',
                            verbose_name='Год издания')
    author = models.ManyToManyField('Author',
                                    help_text='Выберите автора книги',
                                    verbose_name='Автор книги')
    summary = models.TextField(max_length=1200,
                               help_text='Введите краткое описание книги',
                               verbose_name='Аннотация книги')
    isbn = models.CharField(max_length=13,
                            help_text='Должно содержать 13 символов',
                            verbose_name='ISBN книги')
    price = models.DecimalField(max_digits=7, decimal_places=2,
                                help_text='Введите цену книги',
                                verbose_name='Цена (руб.)')
    photo = models.ImageField(upload_to='images',
                              help_text='Введите изображение обложки',
                              verbose_name='Изображение обложки')

    class Meta:
        ordering = ['-id']

    def display_author(self):
        return ', '.join([author.last_name for author in self.author.all()])
    display_author.short_description = 'Авторы'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('book-detail', args=[str(self.id)])


class Status(models.Model):
    name = models.CharField(max_length=20, help_text='Введите статус экземпляра книги',
                            verbose_name='Статус экземпляра книги')

    def __str__(self):
        return self.name


# экземпляр книги
class BookInstance(models.Model):
    book = models.ForeignKey('Book', on_delete=models.CASCADE, null=True)
    inv_nom = models.CharField(max_length=20, null=True,
                               help_text='Введите инвентарный номер экземпляра', verbose_name='Инвентарный номер')
    status = models.ForeignKey('Status', on_delete=models.CASCADE, null=True,
                               help_text='Изменить состояние экземпляра', verbose_name='Статус экземпляра книги')
    due_back = models.DateField(null=True, blank=True,
                                help_text='Введите конец срока статуса', verbose_name='Дата окончания статуса')
    borrower = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Заказчик",
                                 help_text="Выберите заказчика книги")
    objects = models.Manager

    @property
    def is_overdue(self):
        if self.due_back and date.today() > self.due_back:
            return True
        return False

    class Meta:
        ordering = ['due_back']

    def __str__(self):
        return '%s %s %s' % (self.inv_nom, self.book, self.status)


