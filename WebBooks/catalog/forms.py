from django import forms
from datetime import date
from .models import Author, Book


#  форма для добавления в БД новых авторов
class Form_add_author(forms.Form):
    first_name = forms.CharField(label="Имя автора")
    last_name = forms.CharField(label="Фамилия автора")
    date_of_birth = forms.DateField(
        label="Дата рождения",
        initial=format(date.today()),
        widget=forms.widgets.DateInput(attrs={'type': 'date'}))
    about = forms.CharField(label="Сведения об авторе", widget=forms.Textarea)
    photo = forms.ImageField(label="Фото автора")


#  Форма для изменения сведений об авторах
class Form_edit_author(forms.ModelForm):
    class Meta:
        model = Author
        fields = '__all__'


#  Форма для изменения сведений о книгах
class Book_model_form(forms.ModelForm):
    fields = 'about'
    labels = {'about': ('Аннотация'), }
    help_texts = {'about': ("Не более 1000 символов"), }

    class Meta:
        model = Book
        fields = '__all__'

