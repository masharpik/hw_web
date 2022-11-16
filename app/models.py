from django.db import models

ANSWERS_FOR_QUESTIONS = [
    {
        'id': id,
        'text': f"Text of answer #{id + 1}",
        'is_correct': bool(id % 2),
        'score': id % 3
    }
    for id in range(21)
]

QUESTIONS = [
    {
        'id': id,
        'title': f"Question #{id + 1}",
        'text': f"Text of question #{id + 1}",
        'count_answers': id % 3 + 1,
        'tags': ['bender', 'milk', 'python'],
        'score': id % 4,
        'answers': ANSWERS_FOR_QUESTIONS
    }
    for id in range(66)
]
