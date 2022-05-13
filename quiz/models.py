from django.db import models
from django.contrib.auth.models import User
from random import randint

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, null=True,on_delete=models.CASCADE)
    quizzies = models.ManyToManyField("Quiz", related_name="+", blank=True)
    classes = models.ManyToManyField("QuizClass", related_name="+", blank=True)
    classes_owner = models.ManyToManyField("QuizClass", related_name="+", blank=True)
    def __str__(self):
        return self.user.username

        

class Quiz(models.Model):
    owner =  models.ForeignKey("Profile", null=True,on_delete=models.CASCADE)
    name = models.CharField(max_length=200, blank=True)
    description = models.CharField(max_length=600, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    public = models.BooleanField(default=False)
    questions = models.ManyToManyField("Question", related_name="+", blank=True)
    sessions = models.ManyToManyField("Session", related_name="+", blank=True)
    views = models.DecimalField(default=0, max_digits=99999, decimal_places=0, blank=True)
    finished_sessions = models.DecimalField(default=0, max_digits=99999, decimal_places=0, blank=True)
    def point_count(self):
        return self.questions.all().count()

    def __str__(self):
        return str(self.name)

class Question(models.Model):
    quiz = models.ForeignKey("Quiz", null=True,on_delete=models.CASCADE)
    question_text = models.CharField(max_length=500, default="Pytanie")
    answers = models.ManyToManyField("Answer", related_name="+", blank=True)
    def __str__(self):
        return str(self.question_text)

class Answer(models.Model):
    answer_text = models.CharField(max_length=500)
    correct = models.BooleanField(default=False)
    question = models.ForeignKey("Question", null=True,on_delete=models.CASCADE)
    def __str__(self):
        return str(self.answer_text)

class Session(models.Model):
    quiz = models.ForeignKey("Quiz", null=True, on_delete=models.CASCADE)
    owner = models.ForeignKey("Profile", null=True, on_delete=models.CASCADE)
    points = models.DecimalField(default=0, max_digits=999, decimal_places=0, blank=True)
    finished = models.BooleanField(default=False)
    not_answered_questions = models.ManyToManyField("Question", related_name="+", blank=True)

    def __str__(self):
        return str(self.owner.user.username) 

class QuizClass(models.Model):
    name = models.CharField(max_length=200)
    owner = models.ForeignKey("Profile", null=True, on_delete=models.CASCADE)
    students = models.ManyToManyField("Profile", related_name="+", blank=True)
    sessions = models.ManyToManyField("ClassSession", related_name="+", blank=True)

    def __str__(self):
        return str(self.name) 
    

class ClassSession(models.Model):
    quiz_class = models.ForeignKey("QuizClass", null=True, on_delete=models.CASCADE)
    quiz = models.ForeignKey("Quiz", null=True, on_delete=models.CASCADE)
    sessions = models.ManyToManyField("Session", related_name="+", blank=True)
    start = models.DateTimeField()
    end = models.DateTimeField()

    def __str__(self):
        return str(self.quiz_class.owner.user.username) 
