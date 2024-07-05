from django.db import models
from users.models import UserData

class Quiz(models.Model):
    title = models.CharField(max_length=100)
    user = models.ForeignKey(UserData, on_delete=models.CASCADE)
    active = models.BooleanField(default=True)
    viewanswer = models.BooleanField(default=False)
    showscore = models.BooleanField(default=True)

class TextQuestion(models.Model):
    question = models.CharField(max_length=200)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='text_questions')

class MCQ(models.Model):
    question = models.CharField(max_length=200)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='mcqs')
    points = models.IntegerField(default=1)

class McqOption(models.Model):
    text = models.CharField(max_length=200)
    is_correct = models.BooleanField(default=False)
    mcq = models.ForeignKey(MCQ, on_delete=models.CASCADE, related_name='options')


class Response(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    time = models.DateTimeField(auto_now_add=True, null=True)


class TextAnswer(models.Model):
    question = models.ForeignKey(TextQuestion, on_delete=models.CASCADE)
    response = models.ForeignKey(Response, on_delete=models.CASCADE)
    answer = models.TextField(null=True)


class McqAnswer(models.Model):
    question = models.ForeignKey(MCQ, on_delete=models.CASCADE)
    response = models.ForeignKey(Response, on_delete=models.CASCADE)
    answer = models.ForeignKey(McqOption, on_delete=models.CASCADE)