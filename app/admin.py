from django.contrib import admin
from app.models import Tag, Profile, Question, Answer, VoteQuestion, VoteAnswer

# Register your models here.
admin.site.register(Profile)
admin.site.register(Tag)
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(VoteAnswer)
admin.site.register(VoteQuestion)
