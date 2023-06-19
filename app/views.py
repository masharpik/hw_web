from django.http import HttpResponse, HttpRequest, HttpResponseBadRequest
from django.shortcuts import render, redirect
from askme.settings import LOGIN_URL
from . import models
from django.core.paginator import Paginator
from app.models import *
from app.forms import *
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.core.files.storage import FileSystemStorage
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse


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
    curr_user = request.user
    curr_profile = curr_user.profile if not curr_user.is_anonymous else None
    vote_questions = curr_profile.get_vote_questions() if curr_profile else []
    vote_answers = curr_profile.get_vote_answers() if curr_profile else []

    context = {'curr_user': curr_user, 'curr_profile': curr_profile, 'questions': page.object_list, 'request': request,
        'paginator': paginator_data, 'curr_url': 'index', 'tags': TAGS, 'members': MEMBERS, 'vote_questions': vote_questions,
        'vote_answers': vote_answers}
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
    curr_user = request.user
    curr_profile = curr_user.profile if not curr_user.is_anonymous else None
    vote_questions = curr_profile.get_vote_questions() if curr_profile else []
    vote_answers = curr_profile.get_vote_answers() if curr_profile else []

    context = {'curr_user': curr_user, 'curr_profile': curr_profile, 'questions': page.object_list, 'request': request,
        'paginator': paginator_data, 'curr_url': 'hot', 'tags': TAGS, 'members': MEMBERS, 'vote_questions': vote_questions,
        'vote_answers': vote_answers}
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
    curr_user = request.user
    curr_profile = curr_user.profile if not curr_user.is_anonymous else None
    vote_questions = curr_profile.get_vote_questions() if curr_profile else []
    vote_answers = curr_profile.get_vote_answers() if curr_profile else []

    context = {'curr_user': curr_user, 'curr_profile': curr_profile, 'tag': tag_name, 'request': request, 'questions': page.object_list,
        'paginator': paginator_data, 'curr_url': 'tag', 'tags': TAGS, 'members': MEMBERS, 'vote_questions': vote_questions,
        'vote_answers': vote_answers}
    return render(request, 'tag.html', context=context)


@login_required
def ask(request: HttpRequest):

    if request.method == "POST":
        title, text, tags = request.POST['title'], request.POST['text'], request.POST['tags']
        profile_id = Profile.objects.get_profile_by_user_id(request.user.id).id
        ask_form = AskForm(request.POST, profile_id=profile_id, initial={"title": title, "text": text, "tags": tags})
        if ask_form.is_valid():
            new_question = ask_form.save()
            if new_question:
                return redirect('question', question_id=new_question.id)

    elif request.method == "GET":
        ask_form = AskForm()

    TAGS = Tag.objects.top_of_tags()
    MEMBERS = Profile.objects.top_of_profiles()
    curr_user = request.user
    curr_profile = curr_user.profile if not curr_user.is_anonymous else None

    context = {'curr_user': curr_user, 'curr_profile': curr_profile, 'request': request, 'curr_url': 'ask', 'tags': TAGS,
        'members': MEMBERS, 'ask_form': ask_form}
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

    if request.method == "POST":
        if not request.user.is_authenticated:
            response = redirect(LOGIN_URL)
            response['Location'] += f'?next={request.get_full_path()}'
            return response

        text = request.POST['text']
        profile_id = Profile.objects.get_profile_by_user_id(request.user.id).id
        answer_form = AnswerForm(request.POST, question_id=question_id, profile_id=profile_id, initial={'text': text})
        if answer_form.is_valid():
            new_answer = answer_form.save()
            if new_answer:
                ANSWERS = question_item.get_answers()
                id_answers = list(question_item.get_id_answers())
                need_page = id_answers.index((new_answer.id,)) // 5

                response = redirect('question', question_id)
                response['Location'] += f'?page={need_page}' + f'#answer-{new_answer.id}'
                return response

    elif request.method == "GET":
        answer_form = AnswerForm()
    
    curr_user = request.user
    curr_profile = curr_user.profile if not curr_user.is_anonymous else None
    vote_questions = curr_profile.get_vote_questions() if curr_profile else []
    vote_answers = curr_profile.get_vote_answers() if curr_profile else []

    context = {'curr_user': curr_user, 'curr_profile': curr_profile, 'request': request, 'question': question_item, 'id': question_id,
        'answers': page.object_list, 'paginator': paginator_data, 'curr_url': 'question', 'tags': TAGS,
        'members': MEMBERS, 'answer_form': answer_form, 'input_page': input_page, 'vote_questions': vote_questions,
        'vote_answers': vote_answers}
    return render(request, 'question.html', context=context)


def login(request: HttpRequest):

    next_url = request.GET.get('next', 'index')

    if request.method == "POST":

        login_form = LoginForm(request.POST, request=request)

        if login_form.is_valid():
            user = auth.authenticate(request=request, **login_form.cleaned_data)
            if user is not None:
                auth_login(request, user)
                return redirect(next_url)

    elif request.method == "GET":
        login_form = LoginForm()
    
    TAGS = Tag.objects.top_of_tags()
    MEMBERS = Profile.objects.top_of_profiles()
    curr_user = request.user
    curr_profile = curr_user.profile if not curr_user.is_anonymous else None

    context = {'curr_user': curr_user, 'curr_profile': curr_profile, 'request': request, 'curr_url': 'login',
        'form': login_form, 'next_url': next_url, 'tags': TAGS, 'members': MEMBERS}
    return render(request, 'login.html', context=context)


def signup(request: HttpRequest):

    if request.method == "POST":
        signup_form = SignUpForm(request.POST, request.FILES, request=request)

        if signup_form.is_valid():

            user = signup_form.save()
            if user:
                auth_login(request, user)
                return redirect('index')

    elif request.method == "GET":
        signup_form = SignUpForm()

    TAGS = Tag.objects.top_of_tags()
    MEMBERS = Profile.objects.top_of_profiles()
    curr_user = request.user
    curr_profile = curr_user.profile if not curr_user.is_anonymous else None

    context = {'curr_user': curr_user, 'curr_profile': curr_profile, 'curr_url': 'signup', 'request': request,
        'form': signup_form, 'tags': TAGS, 'members': MEMBERS}
    return render(request, 'signup.html', context=context)


@login_required
def settings(request: HttpRequest):

    if request.method == "POST":
        curr_username, email = request.user.username, request.POST['email']

        profile = Profile.objects.get_profile_by_user_id(request.user.id)
        avatar = profile.avatar

        settings_form = SettingsForm(request.POST, request.FILES, request=request, initial={'username': curr_username, 'email': email})
        if settings_form.is_valid():
            settings_form.save()

    elif request.method == "GET":
        user_id = request.user.id
        user, profile = Profile.objects.get_user_by_id(user_id), Profile.objects.get_profile_by_user_id(user_id)
        settings_form = SettingsForm(initial={'username': user.username, 'email': user.email, 'avatar': profile.avatar})

    TAGS = Tag.objects.top_of_tags()
    MEMBERS = Profile.objects.top_of_profiles()
    curr_user = request.user
    curr_profile = curr_user.profile if not curr_user.is_anonymous else None

    context = {'curr_user': curr_user, 'curr_profile': curr_profile, 'request': request,
        'curr_url': 'settings', 'tags': TAGS, 'members': MEMBERS,
        'form': settings_form}
    return render(request, 'settings.html', context=context)


def logout(request: HttpRequest):
    next_url = request.GET.get('next', 'index')

    auth_logout(request)
    return redirect(next_url)


@require_http_methods(["POST"])
def like_question(request: HttpRequest):
    if not request.user.is_authenticated:
        return JsonResponse({'status': 'not_auth'})
    try:
        question_id = int(request.POST['question_id'])
        islike = int(request.POST['islike'])

        some_question = Question.objects.get_question_by_id(question_id)

        profile_id = request.user.profile.id
        
        if islike == 0:
            VoteQuestion.objects.create_vote_question_by_profile_and_question_id(question_id, profile_id)
            islike = 1
        elif islike == 1:
            vote = VoteQuestion.objects.get_vote_question_by_profile_and_question_id(question_id, profile_id)
            vote.delete()
            islike = 0

        return JsonResponse({'status': 'ok', 'islike': islike, 'likes_count': some_question.get_likes_count()})
    except:
        return JsonResponse({'status': 'error'})


@require_http_methods(["POST"])
def like_answer(request: HttpRequest):
    if not request.user.is_authenticated:
        return JsonResponse({'status': 'not_auth'})
    try:
        answer_id = int(request.POST['answer_id'])
        islike = int(request.POST['islike'])

        some_answer = Answer.objects.get_answer_by_id(answer_id)

        profile_id = request.user.profile.id
        
        if islike == 0:
            VoteAnswer.objects.create_vote_answer_by_profile_and_answer_id(answer_id, profile_id)
            islike = 1
        elif islike == 1:
            vote = VoteAnswer.objects.get_vote_answer_by_profile_and_answer_id(answer_id, profile_id)
            vote.delete()
            islike = 0

        return JsonResponse({'status': 'ok', 'islike': islike, 'likes_count': some_answer.get_likes_count()})
    except:
        return JsonResponse({'status': 'error'})

@require_http_methods(["POST"])
def correctness(request: HttpRequest):
    if not request.user.is_authenticated:
        return JsonResponse({'status': 'not_auth'})
    try:
        answer_id = int(request.POST['answer_id'])
        iscorrectness = int(request.POST['iscorrectness'])

        some_answer = Answer.objects.get_answer_by_id(answer_id)
        
        if iscorrectness == 0:
            some_answer.correctness = True
            some_answer.save()
            iscorrectness = 1
        elif iscorrectness == 1:
            some_answer.correctness = False
            some_answer.save()
            iscorrectness = 0

        return JsonResponse({'status': 'ok', 'iscorrectness': iscorrectness})
    except:
        return JsonResponse({'status': 'error'})
