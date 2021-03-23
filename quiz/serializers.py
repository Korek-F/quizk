from rest_framework import serializers
from .models import Quiz, Question, Answer

class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ['answer_text','correct']

class StartedQuizAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ("id","answer_text")

class StartedQuizQuestionSerializer(serializers.ModelSerializer):
    #answers1 = StartedQuizAnswerSerializer()
    class Meta:
        model = Question
        fields = ['question_text', 'answers', 'quiz_id', 'id']
        depth =1


class QuestionSerializer(serializers.ModelSerializer):
    answers = AnswerSerializer(many=True)
    quiz_id = serializers.CharField()

    class Meta:
        model = Question
        fields = ['question_text', 'answers', 'quiz_id', 'id']
        
    def validate(self, data):
        return data
  
    def create(self, validated_data):
        quiz_id = validated_data.pop('quiz_id')
        print(quiz_id)
        quiz = Quiz.objects.get(id=quiz_id)
        
        answers_data = validated_data.pop('answers')
        question = Question.objects.create(quiz=quiz, **validated_data)

        quiz.questions.add(question)
        for answer_data in answers_data:
            a1 = Answer.objects.create(question=question, **answer_data)
            question.answers.add(a1)
        return question

class QuizSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True)

    class Meta:
        model = Quiz
        fields = ['name', 'questions']
        depth=2
    def create(self, validated_data):
        questions_data = validated_data.pop('questions')
        quiz = Quiz.objects.create(**validated_data)
        for question_data in questions_data:
            question_text = question_data.pop('question_text')
            question = Question.objects.create(quiz=quiz,question_text=question_text)
            quiz.questions.add(question)
            answers_data = question_data.pop('answers')
            for answer_data in answers_data:
                a1 = Answer.objects.create(question=question, **answer_data)
                question.answers.add(a1)
        return quiz

"""
from quiz.serializers import QuizSerializer
serializer = QuizSerializer(data=data)
serializer.is_valid()
serializer.save()
data = {
    'name':'Quiz12',
    'questions':[
            {'question_text': 'Kim jestem?',
                'answers': [
                    {'answer_text': "AA", 'correct':False},
                    {'answer_text': "BB", 'correct':False},
                    {'answer_text': "CC", 'correct':True},
                    ],
                },
            {'question_text': 'DDDm?',
                'answers': [
                    {'answer_text': 23, 'correct':False},
                    {'answer_text': 3222, 'correct':True},
                    {'answer_text': 223, 'correct':True},
                    ],
                },
            ],
}


from quiz.serializers import QuestionSerializer;serializer = QuestionSerializer(data=data);serializer.is_valid();serializer.save();

data ={'question_text': 'Kim ssjestem?',
        'quiz_id': 18,
        'answers': [
            {'answer_text': "AA", 'correct':False},
            {'answer_text': "BB", 'correct':False},
            {'answer_text': "CC", 'correct':True},
            ],
        }










                {
    'name':'Quiz12',
    'questions':[
            {'question_text': 'Kim jestem?',
                'answers': [
                    {'answer_text': 1, 'correct':False},
                    {'answer_text': 2, 'correct':False},
                    {'answer_text': 3, 'correct':True},
                    ],
                },
            {'question_text': 'DDDm?',
                'answers': [
                    {'answer_text': 23, 'correct':False},
                    {'answer_text': 3222, 'correct':True},
                    {'answer_text': 223, 'correct':True},
                    ],
                },
            ],
}
"""