from django.contrib import admin
from .models import Profile, Quiz, Answer, Question, Session
# Register your models here.
admin.site.register(Profile)
admin.site.register(Quiz)
admin.site.register(Answer)
admin.site.register(Question)
admin.site.register(Session)