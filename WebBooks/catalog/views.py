from django.shortcuts import render

def index(request):
    text_head = 'Это загаловок страницы сайта' # Словарь для передачи данных в шаблон
    text_body = 'Это содержимое главной страницы сайта'
    context = {'text_head': text_head, 'text_body': text_body}
    # передача словаря context c данными в шаблон
    return render(request, 'catalog/index.html', context)