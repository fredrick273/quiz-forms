from django.urls import path
from . import views

urlpatterns = [
    path('createquiz/', views.createquiz ),
    path('listquiz/',views.quizlist , name='quiz_list'),
    path('quiz/<int:id>/',views.attemptquiz)

]