from django.shortcuts import render, redirect
from django.views.generic.base import View
from django.contrib.auth.models import User
from .models import Profile
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from .models import Quiz, Question, Answer, Session, QuizClass, ClassSession
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from .serializers import QuizSerializer, QuestionSerializer, StartedQuizQuestionSerializer
from django.contrib.auth.decorators import login_required
from rest_framework.response import Response
from .forms import EditQuizForm, QuizClassForm


class MainPage(View):
    def get(self, request):
        quizzes = Quiz.objects.all().filter(public=True)
        return render(request, "quiz/main_page.html",{"quizzes":quizzes,})

import string
def validate(password):
    letters = set(string.ascii_letters)
    digits = set(string.digits)
    pwd = set(password)
    return not (pwd.isdisjoint(letters) or pwd.isdisjoint(digits))

class RegisterView(View):
    def get(self, request):
        return render(request, "quiz/register.html")
    def post(self, request):
        name = request.POST["name"]
        email = request.POST["email"]
        password = request.POST["password"]
        if not User.objects.filter(username=name).exists():
            if not validate(password) and len(password)<7:
                print("A")
                return render(request, 'quiz/register.html')
            user = User.objects.create_user(username=name, email=email)
            user.set_password(password)
            user.save()
            profile = Profile(user=user)
            profile.save()
            print("B")
            return redirect("login_view")
        
        return render(request, 'quiz/register.html')
        
class LoginView(View):
    def get(self, request):
        return render(request, "quiz/login_view.html")
    def post(self, request):
        name = request.POST["name"]
        password = request.POST["password"]
        user = authenticate(request, username=name, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect("main_page")
        else:
            return render(request, "quiz/login_view.html")


class AddQuizView(View):
    def get(self, request):
        return render(request, 'quiz/add_quiz.html')
    def post(self, request):
        user = request.user.profile
        quiz_name = request.POST["quiz_name"]
        quiz_description = request.POST["quiz_description"]
        quiz = Quiz(owner=user, name=quiz_name, description=quiz_description)
        quiz.save()
        user.quizzies.add(quiz)
        user.save()
        return redirect('quiz', quiz.id)

class QuizView(View):
    def get(self, request, id):
        quiz = get_object_or_404(Quiz, id=id)
        context = {
            'quiz':quiz,
        }
        quiz.views +=1
        quiz.save()
        return render(request, 'quiz/quiz_detail.html',context)

@api_view(["POST"])
def AddQuestion(request):
    serializer = QuestionSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
    else:
        print(serializer.errors)
    return Response(serializer.data)

@api_view(["GET"])   
def GetAllQuestions(request,pk):
    quiz = Quiz.objects.get(id=pk)
    serializers = QuizSerializer(quiz, many=False)
    return Response(serializers.data)

@api_view(["GET"])   
def GetQuestion(request, pk ):
    question = Question.objects.get(id=pk)
    serializers = QuestionSerializer(question, many=False)
    return Response(serializers.data)

@api_view(["DELETE"])   
def DeleteQuestion(request, pk):
    question = Question.objects.get(id=pk)
    question.delete()
    return Response("Status Ok")

def StartSession(request, id):
    profile = request.user.profile
    quiz = Quiz.objects.get(id=id)
    if quiz.sessions.filter(owner=profile, finished=False).exists():
        try:
            session = quiz.sessions.filter(owner=profile, finished=False)[0]
        except:
            session = []
    else:
        session = Session(owner=profile, quiz=quiz)
        session.save()
        for question in quiz.questions.all():
            question1 = Question.objects.get(id=question.id)
            session.not_answered_questions.add(question1)
        session.save()
        quiz.sessions.add(session)
        quiz.save()
    
    return render(request, "quiz/start_quiz.html",{"session":session})

import random
@api_view(["GET"])  
def StartedQuizGetQuestion(request, id):
    session = Session.objects.get(id=id)
    if session.not_answered_questions.count()>0:
        question = random.choice(session.not_answered_questions.all())
        serializer = StartedQuizQuestionSerializer(question, many=False)
        session.not_answered_questions.remove(question)
        return Response(serializer.data)
    else:
        return Response("Brak")

import json
from django.http import JsonResponse
class StartedQuizPostAnswer(View):
    def post(self, request, id):
        session = Session.objects.get(id=id)
        data = json.loads(request.body)
        question_id = data["question_id"]
        question = Question.objects.get(id=question_id)
        correct_id = []
        user_id = []
        for answer in question.answers.all():
            if answer.correct:
                correct_id.append(answer.id)
        for answer in data["answers"]:
            if answer['correct']:
                user_id.append(answer['answer_id'])
        correct_id.sort()
        user_id.sort()
        if user_id == correct_id:
            correct_answer = True
            session.points +=1
        else: 
            correct_answer = False
        
        session.save()

        return JsonResponse(list([correct_answer]), safe=False)

class FinishedQuiz(View):
    def get(self, request, id):
        session = Session.objects.get(id=id)
        session.finished = True
        quiz = session.quiz
        max_points = quiz.questions.all().count()
        session_points = int(session.points)
        session.save()
        quiz.finished_sessions +=1
        quiz.save()

        return JsonResponse(list([session_points, max_points]), safe=False)

class MyProfile(View):
    def get(self, request, id):
        profile = Profile.objects.get(id=id)
        total_views = 0
        for quiz in profile.quizzies.all():
            total_views += quiz.views
        try:
            most_popular_quiz= profile.quizzies.all().order_by("-views")[0]
        except:
            most_popular_quiz = None
        context = {
            'profile':profile,
            'public_quiz':profile.quizzies.all().filter(public=True),
            'private_quiz':profile.quizzies.all().filter(public=False),
            'most_popular_quiz':most_popular_quiz,
            'total_views':total_views,
            'quiz_count':profile.quizzies.all().count(),
        }
        return render(request, 'quiz/profile.html', context)

class EditQuiz(View):
    def get(self, request, id):
        quiz = get_object_or_404(Quiz, id=id)
        context = {
            'quiz':quiz,
            'form':EditQuizForm(initial={
                'name':quiz.name,
                'description':quiz.description,
                'public':quiz.public,
            }),
        } 
        return render(request, 'quiz/edit_quiz.html', context)
    def post(self, request, id):
        quiz = get_object_or_404(Quiz, id=id)
        form = EditQuizForm(request.POST, instance=quiz)
        if form.is_valid():
            form.save()
            return redirect("quiz",quiz.id)
        else:
            return redirect("quiz",quiz.id)

def DeleteQuiz(request, id):
    quiz = get_object_or_404(Quiz, id=id)
    owner_id = quiz.owner.id
    quiz.delete()
    return redirect("profile",owner_id)

class MyClassView(View):
    def get(self, request):
        profile = request.user.profile
        
        context={
            'my_classes':profile.classes_owner.all(),
            'classes':profile.classes.all(),
        }
        return render(request, 'quiz/class.html', context)

class AddClassView(View):
    def get(self, request):
        context={
            'form':QuizClassForm(),
        }
        return render(request, "quiz/add_class.html", context)
    def post(self, request):
        profile = request.user.profile
        form = QuizClassForm(request.POST)
        if form.is_valid():
            quiz_class = form.save(commit=False)
            quiz_class.owner = request.user.profile
            quiz_class.save()
            profile.classes_owner.add(quiz_class)
            profile.save()
            return redirect('main_page')
        return redirect('add_class')

class ClassView(View):
    def get(self, request, pk):
        quiz_class = get_object_or_404(QuizClass, id=pk)
        context={
            'class':quiz_class,
        }
        return render(request, 'quiz/class_view.html', context)

def AddUserToClass(request, pk):
    if request.method=="POST":
        quiz_class = get_object_or_404(QuizClass, id=pk)
        user = request.POST["user_name"]
        student = User.objects.filter(username=user)
        if student.exists():
            quiz_class.students.add(student[0].profile)
            student[0].profile.classes.add(quiz_class)
            student[0].profile.save()
            quiz_class.save()
        return redirect("class",quiz_class.id )

def RemoveUserFromClass(request, pk, id):
    if request.method=="POST":
        quiz_class = get_object_or_404(QuizClass, id=pk)
        user = get_object_or_404(Profile, id=id)
        quiz_class.students.remove(user)
        quiz_class.save()
        user.classes.remove(quiz_class)
        user.save()
        return redirect("class",quiz_class.id )
