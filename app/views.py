from django.http import HttpResponse, HttpRequest
from django.shortcuts import render
from . import models
from django.core.paginator import Paginator

def get_paginator_data(list_data, per_page, curr_page):
    paginator = Paginator(list_data, per_page)
    num_pages = paginator.num_pages
    if curr_page < 0 or curr_page >= num_pages:
        return (0, [])
    page = paginator.page(curr_page + 1)
    paginator_data = {
        'enabled_previous': page.has_previous(),
        'page_start': 1,
        'prev_prev_page': curr_page - 1,
        'prev_page': curr_page,
        'page': curr_page + 1,
        'next_page': curr_page + 2,
        'next_next_page': curr_page + 3,
        'page_prev_end': num_pages - 1,
        'page_end': num_pages,
        'enabled_next': page.has_next()
    }
    return (page, paginator_data)


def index(request: HttpRequest):
    input_page = request.GET.get('page', '0')
    if not input_page.isdigit():
        return HttpResponse(status=404)
    input_page = int(input_page)

    page, paginator_data = get_paginator_data(models.QUESTIONS, 10, input_page)
    if not page:
        return HttpResponse(status=404)

    context = {'questions': page.object_list, 'paginator': paginator_data, 'curr_url': 'index'}
    return render(request, 'index.html', context=context)


def hot(request: HttpRequest):
    input_page = request.GET.get('page', '0')
    if not input_page.isdigit():
        return HttpResponse(status=404)
    input_page = int(input_page)

    page, paginator_data = get_paginator_data(models.QUESTIONS, 10, input_page)
    if not page:
        return HttpResponse(status=404)

    context = {'questions': page.object_list, 'paginator': paginator_data, 'curr_url': 'hot'}
    return render(request, 'hot.html', context=context)

def tag(request: HttpRequest, tag_name: str):

    input_page = request.GET.get('page', '0')
    if not input_page.isdigit():
        return HttpResponse(status=404)
    input_page = int(input_page)


    page, paginator_data = get_paginator_data(models.QUESTIONS, 10, input_page)
    if not page:
        return HttpResponse(status=404)

    context = {'tag': tag_name, 'questions': page.object_list, 'paginator': paginator_data, 'curr_url': 'tag'}
    return render(request, 'tag.html', context=context)


def ask(request: HttpRequest):
    return render(request, 'ask.html')


def login(request: HttpRequest):
    return render(request, 'login.html')


def question(request: HttpRequest, question_id: int):
    if question_id >= len(models.QUESTIONS):
        return HttpResponse(status=404)
    
    question_item = models.QUESTIONS[question_id]

    input_page = request.GET.get('page', '0')
    if not input_page.isdigit():
        return HttpResponse(status=404)
    input_page = int(input_page)

    page, paginator_data = get_paginator_data(question_item['answers'], 5, input_page)
    if not page:
        return HttpResponse(status=404)

    context = {'question': question_item, 'id': question_id, 'answers': page.object_list, 'paginator': paginator_data, 'curr_url': 'question'}
    return render(request, 'question.html', context=context)


def registration(request: HttpRequest):
    return render(request, 'registration.html')


def settings(request: HttpRequest):
    return render(request, 'settings.html')
