from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('createquiz/', views.createquiz ),
    path('listquiz/',views.quizlist , name='quiz_list'),
    path('quiz/<int:id>/',views.attemptquiz, name='attempt_quiz'),
    path('viewresponse/<int:response_id>/', views.view_attempted_response, name='view_attempted_response'),
    path('adminviewresponse/<int:response_id>/', views.admin_viewresponse, name='admin_view_response'),
    path('adminquizresponse/<int:id>/', views.view_quiz_reponses, name='adminquizresponse')
]