from src.negation.question_negator import negate_question


questions = [

    "Who won the championship?",

    "Which player scored 10 goals?",

    "What city has population greater than 5000?",

    "What are the notes for South Australia?",

    "Which country hosted the Olympics?",

    "Who directed Titanic?",

    "Which player plays for Barcelona?"
]


for q in questions:

    negated = negate_question(q)

    print("\nORIGINAL:")
    print(q)

    print("\nNEGATED:")
    print(negated)

    print("\n" + "="*60)