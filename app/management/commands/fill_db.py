from django.core.management.base import BaseCommand
from itertools import islice
from django.contrib.auth.models import User
from app.models import Tag, Profile, Question, Answer, VoteQuestion, VoteAnswer
from django.db.models import Count

class Command(BaseCommand):
    help = 'populates currencies table'

    STEP = 1000
    RATIO = 10000

    def add_arguments(self, parser):
        parser.add_argument('ratio', nargs='?', type=int, default=self.RATIO, help='Количество')

    def fill_vote_questions(self, ratio):
        profiles = Profile.objects.all()[:1001]
        questions = Question.objects.all()[:1001]

        batch_size = 10000
        objs = []

        iter = 0
        for i in profiles:
            for j in questions:
                vote_question = VoteQuestion(is_like=False)
                vote_question.profile = i
                vote_question.question = j
                objs.append(vote_question)
            iter += 1
            print(iter)
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
                vote_answer = VoteAnswer(is_like=False)
                vote_answer.profile = i
                vote_answer.answer = j
                objs.append(vote_answer)
            iter += 1
            print(iter)
            if iter == 25:
                objs = (y for y in objs)
                VoteAnswer.objects.bulk_create(objs)
                iter = 0
                objs = []

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
        # print("VoteQuestion WILL FILL")
        # self.fill_vote_questions(ratio * 100 + 1)
        # print("VoteQuestion FILLED")

        VoteAnswer.objects.all().delete()
        print("VoteAnswer WILL FILL")
        self.fill_vote_answers(ratio * 100 + 1)
        print("VoteAnswer FILLED")

        # print(Question.objects.all()[:10])
        # print(list(Question.objects.all()[:10]))

        # tags = Tag.objects.annotate(Count('question')).order_by('-question__count')[:8]
        # for e in tags:
        #     print(e.name)
        # print(e.tags.all())
        # question = Question.objects.all()[0]
        # c = Question.objects.filter(votequestion__question=question, votequestion__is_like=False).count()
        # print(c)

        # self.update_tags_name()

        # m = Profile.objects.annotate(Count('question')).order_by('-question__count')[:7]
        # print(m)
        # for e in m:
        #     print(Question.objects.filter(profile=e).count())

        # a = 20
        # b = 30
        # q = Question.objects.all().order_by('datetime')[a:b]
        # print(q)
        # q = Question.objects.all().order_by('datetime')
        # print(q)
        # print(1)
        # Profile.objects.top_of_profiles()
        # print(1)
        # print(2)
        # tags = Tag.objects.top_of_tags()
        # print(Tag.objects.annotate(Count('question')).order_by('-question__count')[:8].query)
        # print(2)
        # print(3)
        # Question.objects.get_new_questions()
        # print(3)
        # question = Question.objects.first()
        # print(4)
        # question.get_likes_count()
        # print(4)
        # print(5)
        # print(question.get_dislikes_count())
        # print(5)
        # print(6)
        # question.get_count_answer()
        # print(6)
        # print(7)
        # question.get_tags()
        # print(7)
        # QUESTIONS = Question.objects.get_new_questions()
        # s = {}
        # for q in QUESTIONS:
        #     s[q.id] = q.get_likes_count()
        # print(s)
        # qs = Question.objects.all()[:1]
        # print(qs.query)
        # print(qs[0])
        # print(qs[0].answer_set.all())
        # print(qs.query)
