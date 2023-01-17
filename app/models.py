from django.db import models
from django.contrib.auth.models import User
from django.db.models import Count

class ProfileManager(models.Manager):
    def top_of_profiles(self):
        return Profile.objects.annotate(Count('question')).order_by('-question__count')[:5]


class VoteQuestionManager(models.Manager):
    def get_score_of_question(self, question_id):
        pass


class VoteAnswerManager(models.Manager):
    def get_score_of_answer(self, answer_id):
        pass


class TagManager(models.Manager):
    def top_of_tags(self):
        return Tag.objects.annotate(Count('question')).order_by('-question__count')[:8]

    def get_tag_by_name(self, tag_name):
        return Tag.objects.get(name=tag_name)
            

class QuestionManager(models.Manager):
    def get_new_questions(self, a, b):
        return Question.objects.all().order_by('datetime')[a:b]

    def get_hot_questions(self, a, b):
        # q = Question.objects.all()
        # answer = [question for question in q]
        # answer.sort(key=lambda x: x.get_likes_count(), reverse=True)
        # return answer[a:b]
        return Question.objects.order_by('-answer__count')[a:b].annotate(Count('answer'))
        # return Question.objects.order_by('-votequestion__likes_count')[a:b].annotate(likes_count=Count('votequestion'))
        # return Question.objects.annotate(likes_count=Count('votequestion')).order_by('likes_count')[a:b]

    def get_curr_count(self):
        return Question.objects.all().count()

    def get_questions_by_tag(self, tag, a, b):
        questions = Question.objects.all()[a:b]
        result = []
        for question in questions:
            if tag.is_in_question(question):
                result.append(question)
        return result
    
    def get_question_by_id(self, id):
        return Question.objects.get(pk=id)


class AnswerManager(models.Manager):
    def get_answers_by_question(self, question_id):
        pass


class Tag(models.Model):
    name = models.CharField(max_length=15, unique=True)

    objects = TagManager()

    def __str__(self):
        return f"Tag {self.name}"

    def is_in_question(self, question):
        return self.question_set.filter(pk=question.pk).exists()


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

    def get_likes_count(self):
        return Question.objects.filter(votequestion__question=self,
            votequestion__is_like=True).count()
    
    def get_dislikes_count(self):
        return Question.objects.filter(votequestion__question=self,
            votequestion__is_like=False).count()
    
    def get_count_answer(self):
        return Question.objects.filter(answer__question=self).count()
    
    def get_tags(self):
        return self.tags.all()
    
    def get_answers(self):
        return self.answer_set.all()


class Answer(models.Model):
    text = models.CharField(max_length=255)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    correctness = models.BooleanField(default=False)

    objects = AnswerManager()

    def __str__(self):
        return f"Answer {self.text}"

    def get_likes_count(self):
        return Answer.objects.filter(voteanswer__answer=self,
            voteanswer__is_like=True).count()
    
    def get_dislikes_count(self):
        return Answer.objects.filter(voteanswer__answer=self,
            voteanswer__is_like=False).count()
    
    def get_correctness(self):
        return self.correctness


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
