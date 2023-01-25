from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('hot/', views.hot, name='hot'),
    path('tag/<str:tag_name>/', views.tag, name='tag'),
    path('ask/', views.ask, name='ask'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('question/<int:question_id>/', views.question, name='question'),
    path('signup/', views.signup, name='signup'),
    path('profile/edit/', views.settings, name='settings'),
    path('like_question/', views.like_question, name='like_question'),
    path('like_answer/', views.like_answer, name='like_answer'),
    path('correctness/', views.correctness, name='correctness')
]
