from django.http import HttpResponse, HttpRequest, HttpResponseBadRequest
from django.shortcuts import render, redirect
from . import models
from django.core.paginator import Paginator
from app.models import *
from app.forms import *
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login as auth_login, logout as auth_logout

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

    QUESTIONS = Question.objects.get_new_questions()
    page, paginator_data = get_paginator_data(QUESTIONS, 10, input_page)
    if not paginator_data:
        return HttpResponse(status=404)
    
    TAGS = Tag.objects.top_of_tags()
    MEMBERS = Profile.objects.top_of_profiles()

    context = {'curr_user': request.user, 'questions': page.object_list, 'request': request,
        'paginator': paginator_data, 'curr_url': 'index', 'tags': TAGS, 'members': MEMBERS}
    return render(request, 'index.html', context=context)


def hot(request: HttpRequest):
    input_page = request.GET.get('page', '0')
    if not input_page.isdigit():
        return HttpResponse(status=404)
    input_page = int(input_page)

    QUESTIONS = Question.objects.get_hot_questions()
    page, paginator_data = get_paginator_data(QUESTIONS, 10, input_page)
    if not paginator_data:
        return HttpResponse(status=404)
    
    TAGS = Tag.objects.top_of_tags()
    MEMBERS = Profile.objects.top_of_profiles()

    context = {'curr_user': request.user, 'questions': page.object_list, 'request': request,
        'paginator': paginator_data, 'curr_url': 'hot', 'tags': TAGS, 'members': MEMBERS}
    return render(request, 'hot.html', context=context)


def tag(request: HttpRequest, tag_name: str):
    input_page = request.GET.get('page', '0')
    if not input_page.isdigit():
        return HttpResponse(status=404)
    input_page = int(input_page)

    try:
        QUESTIONS = Tag.objects.get_questions_by_tag(tag_name)
    except:
        return HttpResponseBadRequest()

    page, paginator_data = get_paginator_data(QUESTIONS, 10, input_page)
    if not paginator_data:
        return HttpResponse(status=404)
    
    TAGS = Tag.objects.top_of_tags()
    MEMBERS = Profile.objects.top_of_profiles()

    context = {'curr_user': request.user, 'tag': tag_name, 'request': request, 'questions': page.object_list,
        'paginator': paginator_data, 'curr_url': 'tag', 'tags': TAGS, 'members': MEMBERS}
    return render(request, 'tag.html', context=context)


@login_required
def ask(request: HttpRequest):
    TAGS = Tag.objects.top_of_tags()
    MEMBERS = Profile.objects.top_of_profiles()

    context = {'curr_user': request.user, 'request': request, 'curr_url': 'ask', 'tags': TAGS,
        'members': MEMBERS}
    return render(request, 'ask.html', context=context)


def question(request: HttpRequest, question_id: int):

    try:
        question_item = Question.objects.get_question_by_id(question_id)
    except:
        return HttpResponseBadRequest()
    
    input_page = request.GET.get('page', '0')
    if not input_page.isdigit():
        return HttpResponse(status=404)
    input_page = int(input_page)

    ANSWERS = question_item.get_answers()
    TAGS = Tag.objects.top_of_tags()
    MEMBERS = Profile.objects.top_of_profiles()

    page, paginator_data = get_paginator_data(ANSWERS, 5, input_page)
    if not page and len(list(ANSWERS)) != 0:
        return HttpResponse(status=404)

    context = {'curr_user': request.user, 'request': request, 'question': question_item, 'id': question_id,
        'answers': page.object_list, 'paginator': paginator_data, 'curr_url': 'question', 'tags': TAGS,
        'members': MEMBERS}
    return render(request, 'question.html', context=context)


def login(request: HttpRequest):

    next_url = request.GET.get('next', 'index')

    if request.method == "POST":

        login_form = LoginForm(request.POST)

        if login_form.is_valid():
            user = auth.authenticate(request=request, **login_form.cleaned_data)
            if user is not None:
                auth_login(request, user)
                return redirect(next_url)
            else:
                login_form.add_error(field=None, error="Wrong username or password!")

    elif request.method == "GET":
        login_form = LoginForm()
    
    TAGS = Tag.objects.top_of_tags()
    MEMBERS = Profile.objects.top_of_profiles()

    context = {'curr_user': request.user, 'request': request, 'curr_url': 'login',
        'form': login_form, 'next_url': next_url, 'tags': TAGS, 'members': MEMBERS}
    return render(request, 'login.html', context=context)


def signup(request: HttpRequest):

    if request.method == "POST":

        signup_user_form = SignUpUserForm(request.POST)
        signup_profile_form = SignUpProfileForm(request.POST)

        if signup_user_form.is_valid() and signup_profile_form.is_valid():
            user = signup_user_form.save()
            profile = signup_profile_form.save(user)
            if user and profile:
                auth_login(request, user)
                return redirect('index')
            else:
                signup_user_form.add_error("User saving error!")

    elif request.method == "GET":
        signup_user_form = SignUpUserForm()
        signup_profile_form = SignUpProfileForm()

    TAGS = Tag.objects.top_of_tags()
    MEMBERS = Profile.objects.top_of_profiles()

    context = {'curr_user': request.user, 'curr_url': 'signup', 'request': request,
        'form_user': signup_user_form, 'form_profile': signup_profile_form, 'tags': TAGS, 'members': MEMBERS}
    return render(request, 'signup.html', context=context)


@login_required
def settings(request: HttpRequest):

    if request.method == "POST":
        user_id = request.user.id
        user, profile = Profile.objects.get_user_by_id(user_id), Profile.objects.get_profile_by_user_id(user_id)

        settings_user_form = SettingsUserForm(request.POST, instance=user)
        settings_profile_form = SettingsProfileForm(request.POST, instance=profile)
        if settings_user_form.is_valid() and settings_profile_form.is_valid():
            curr_username = request.user.username
            curr_password = request.POST['password']
            test_auth_user = auth.authenticate(request=request, username=curr_username, password=curr_password)
            if test_auth_user is None:
                settings_user_form.add_error(field='password', error="The old password is incorrect!")
            else:
                new_user = settings_user_form.update(user)
                new_profile = settings_profile_form.update(user)

                if new_user and new_profile:
                    new_password = request.POST['new_password']
                    if new_password != '':
                        test_auth_user = auth.authenticate(request=request, username=new_user.username, password=new_password)
                    
                    if test_auth_user is not None:
                        auth_login(request, test_auth_user)
                    else:
                        settings_user_form.add_error(field=None, error="User authenticating error!")
                else:
                    settings_user_form.add_error(field=None, error="User saving error!")
            

    elif request.method == "GET":
        user_id = request.user.id
        user, profile = Profile.objects.get_user_by_id(user_id), Profile.objects.get_profile_by_user_id(user_id)
        settings_user_form = SettingsUserForm(initial={'username': user.username, 'email': user.email})
        settings_profile_form = SettingsProfileForm(initial={'avatar': profile.avatar})

    TAGS = Tag.objects.top_of_tags()
    MEMBERS = Profile.objects.top_of_profiles()

    context = {'curr_user': request.user, 'request': request,
        'curr_url': 'settings', 'tags': TAGS, 'members': MEMBERS,
        'form_user': settings_user_form, 'form_profile': settings_profile_form}
    return render(request, 'settings.html', context=context)

def logout(request: HttpRequest):
    next_url = request.GET.get('next', 'index')

    auth_logout(request)
    return redirect(next_url)
