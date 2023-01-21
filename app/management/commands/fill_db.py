from django.core.management.base import BaseCommand
from itertools import islice
from django.contrib.auth.models import User
from app.models import Tag, Profile, Question, Answer, VoteQuestion, VoteAnswer
from django.db.models import Count
import random

class Command(BaseCommand):
    help = 'populates currencies table'

    STEP = 1000
    RATIO = 10000

    def add_arguments(self, parser):
        parser.add_argument('ratio', nargs='?', type=int, default=self.RATIO, help='Количество')
    
    def handle(self, *args, **options):
        ratio = options['ratio']
        # self.fill_db_again(ratio)

    def fill_vote_questions(self, ratio):
        profiles = Profile.objects.all()[:1001]
        questions = Question.objects.all()[:1001]

        batch_size = 10000
        objs = []

        iter = 0
        for i in profiles:
            for j in questions:
                vote_question = VoteQuestion(is_like=bool(iter))
                vote_question.profile = i
                vote_question.question = j
                objs.append(vote_question)
            iter += 1
            if iter == 25:
                objs = (y for y in objs)
                VoteQuestion.objects.bulk_create(objs)
                iter = 0
                objs = []

    def fill_vote_answers(self, ratio):
        profiles = Profile.objects.all()[:1001]
        answers = Answer.objects.all()[:1001]

        batch_size = 10000
        objs = []

        iter = 0
        for i in profiles:
            for j in answers:
                vote_answer = VoteAnswer(is_like=bool(iter))
                vote_answer.profile = i
                vote_answer.answer = j
                objs.append(vote_answer)
            iter += 1
            if iter == 25:
                objs = (y for y in objs)
                VoteAnswer.objects.bulk_create(objs)
                iter = 0
                objs = []

    def fill_profiles(self, ratio):
        users = User.objects.all()
        batch_size = self.STEP
        objs = (Profile(user=i, avatar="default_avatar.jpeg") for i in users)
        while True:
            batch = list(islice(objs, batch_size))
            if not batch:
                break
            Profile.objects.bulk_create(batch, batch_size)

    def fill_users(self, ratio):
        def make_user(idx):
            user = User(username='Username%s' % idx, email='usename%s@beatles.com' % idx)
            user.set_password('Username%s' % idx)
            return user

        batch_size = self.STEP
        objs = (make_user(i) for i in range(4000, ratio))

        while True:
            batch = list(islice(objs, batch_size))
            if not batch:
                break
            User.objects.bulk_create(batch, batch_size)

    def fill_tags(self, ratio):
        batch_size = self.STEP
        objs = (Tag(name='Tag %s' % i) for i in range(ratio))
        while True:
            batch = list(islice(objs, batch_size))
            if not batch:
                break
            Tag.objects.bulk_create(batch, batch_size)


    def fill_questions(self, ratio):
        profiles = Profile.objects.all()
        N = Profile.objects.all().count()
        batch_size = self.STEP

        objs = (Question(title=('Question #%s' % i), text=('Text of the question #%s' % i), profile=profiles[i % N]) for i in range(ratio))
    
        while True:
            batch = list(islice(objs, batch_size))
            if not batch:
                break
            Question.objects.bulk_create(batch, batch_size)

    def add_tags_to_questions(self):

        def forming_question(question, some_tag):
            question.tags.add(some_tag)

        try:
            questions = Question.objects.all()
            all_tags = list(Tag.objects.all())
            batch_size = self.STEP

            for question in questions:
                for some_tag in random.sample(all_tags, 3):
                    forming_question(question, some_tag)

        except Exception as e:
            print(e)
            pass
    
    def fill_answers(self, ratio):
        profiles = Profile.objects.all()
        questions = Question.objects.all()
        batch_size = 10000
        objs = []
        i = 0
        for profile in profiles[:11]:
            for question in questions:
                answer = Answer(text='Text of the answer #%s' % i, correctness=bool(i))
                i += 1
                answer.profile=profile
                answer.question=question
                objs.append(answer)

        objs = (y for y in objs)
        while True:
            batch = list(islice(objs, batch_size))
            if not batch:
                break
            Answer.objects.bulk_create(batch, batch_size)
    
    def update_tags_name(self):
        TAGS = Tag.objects.all()
        i = 0
        for tag in TAGS:
            tag.name = f"Tag{i}"
            i += 1
            tag.save()

    def fill_db_again(self, ratio):
        print(f"ratio = {ratio}")

        User.objects.all().delete()
        print("USERS WILL FILL")
        self.fill_users(ratio + 1)
        print("USERS FILLED")

        print("PROFILES WILL FILL")
        self.fill_profiles(ratio + 1)
        print("PROFILES FILLED")

        print("QUESTIONS WILL FILL")
        self.fill_questions(ratio * 10 + 1)
        print("QUESTIONS FILLED")

        print("TAGS WILL FILL")
        self.fill_tags(ratio + 1)
        print("TAGS FILLED")

        print("QUESTIONS WILL UPDATE")
        self.add_tags_to_questions()
        print("QUESTIONS UPDATED")

        print("ANSWERS WILL FILL")
        self.fill_answers(ratio * 100 + 1)
        print("ANSWERS FILLED")

        print("VoteQuestion WILL FILL")
        self.fill_vote_questions(ratio * 100 + 1)
        print("VoteQuestion FILLED")

        print("VoteAnswer WILL FILL")
        self.fill_vote_answers(ratio * 100 + 1)
        print("VoteAnswer FILLED")
