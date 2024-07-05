from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Quiz, TextQuestion,McqOption,MCQ,Response,TextAnswer,McqAnswer

# Create your views here.
@login_required
def createquiz(request):
    if request.method == 'POST':
        print(request.POST)
        title = request.POST.get('title')
        viewanswer = 'viewans' in request.POST
        showscore = 'showscore' in request.POST

        quiz = Quiz.objects.create(
            title=title,
            user=request.user,
            viewanswer=viewanswer,
            showscore=showscore
        )
        text_question_count = 1
        while True:
            text_question = request.POST.get(f'textquestion_{text_question_count}')
            if not text_question:
                break
            TextQuestion.objects.create(
                question=text_question,
                quiz=quiz
            )
            text_question_count += 1

        mcq_question_count = 1
        while True:
            mcq_question = request.POST.get(f'mcq_{mcq_question_count}')
            if not mcq_question:
                break
            points = request.POST.get(f'points_{mcq_question_count}')
            mcq = MCQ.objects.create(
                question=mcq_question,
                quiz=quiz,
                points=points
            )

            option_count = 1
            while True:
                option_text = request.POST.get(f'option_{mcq_question_count}_{option_count}')
                if not option_text:
                    break
                is_correct = f'correct_{mcq_question_count}_{option_count}' in request.POST
                McqOption.objects.create(
                    text=option_text,
                    is_correct=is_correct,
                    mcq=mcq
                )
                option_count += 1

            mcq_question_count += 1
        return redirect('quiz_list')
    return render(request,"quiz/createquiz.html")

def quizlist(request):
    return render(request,'quiz/quizlist.html',{'quizes': Quiz.objects.all()})

def attemptquiz(request,id):
    quiz = get_object_or_404(Quiz,id = id)
    if request.method == 'POST':
        
        res = Response(
            quiz = quiz
        )
        res.save()
        for i in request.POST:
            key = i.split('_')
            if key[0] == 'text':
                textans = TextAnswer(
                    question = TextQuestion.objects.get(id = int(key[1])),
                    response = res,
                    answer = request.POST.get(i)
                )
                textans.save()
            elif key[0] == 'mcq':
                print(MCQ.objects.get(id = int(key[1])),McqOption.objects.get(id = int(request.POST.get(i))))
                mcqans = McqAnswer(
                    question = MCQ.objects.get(id = int(key[1])),
                    response = res,
                    answer = McqOption.objects.get(id = int(request.POST.get(i)))
                )
                mcqans.save()
                print()
            print(key)
        return redirect('quiz_list')
    
    quiz = get_object_or_404(Quiz,id = id)
    textquestions = TextQuestion.objects.filter(quiz= quiz)
    mcqs = MCQ.objects.filter(quiz=quiz)
    mcqqustions = []
    for i in mcqs:
        options = McqOption.objects.filter(mcq = i)
        mcqqustions.append({
            'question': i,
            'options': options
        })
    print(mcqqustions)

    return render(request,'quiz/attemptquiz.html', {'quiz':quiz,'text':textquestions,'mcqs':mcqqustions})