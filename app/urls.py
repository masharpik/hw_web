from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('hot', views.hot, name='hot'),
    path('tag/<str:tag_name>', views.tag, name='tag'),
    path('ask', views.ask, name='ask'),
    path('login', views.login, name='login'),
    path('question/<int:question_id>', views.question, name='question'),
    path('signup', views.registration, name='registration'),
    path('settings', views.settings, name='settings')
]