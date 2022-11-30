from django.db import models
from django.contrib.auth.models import User

# ANSWERS_FOR_QUESTIONS = [
#     {
#         'id': id,
#         'text': f"Text of answer #{id + 1}",
#         'is_correct': bool(id % 2),
#         'score': id % 3
#     }
#     for id in range(21)
# ]

# QUESTIONS = [
#     {
#         'id': id,
#         'title': f"Question #{id + 1}",
#         'text': f"Text of question #{id + 1}",
#         'count_answers': id % 3 + 1,
#         'tags': ['bender', 'milk', 'python'],
#         'score': id % 4,
#         'answers': ANSWERS_FOR_QUESTIONS
#     }
#     for id in range(66)
# ]

class ProfileManager(models.Manager):
    pass


class VoteQuestionManager(models.Manager):
    def get_score_of_question(question_id):
        pass


class VoteAnswerManager(models.Manager):
    def get_score_of_answer(answer_id):
        pass


class TagManager(models.Manager):
    def get_questiona_by_tag(tag_name):
        pass


class QuestionManager(models.Manager):
    def get_new_questions():
        pass


    def get_hot_questions():
        pass


class AnswerManager(models.Manager):
    def get_answers_by_question(question_id):
        pass



class Tag(models.Model):
    name = models.CharField(max_length=15)

    objects = TagManager()


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    avatar = models.ImageField(blank=True, null=True)
    email = models.EmailField(max_length=33)

    objects = ProfileManager()


class Question(models.Model):
    title = models.CharField(max_length=33)
    text = models.CharField(max_length=255)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    tag = models.ManyToManyField(Tag)
    score = models.IntegerField(default=0)
    date = models.DateTimeField(auto_now_add=True)

    objects = QuestionManager()


class Answer(models.Model):
    text = models.CharField(max_length=255)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    score = models.IntegerField(default=0)
    correctness = models.BooleanField(default=False)

    objects = AnswerManager()


class VoteQuestion(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)


    class Meta:
        unique_together = ['question', 'profile']


    is_like = models.BooleanField()

    objects = VoteQuestionManager()


class VoteAnswer(models.Model):
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)


    class Meta:
        unique_together = ['answer', 'profile']


    is_like = models.BooleanField()

    objects = VoteAnswerManager()
