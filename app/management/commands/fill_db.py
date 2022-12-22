from django.core.management.base import BaseCommand
from itertools import islice
from django.contrib.auth.models import User
from app.models import Tag, Profile, Question, Answer, VoteQuestion, VoteAnswer
from random import choice

class Command(BaseCommand):
    help = 'populates currencies table'

    STEP = 1000
    RATIO = 10000

    def add_arguments(self, parser):
        parser.add_argument('ratio', nargs='?', type=int, default=self.RATIO, help='Количество')

    def fill_vote_questions(self, ratio):
        profiles = Profile.objects.all()
        questions = Question.objects.all()
        idx_p = 0
        idx_q = 0

        batch_size = 10000
        objs = []

        been = []
        for j in range(0, ratio):
            while (idx_p % ((ratio - 1) // 100 + 1), idx_q % ((ratio - 1) // 10 + 1)) in been:
                if idx_q + 1 == ((ratio - 1) // 10 + 1):
                    idx_q = 0 % ((ratio - 1) // 10 + 1)
                    idx_p += 1 % ((ratio - 1) // 100 + 1)
                else:
                    idx_q += 1 % ((ratio - 1) // 10 + 1)
            prof = profiles[idx_p]
            quest = questions[idx_q]

            been.append((idx_p, idx_q))

            vote_question = VoteQuestion(is_like=bool(j))
            vote_question.profile=prof
            vote_question.question=quest
            objs.append(vote_question)
        print("END")
        objs = (y for y in objs)
        while True:
            batch = list(islice(objs, batch_size))
            if not batch:
                break
            VoteQuestion.objects.bulk_create(batch, batch_size)
    
    def fill_vote_answers(self, ratio):
        profiles = Profile.objects.all()
        answers = Answer.objects.all()
        batch_size = 10000
        objs = []
        need_to_circle = False
        for i in range(0, ratio, self.STEP):
            prof = profiles[(i * self.STEP) % ((ratio - 1) // 100 + 1)]
            answ = answers[(i * self.STEP) % ratio]
            for j in range(i, i + self.STEP):
                if j >= ratio:
                    need_to_circle = True
                    break
                vote_answer = VoteAnswer(is_like=bool(i))
                vote_answer.profile=prof
                vote_answer.answer=answ
                objs.append(vote_answer)
            if need_to_circle:
                break
        objs = (y for y in objs)
        while True:
            batch = list(islice(objs, batch_size))
            if not batch:
                break
            VoteAnswer.objects.bulk_create(batch, batch_size)

    def fill_profiles(self, ratio):
        users = User.objects.all()
        batch_size = self.STEP
        objs = (Profile(user=users[i], avatar="default_avatar.jpeg") for i in range(ratio))
        while True:
            batch = list(islice(objs, batch_size))
            if not batch:
                break
            Profile.objects.bulk_create(batch, batch_size)

    def fill_users(self, ratio):
        batch_size = self.STEP
        objs = (User(username='Nickname%s' % i, email='Nickname%s@beatles.com' % i, password='Nickname%s' % i) for i in range(ratio))
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

    def create_question(self, curr_idx, ratio, some_profile):
        quest = Question()
        quest.title = 'Question #%s' % curr_idx
        quest.text = 'Text of the question #%s' % curr_idx 
        quest.profile = some_profile
        return quest

    def fill_questions(self, ratio):
        profiles = Profile.objects.all()
        batch_size = self.STEP
        objs = (self.create_question(i, ratio, profiles[i % ((ratio - 1) // 10 + 1)]) for i in range(ratio))
        while True:
            batch = list(islice(objs, batch_size))
            if not batch:
                break
            Question.objects.bulk_create(batch, batch_size)

    def add_tags_to_questions(self):
        try:
            questions = Question.objects.all()
            three_tags = Tag.objects.all()[4:7]
            batch_size = self.STEP
            objs = []
            for question in questions:
                for some_tag in three_tags:
                    question.tags.add(some_tag)
                objs.append(question)

            while True:
                batch = list(islice(objs, batch_size))
                if not batch:
                    break
                Question.objects.bulk_update(batch, batch_size)
        except Exception as e:
            print(e)
            pass
    
    def fill_answers(self, ratio):
        profiles = Profile.objects.all()
        questions = Question.objects.all()
        batch_size = 10000
        objs = []
        need_to_circle = False
        for i in range(0, ratio, self.STEP):
            prof = profiles[(i * self.STEP) % ((ratio - 1) // 100 + 1)]
            quest = questions[(i * self.STEP) % ((ratio - 1) // 10 + 1)]
            for j in range(i, i + self.STEP):
                if j >= ratio:
                    need_to_circle = True
                    break
                answer = Answer(text='Text of the answer #%s' % i, correctness=bool(i))
                answer.profile=prof
                answer.question=quest
                objs.append(answer)
            if need_to_circle:
                break
        objs = (y for y in objs)
        while True:
            batch = list(islice(objs, batch_size))
            if not batch:
                break
            Answer.objects.bulk_create(batch, batch_size)

    def handle(self, *args, **options):
        ratio = options['ratio']
        print(f"ratio = {ratio}")
        # Tag.objects.all().delete()
        # print("TAGS WILL FILL")
        # self.fill_tags(ratio + 1)
        # print("TAGS FILLED")

        # User.objects.all().delete()
        # print("USERS WILL FILL")
        # self.fill_users(ratio + 1)
        # print("USERS FILLED")

        # Profile.objects.all().delete()
        # print("PROFILES WILL FILL")
        # self.fill_profiles(ratio + 1)
        # print("PROFILES FILLED")

        # Question.objects.all().delete()
        # print("QUESTIONS WILL FILL")
        # self.fill_questions(ratio * 10 + 1)
        # print("QUESTIONS FILLED")
        # print("QUESTIONS WILL UPDATE")
        # self.add_tags_to_questions()
        # print("QUESTIONS UPDATED")

        # Answer.objects.all().delete()
        # print("ANSWERS WILL FILL")
        # self.fill_answers(ratio * 100 + 1)
        # print("ANSWERS FILLED")

        # VoteQuestion.objects.all().delete()
        print("VoteQuestion WILL FILL")
        self.fill_vote_questions(ratio * 100 + 1)
        print("VoteQuestion FILLED")

        # VoteAnswer.objects.all().delete()
        # print("VoteAnswer WILL FILL")
        # self.fill_vote_anwers(ratio * 100 + 1)
        # print("VoteAnswer FILLED")
