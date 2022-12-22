from django.db import models
from django.contrib.auth.models import User

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

    def __str__(self):
        return f"Tag {self.name}"


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    avatar = models.ImageField(blank=True, null=True, upload_to='profile_images')

    objects = ProfileManager()

    def __str__(self):
        return f"Profile {self.user.username}"


class Question(models.Model):
    title = models.CharField(max_length=33)
    text = models.CharField(max_length=255)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag)
    datetime = models.DateTimeField(auto_now_add=True)

    objects = QuestionManager()

    def __str__(self):
        return f"Question {self.title}"


class Answer(models.Model):
    text = models.CharField(max_length=255)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    correctness = models.BooleanField(default=False)

    objects = AnswerManager()

    def __str__(self):
        return f"Answer {self.text}"


class VoteQuestion(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)

    def __str__(self):
        return f"VoteQuestion"

    class Meta:
        unique_together = ['question', 'profile']

    is_like = models.BooleanField()

    objects = VoteQuestionManager()


class VoteAnswer(models.Model):
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)

    def __str__(self):
        return f"VoteQuestion"

    class Meta:
        unique_together = ['answer', 'profile']

    is_like = models.BooleanField()

    objects = VoteAnswerManager()
