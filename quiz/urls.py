from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path("", views.MainPage.as_view(),  name="main_page"),
    path("register", views.RegisterView.as_view(),  name="register"),
    path("login", views.LoginView.as_view(),  name="login_view"),
    path("add_quiz", views.AddQuizView.as_view(),  name="add_quiz"),
    path("quiz/<int:id>", views.QuizView.as_view(),  name="quiz"),
    path("add_question", views.AddQuestion,  name="add_question"),
    path("get_questions/<int:pk>", views.GetAllQuestions,  name="get_questions"),
    path("get_question/<int:pk>", views.GetQuestion,  name="get_question"),
    path("delete_question/<int:pk>", views.DeleteQuestion,  name="delete_question"),
    path('profile/<int:id>', views.MyProfile.as_view(), name="profile"),
    path('edit_quiz/<int:id>', views.EditQuiz.as_view(), name="edit_quiz"),
    path('delete_quiz/<int:id>', views.DeleteQuiz, name="delete_quiz"),
    path("quiz/<int:id>/start", views.StartSession,  name="start_session"),
    path("started_quiz_get_question/<int:id>", views.StartedQuizGetQuestion,  name="started_quiz_get_question"),
    path("started_quiz_post_answer/<int:id>", views.StartedQuizPostAnswer.as_view(),  name="started_quiz_post_answer"),
    path("finish_quiz/<int:id>", views.FinishedQuiz.as_view(),  name="finish_quiz"),
    path('my_class', views.MyClassView.as_view(), name="my_class"),
    path('add_class', views.AddClassView.as_view(), name="add_class"),
    path('class/<int:pk>', views.ClassView.as_view(), name="class"),
    path('add_user_to_class/<int:pk>', views.AddUserToClass, name="add_user_to_class"),
    path('remove_user_from_class/<int:pk>/<int:id>', views.RemoveUserFromClass, name="remove_user_from_class"),
]
